#!/usr/bin/env python3
"""944 EV head-unit — dev backend (stdlib only, no pip installs).

Serves the web app + a MOCK telemetry/CAN API so you can run the whole thing on a
laptop with no car. On the real Pi, swap MockCan for a SocketCAN reader that decodes
openinverter frames (see the `read()` contract below).

  Run:  python3 app/backend/server.py     then open  http://localhost:8080

SAFETY: this app is NON-safety (ADR-0014). It only reads telemetry and writes BOUNDED
drive-mode presets. The VCU + BMS enforce all hard limits/interlocks independently.
"""
import csv
import io
import json
import math
import os
import sqlite3
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.join(HERE, "..", "frontend")
MODES_FILE = os.path.join(HERE, "..", "drive_modes.json")

with open(MODES_FILE) as f:
    MODES = json.load(f)["modes"]

# Simulated car conditions you can flip between to see the UI react.
SCENARIOS = ["CITY", "HIGHWAY", "CHARGING", "HOT DAY", "LOW BATTERY", "FAULT"]
STATE = {"mode": "NORMAL", "scenario": "CITY", "soc": 78.0, "t0": time.time(),
         "route_d": 0.0, "last_t": time.time()}

# Tunable VCU parameters (UI enforces these bounds; the VCU STILL clamps to hard limits).
PARAMS = {
    "max_torque_pct":       {"value": 100, "min": 20, "max": 100, "step": 5,  "unit": "%",   "label": "Max torque"},
    "max_current_a":        {"value": 350, "min": 50, "max": 450, "step": 10, "unit": "A",   "label": "Max current"},
    "regen_pct":            {"value": 60,  "min": 0,  "max": 100, "step": 5,  "unit": "%",   "label": "Regen strength"},
    "throttle_deadband_pct":{"value": 4,   "min": 0,  "max": 20,  "step": 1,  "unit": "%",   "label": "Throttle deadband"},
    "throttle_curve":       {"value": 50,  "min": 0,  "max": 100, "step": 5,  "unit": "",    "label": "Throttle curve (lin→sharp)"},
    "ramp_rate":            {"value": 50,  "min": 5,  "max": 100, "step": 5,  "unit": "",    "label": "Torque ramp"},
    "creep_torque_pct":     {"value": 0,   "min": 0,  "max": 30,  "step": 2,  "unit": "%",   "label": "Creep torque"},
    "speed_limit_mph":      {"value": 0,   "min": 0,  "max": 120, "step": 5,  "unit": "mph", "label": "Speed limit (0=off)"},
}

HISTORY = []          # rolling telemetry log for the trip graphs
HIST_MAX = 240        # ~2 min at 0.5 s sampling

# Mock GPS route — a loop the marker drives along, paced by the simulated speed.
ROUTE = [
    [37.7785, -122.4256], [37.7806, -122.4180], [37.7799, -122.4100],
    [37.7742, -122.4072], [37.7698, -122.4128], [37.7693, -122.4212],
    [37.7726, -122.4271], [37.7785, -122.4256],
]


def _haversine(a, b):
    R = 6371000.0
    la1, lo1, la2, lo2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2 * R * math.asin(math.sqrt(h))


_SEGS, _cum = [], 0.0
for _i in range(len(ROUTE) - 1):
    _L = _haversine(ROUTE[_i], ROUTE[_i + 1])
    _SEGS.append((_cum, ROUTE[_i], ROUTE[_i + 1], _L))
    _cum += _L
_TOTAL = _cum


def _pos_at(d):
    if _TOTAL <= 0:
        return ROUTE[0]
    d %= _TOTAL
    for start, p0, p1, L in _SEGS:
        if d <= start + L:
            f = (d - start) / L if L > 0 else 0.0
            return [p0[0] + (p1[0]-p0[0])*f, p0[1] + (p1[1]-p0[1])*f]
    return ROUTE[-1]


class MockCan:
    """Scenario-driven mock of the openinverter CAN telemetry. On the Pi, replace
    read() with decoded real frames; keep the same return contract."""

    def read(self):
        sc, t = STATE["scenario"], time.time() - STATE["t0"]
        warnings, charging = [], (sc == "CHARGING")

        if charging:
            speed, status = 0, "Charging"
            STATE["soc"] = min(100.0, STATE["soc"] + 0.03)
            kw = -6.6                                   # AC charging (negative = into pack)
        else:
            if sc == "HIGHWAY":
                speed = 68 + 6 * math.sin(t / 20)
            elif sc == "CITY":
                speed = max(0.0, 22 + 22 * math.sin(t / 8) + 8 * math.sin(t / 2))
            else:
                speed = max(0.0, 42 + 30 * math.sin(t / 12))
            cap = MODES[STATE["mode"]]["power_cap_kw"]
            kw = min(cap, speed * 0.45 + 16 * max(0.0, math.sin(t / 3)))
            if sc == "FAULT":
                kw = min(kw, 20)
                warnings.append("BMS FAULT — reduced power")
            STATE["soc"] = max(2.0, STATE["soc"] - kw * 0.00008)
            status = "Driving" if speed > 1 else "Ready"

        if sc == "LOW BATTERY":
            STATE["soc"] = min(STATE["soc"], 8.0)
        motor_c = 40 + abs(kw) * 0.25 + (35 if sc == "HOT DAY" else 0)
        inv_c = 38 + abs(kw) * 0.2 + (40 if sc == "HOT DAY" else 0)
        if STATE["soc"] <= 10:
            warnings.append("LOW BATTERY")
        if inv_c >= 78:
            warnings.append("INVERTER HOT — derating")
        if motor_c >= 95:
            warnings.append("MOTOR HOT")

        now = time.time()
        dt = max(0.0, min(2.0, now - STATE["last_t"]))
        STATE["last_t"] = now
        STATE["route_d"] += speed * 0.447 * dt          # mph→m/s, advance along the route
        lat, lon = _pos_at(STATE["route_d"])
        return {
            "mode": STATE["mode"], "scenario": sc, "status": status, "charging": charging,
            "warnings": warnings,
            "speed_mph": round(speed),
            "power_kw": round(kw, 1),
            "soc_pct": round(STATE["soc"], 1),
            "range_mi": round(STATE["soc"] / 100 * 74 * 0.9 / 0.30),
            "motor_c": round(motor_c), "inverter_c": round(inv_c),
            "pack_v": round(330 + STATE["soc"] * 0.4),
            "pack_a": round(kw * 1000 / 330),
            "wh_mi": round(250 + 80 * max(0.0, math.sin(t / 3))),
            "lat": round(lat, 6), "lon": round(lon, 6),
        }


# Telemetry source: real SocketCAN on the Pi (CAN_IFACE=can0), else the dev mock.
_iface = os.environ.get("CAN_IFACE")
if _iface:
    try:
        from can_source import SocketCanSource
        CAN = SocketCanSource(_iface, os.path.join(HERE, "..", "can_map.json"))
        print("Telemetry source: SocketCAN on", _iface)
    except Exception as e:
        print("SocketCAN unavailable (%r) — using MockCan" % e)
        CAN = MockCan()
else:
    print("Telemetry source: MockCan  (set CAN_IFACE=can0 on the Pi for real CAN)")
    CAN = MockCan()

# --- trip persistence (SQLite, stdlib) ---
DB_PATH = os.path.join(HERE, "..", "data", "trips.db")
os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
DB = sqlite3.connect(DB_PATH, check_same_thread=False)
DB_LOCK = threading.Lock()
DB.executescript("""
CREATE TABLE IF NOT EXISTS trips(
  id INTEGER PRIMARY KEY AUTOINCREMENT, started_at REAL, ended_at REAL,
  distance_mi REAL DEFAULT 0, kwh_used REAL DEFAULT 0,
  max_kw REAL DEFAULT 0, max_speed REAL DEFAULT 0, n INTEGER DEFAULT 0);
CREATE TABLE IF NOT EXISTS samples(
  id INTEGER PRIMARY KEY AUTOINCREMENT, trip_id INTEGER,
  t REAL, speed REAL, power REAL, soc REAL, motor REAL, inv REAL, lat REAL, lon REAL);
""")
DB.commit()
LAST_LOG_T = time.time()
CURRENT_TRIP = None


def start_trip():
    with DB_LOCK:
        cur = DB.execute("INSERT INTO trips(started_at, ended_at) VALUES(?,?)", (time.time(), time.time()))
        DB.commit()
        return cur.lastrowid


def new_trip():
    global CURRENT_TRIP
    CURRENT_TRIP = start_trip()
    return CURRENT_TRIP


def log_sample(d):
    global LAST_LOG_T
    now = time.time()
    dt = max(0.0, min(2.0, now - LAST_LOG_T))
    LAST_LOG_T = now
    dist = d["speed_mph"] * dt / 3600.0                 # miles this step
    kwh = max(0.0, d["power_kw"]) * dt / 3600.0          # energy drawn (positive only)
    with DB_LOCK:
        DB.execute("INSERT INTO samples(trip_id,t,speed,power,soc,motor,inv,lat,lon) VALUES(?,?,?,?,?,?,?,?,?)",
                   (CURRENT_TRIP, round(now - STATE["t0"], 1), d["speed_mph"], d["power_kw"],
                    d["soc_pct"], d["motor_c"], d["inverter_c"], d["lat"], d["lon"]))
        DB.execute("UPDATE trips SET ended_at=?, distance_mi=distance_mi+?, kwh_used=kwh_used+?, "
                   "max_kw=MAX(max_kw,?), max_speed=MAX(max_speed,?), n=n+1 WHERE id=?",
                   (now, dist, kwh, d["power_kw"], d["speed_mph"], CURRENT_TRIP))
        DB.commit()


def list_trips():
    with DB_LOCK:
        rows = DB.execute("SELECT id,started_at,ended_at,distance_mi,kwh_used,max_kw,max_speed,n "
                          "FROM trips ORDER BY id DESC LIMIT 50").fetchall()
    out = []
    for r in rows:
        dist = r[3]
        out.append({"id": r[0], "started_at": round(r[1]), "minutes": round((r[2]-r[1])/60, 1),
                    "distance_mi": round(dist, 2), "kwh_used": round(r[4], 2),
                    "wh_mi": round(r[4]*1000/dist) if dist > 0.05 else None,
                    "max_kw": round(r[5], 1), "max_speed": round(r[6]), "samples": r[7]})
    return out


def trip_samples(tid):
    with DB_LOCK:
        rows = DB.execute("SELECT t,speed,power,soc,motor,inv FROM samples WHERE trip_id=? ORDER BY id",
                          (tid,)).fetchall()
    return [{"t": r[0], "speed": r[1], "power": r[2], "soc": r[3], "motor": r[4], "inv": r[5]} for r in rows]


new_trip()   # start a fresh trip each server launch


class Handler(BaseHTTPRequestHandler):
    def log_message(self, *a):
        pass

    def _send(self, code, body, ctype="application/json"):
        b = body.encode() if isinstance(body, str) else body
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(b)))
        self.end_headers()
        self.wfile.write(b)

    def do_GET(self):
        if self.path in ("/", "/index.html"):
            try:
                with open(os.path.join(FRONTEND, "index.html"), "rb") as f:
                    self._send(200, f.read(), "text/html; charset=utf-8")
            except FileNotFoundError:
                self._send(404, "frontend/index.html not found")
        elif self.path == "/api/telemetry":
            data = CAN.read()
            data["mode"] = STATE["mode"]            # mode is app state, not from CAN
            log_sample(data)
            HISTORY.append({"t": data and round(time.time() - STATE["t0"], 1),
                            "speed": data["speed_mph"], "power": data["power_kw"],
                            "soc": data["soc_pct"], "motor": data["motor_c"], "inv": data["inverter_c"]})
            if len(HISTORY) > HIST_MAX:
                del HISTORY[0]
            self._send(200, json.dumps(data))
        elif self.path == "/api/modes":
            self._send(200, json.dumps({"active": STATE["mode"], "modes": MODES}))
        elif self.path == "/api/scenarios":
            self._send(200, json.dumps({"active": STATE["scenario"], "scenarios": SCENARIOS}))
        elif self.path == "/api/params":
            self._send(200, json.dumps({"params": PARAMS}))
        elif self.path == "/api/history":
            self._send(200, json.dumps({"samples": HISTORY}))
        elif self.path == "/api/route":
            self._send(200, json.dumps({"route": ROUTE}))
        elif self.path == "/api/trips":
            self._send(200, json.dumps({"trips": list_trips()}))
        elif self.path.startswith("/api/trip.csv?"):
            tid = int(parse_qs(urlparse(self.path).query).get("id", ["0"])[0])
            buf = io.StringIO()
            w = csv.writer(buf)
            w.writerow(["t_s", "speed_mph", "power_kw", "soc_pct", "motor_c", "inverter_c", "lat", "lon"])
            with DB_LOCK:
                rows = DB.execute("SELECT t,speed,power,soc,motor,inv,lat,lon FROM samples "
                                  "WHERE trip_id=? ORDER BY id", (tid,)).fetchall()
            for r in rows:
                w.writerow(r)
            body = buf.getvalue().encode()
            self.send_response(200)
            self.send_header("Content-Type", "text/csv")
            self.send_header("Content-Disposition", 'attachment; filename="trip-%d.csv"' % tid)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            self.wfile.write(body)
        elif self.path.startswith("/api/trip?"):
            tid = int(parse_qs(urlparse(self.path).query).get("id", ["0"])[0])
            self._send(200, json.dumps({"id": tid, "samples": trip_samples(tid)}))
        else:
            self._send(404, "not found")

    def do_POST(self):
        if self.path == "/api/mode":
            n = int(self.headers.get("Content-Length", 0) or 0)
            data = json.loads(self.rfile.read(n) or b"{}")
            m = data.get("mode")
            if m in MODES:
                STATE["mode"] = m              # bounded: only a known preset (VCU still clamps)
                getattr(CAN, "set_mode", lambda *a: None)(m, MODES[m])
                self._send(200, json.dumps({"active": m}))
            else:
                self._send(400, json.dumps({"error": "unknown mode"}))
        elif self.path == "/api/scenario":
            n = int(self.headers.get("Content-Length", 0) or 0)
            s = json.loads(self.rfile.read(n) or b"{}").get("scenario")
            if s in SCENARIOS:
                STATE["scenario"] = s
                self._send(200, json.dumps({"active": s}))
            else:
                self._send(400, json.dumps({"error": "unknown scenario"}))
        elif self.path == "/api/params":
            n = int(self.headers.get("Content-Length", 0) or 0)
            d = json.loads(self.rfile.read(n) or b"{}")
            name, val = d.get("name"), d.get("value")
            if name in PARAMS:
                p = PARAMS[name]
                p["value"] = max(p["min"], min(p["max"], val))   # BOUNDED clamp (VCU clamps again)
                getattr(CAN, "set_param", lambda *a: None)(name, p["value"])
                self._send(200, json.dumps({"name": name, "value": p["value"]}))
            else:
                self._send(400, json.dumps({"error": "unknown param"}))
        elif self.path == "/api/trip/new":
            self._send(200, json.dumps({"id": new_trip()}))
        else:
            self._send(404, "not found")


if __name__ == "__main__":
    print("944 EV head-unit (mock) → http://localhost:8080   (Ctrl-C to stop)")
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
