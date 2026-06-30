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
import mimetypes
import os
import sqlite3
import threading
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs

HERE = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.abspath(os.path.join(HERE, "..", "frontend"))
MODES_FILE = os.path.join(HERE, "..", "drive_modes.json")

with open(MODES_FILE) as f:
    MODES = json.load(f)["modes"]

# Simulated car conditions you can flip between to see the UI react.
SCENARIOS = ["CITY", "HIGHWAY", "CHARGING", "HOT DAY", "LOW BATTERY", "FAULT"]
STATE = {"mode": "NORMAL", "scenario": "CITY", "soc": 78.0, "t0": time.time(),
         "route_d": 0.0, "last_t": time.time(), "regen_kwh": 0.0, "kwh_throughput": 0.0}

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

# Mock GPS routes — road-routed (OSRM), loaded from app/routes.json. Several Wisconsin trips
# so we can drive each and check hardware coverage; the marker drives the ACTIVE route.
ROUTES_FILE = os.path.join(HERE, "..", "routes.json")
try:
    with open(ROUTES_FILE) as f:
        ROUTES = json.load(f)
except Exception:
    ROUTES = {"SE-WI loop": {"loop": True, "dist_mi": 0.0,
              "poly": [[43.1789, -88.1170], [43.30, -88.30], [43.1789, -88.1170]]}}
DEFAULT_ROUTE = "SE-WI loop" if "SE-WI loop" in ROUTES else next(iter(ROUTES))
STATE["route"] = DEFAULT_ROUTE


def _haversine(a, b):
    R = 6371000.0
    la1, lo1, la2, lo2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    h = math.sin((la2-la1)/2)**2 + math.cos(la1)*math.cos(la2)*math.sin((lo2-lo1)/2)**2
    return 2 * R * math.asin(math.sqrt(h))


_SEGS, _TOTAL = [], 0.0


def set_route(name):
    global _SEGS, _TOTAL
    poly = ROUTES.get(name, {}).get("poly", [])
    segs, cum = [], 0.0
    for i in range(len(poly) - 1):
        L = _haversine(poly[i], poly[i + 1])
        segs.append((cum, poly[i], poly[i + 1], L))
        cum += L
    _SEGS, _TOTAL = segs, cum
    STATE["route"] = name
    STATE["route_d"] = 0.0


set_route(STATE["route"])


def _pos_at(d):
    if _TOTAL <= 0:
        return ROUTES[STATE['route']]['poly'][0]
    d %= _TOTAL
    for start, p0, p1, L in _SEGS:
        if d <= start + L:
            f = (d - start) / L if L > 0 else 0.0
            return [p0[0] + (p1[0]-p0[0])*f, p0[1] + (p1[1]-p0[1])*f]
    return ROUTES[STATE['route']]['poly'][-1]


class MockCan:
    """Scenario-driven mock of the openinverter CAN telemetry. On the Pi, replace
    read() with decoded real frames; keep the same return contract."""

    def read(self):
        sc, t = STATE["scenario"], time.time() - STATE["t0"]
        warnings, charging = [], (sc == "CHARGING")
        cap = MODES[STATE["mode"]]["power_cap_kw"]
        now = time.time()
        dt = max(0.0, min(2.0, now - STATE["last_t"]))
        STATE["last_t"] = now

        if charging:
            speed, status, vcu, gear = 0.0, "Charging", "Charge", "P"
            STATE["soc"] = min(100.0, STATE["soc"] + 0.03)
            charge_kw, kw = 6.6, -6.6                   # AC L2 (negative = into pack)
        else:
            if sc == "HIGHWAY":
                speed = 68 + 6 * math.sin(t / 20)
            elif sc == "CITY":
                speed = max(0.0, 22 + 22 * math.sin(t / 8) + 8 * math.sin(t / 2))
            else:
                speed = max(0.0, 42 + 30 * math.sin(t / 12))
            kw = max(-40.0, min(cap, speed * 0.40 + 24 * math.sin(t / 3.5)))   # downswing → regen
            if sc == "FAULT":
                kw = min(kw, 18)
                warnings.append("BMS FAULT — reduced power")
            STATE["soc"] = max(2.0, min(100.0, STATE["soc"] - kw * 0.00008))
            status = "Driving" if speed > 1 else "Ready"
            vcu = "Fault" if sc == "FAULT" else ("Run" if speed > 1 else "Ready")
            gear = "D" if speed > 1 else "N"
            charge_kw = 0.0

        if sc == "LOW BATTERY":
            STATE["soc"] = min(STATE["soc"], 8.0)
        soc = STATE["soc"]

        drive_kw = max(0.0, kw)
        regen_kw = 0.0 if charging else max(0.0, -kw)
        STATE["regen_kwh"] += regen_kw * dt / 3600.0
        STATE["kwh_throughput"] += abs(kw) * dt / 3600.0
        STATE["route_d"] += speed * 0.447 * dt          # mph→m/s, advance along the route
        lat, lon = _pos_at(STATE["route_d"])

        # --- HV pack + per-cell BMS model (96S; one weak cell at index 7) ---
        pack_v = 300 + soc * 0.9
        pack_a = kw * 1000.0 / pack_v
        cell_avg_base = pack_v / 96.0 - 0.00018 * pack_a        # load sag
        spread = 0.012 + (1 - soc / 100) * 0.05 + min(0.045, abs(pack_a) / 2500.0)
        cells, weak = [], 7
        for i in range(24):                              # 24 module groups
            off = 0.45 * spread * math.sin(i * 2.3 + t * 0.25)
            if i == weak:
                off -= spread * 0.9
            cells.append(round(cell_avg_base + off, 3))
        cmin, cmax = min(cells), max(cells)
        cavg, cdelta = sum(cells) / len(cells), cmax - cmin

        # --- temps / thermal ---
        amb = 22 + (15 if sc == "HOT DAY" else 0)
        motor_c = 40 + abs(kw) * 0.25 + (35 if sc == "HOT DAY" else 0)
        inv_c = 38 + abs(kw) * 0.20 + (40 if sc == "HOT DAY" else 0)
        cell_t_avg = amb + abs(kw) * 0.10 + (4 if charging else 0)
        cell_t_min, cell_t_max = cell_t_avg - 1.5, cell_t_avg + 3.5 + abs(pack_a) / 200.0
        rad_fan = max(0.0, min(100.0, (max(motor_c, inv_c) - 45) * 4))
        pump = 100 if (speed > 1 or charging) else 30

        # --- limits / safety / aux ---
        soh = 92.5
        dcl_a = round(400 * min(1.0, soc / 12.0) * (1 - max(0.0, cell_t_max - 45) / 40.0))
        ccl_a = 0 if soc >= 100 else round(125 * (1 - soc / 100.0) * (1 - max(0.0, cell_t_max - 40) / 40.0))
        iso_kohm = 80 if sc == "FAULT" else round(900 - soc * 1.5 + 60 * math.sin(t / 30))
        contactor = "Open" if sc == "FAULT" else "Closed"
        dcdc_v = round(13.9 - (0.4 if (speed > 1 or charging) else 0.1) - 0.01 * abs(kw), 1)
        aux_a = round(9 + (12 if speed > 1 else 0) + (6 if charging else 0))

        # --- motor mechanics ---
        motor_rpm = round(speed * 150)
        omega = motor_rpm * 2 * math.pi / 60
        torque_act = round(min(320.0, kw * 1000 / omega)) if omega > 5 else 0
        torque_cmd = round(min(320.0, cap * 1000 / omega)) if omega > 5 else 0
        pedal = max(0, min(100, round(drive_kw / cap * 100))) if cap else 0

        # --- energy ---
        wh_mi = round(kw * 1000 / speed) if speed > 3 else 0
        range_mi = round(soc / 100 * 74 * 0.9 / 0.30)
        ttf = round((100 - soc) / 100 * 74 / max(charge_kw, 0.1) * 60) if charging else None

        # --- warnings ---
        if soc <= 10:
            warnings.append("LOW BATTERY")
        if inv_c >= 78:
            warnings.append("INVERTER HOT — derating")
        if motor_c >= 95:
            warnings.append("MOTOR HOT")
        if cdelta >= 0.12:
            warnings.append("CELL IMBALANCE")
        if cell_t_max >= 50:
            warnings.append("PACK HOT")
        if iso_kohm < 100:
            warnings.append("ISOLATION FAULT")

        return {
            "mode": STATE["mode"], "scenario": sc, "status": status, "charging": charging,
            "warnings": warnings, "vcu_state": vcu, "gear": gear,
            "vcu_fault": ("OVERCURRENT" if sc == "FAULT" else "none"), "fw": "ZV 5.24.R",
            # powertrain
            "speed_mph": round(speed), "power_kw": round(kw, 1),
            "drive_kw": round(drive_kw, 1), "regen_kw": round(regen_kw, 1),
            "motor_rpm": motor_rpm, "torque_cmd_nm": torque_cmd, "torque_act_nm": torque_act,
            "pedal_pct": pedal, "motor_c": round(motor_c), "inverter_c": round(inv_c),
            # battery / BMS
            "soc_pct": round(soc, 1), "soh_pct": soh, "range_mi": range_mi,
            "pack_v": round(pack_v, 1), "pack_a": round(pack_a),
            "cell_v_min": round(cmin, 3), "cell_v_max": round(cmax, 3),
            "cell_v_avg": round(cavg, 3), "cell_v_delta": round(cdelta, 3),
            "cells": cells, "weak_cell": weak,
            "cell_t_min": round(cell_t_min, 1), "cell_t_avg": round(cell_t_avg, 1),
            "cell_t_max": round(cell_t_max, 1),
            "dcl_a": dcl_a, "ccl_a": ccl_a, "iso_kohm": iso_kohm, "contactor": contactor,
            "cycle_count": 142, "kwh_throughput": round(STATE["kwh_throughput"], 2),
            # thermal
            "ambient_c": round(amb), "coolant_motor_c": round(motor_c - 6),
            "coolant_batt_c": round(cell_t_avg + 1), "rad_fan_pct": round(rad_fan), "pump_pct": pump,
            # 12V / aux
            "dcdc_v": dcdc_v, "aux_a": aux_a,
            # energy
            "wh_mi": wh_mi, "regen_kwh": round(STATE["regen_kwh"], 2),
            # charging
            "charge_kw": round(charge_kw, 1), "time_to_full_min": ttf,
            # gps
            "lat": round(lat, 6), "lon": round(lon, 6),
        }


# Telemetry source: ZombieVerter VCU or generic SocketCAN on the Pi, else the dev mock.
_iface = os.environ.get("CAN_IFACE")
_driver = os.environ.get("CAN_DRIVER", "")           # set CAN_DRIVER=zombieverter to use the VCU module
if _iface and _driver == "zombieverter":
    try:
        from zombieverter import ZombieVerterCAN
        CAN = ZombieVerterCAN(_iface)
        print("Telemetry source: ZombieVerter VCU on", _iface)
    except Exception as e:
        print("ZombieVerter unavailable (%r) — using MockCan" % e)
        CAN = MockCan()
elif _iface:
    try:
        from can_source import SocketCanSource
        CAN = SocketCanSource(_iface, os.path.join(HERE, "..", "can_map.json"))
        print("Telemetry source: SocketCAN on", _iface)
    except Exception as e:
        print("SocketCAN unavailable (%r) — using MockCan" % e)
        CAN = MockCan()
else:
    print("Telemetry source: MockCan  (set CAN_IFACE=can0 + CAN_DRIVER=zombieverter on the Pi)")
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
# migrate older DBs: add the BMS / Wh-per-mile sample columns if missing
_cols = {r[1] for r in DB.execute("PRAGMA table_info(samples)")}
for _c in ("cell_min", "cell_max", "cell_delta", "cell_tmax", "wh_mi"):
    if _c not in _cols:
        DB.execute("ALTER TABLE samples ADD COLUMN %s REAL" % _c)
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
        DB.execute("INSERT INTO samples(trip_id,t,speed,power,soc,motor,inv,lat,lon,"
                   "cell_min,cell_max,cell_delta,cell_tmax,wh_mi) "
                   "VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?)",
                   (CURRENT_TRIP, round(now - STATE["t0"], 1), d["speed_mph"], d["power_kw"],
                    d["soc_pct"], d["motor_c"], d["inverter_c"], d["lat"], d["lon"],
                    d.get("cell_v_min"), d.get("cell_v_max"), d.get("cell_v_delta"),
                    d.get("cell_t_max"), d.get("wh_mi")))
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
        rows = DB.execute("SELECT t,speed,power,soc,motor,inv,cell_delta,cell_tmax,wh_mi "
                          "FROM samples WHERE trip_id=? ORDER BY id", (tid,)).fetchall()
    return [{"t": r[0], "speed": r[1], "power": r[2], "soc": r[3], "motor": r[4], "inv": r[5],
             "cell_delta": r[6], "cell_tmax": r[7], "wh_mi": r[8]} for r in rows]


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
                            "soc": data["soc_pct"], "motor": data["motor_c"], "inv": data["inverter_c"],
                            "cell_delta": data["cell_v_delta"], "cell_tmax": data["cell_t_max"],
                            "wh_mi": data["wh_mi"]})
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
            name = STATE["route"]; r = ROUTES.get(name, {})
            self._send(200, json.dumps({"name": name, "route": r.get("poly", []),
                                        "dist_mi": r.get("dist_mi", round(_TOTAL / 1609.34, 1)),
                                        "loop": r.get("loop", False)}))
        elif self.path == "/api/routes":
            self._send(200, json.dumps({"active": STATE["route"], "routes": [
                {"name": k, "dist_mi": v.get("dist_mi", 0), "loop": v.get("loop", False)}
                for k, v in ROUTES.items()]}))
        elif self.path.startswith("/api/doc"):
            name = parse_qs(urlparse(self.path).query).get("name", ["BOM"])[0]
            if not all(c.isalnum() or c in "-_" for c in name):     # whitelist → no traversal
                self._send(400, "bad doc name"); return
            try:
                with open(os.path.join(HERE, "..", "..", "docs", name + ".md"), encoding="utf-8") as f:
                    self._send(200, f.read(), "text/markdown; charset=utf-8")
            except FileNotFoundError:
                self._send(404, "doc not found")
        elif self.path.startswith("/api/svg"):
            q = parse_qs(urlparse(self.path).query)
            d = q.get("dir", ["images"])[0]; name = q.get("name", [""])[0]
            if d not in ("images", "cad") or not all(c.isalnum() or c in "-_" for c in name):
                self._send(400, "bad svg"); return
            try:
                with open(os.path.join(HERE, "..", "..", d, name + ".svg"), encoding="utf-8") as f:
                    self._send(200, f.read(), "image/svg+xml")
            except FileNotFoundError:
                self._send(404, "svg not found")
        elif self.path == "/api/trips":
            self._send(200, json.dumps({"trips": list_trips()}))
        elif self.path.startswith("/api/trip.csv?"):
            tid = int(parse_qs(urlparse(self.path).query).get("id", ["0"])[0])
            buf = io.StringIO()
            w = csv.writer(buf)
            w.writerow(["t_s", "speed_mph", "power_kw", "soc_pct", "motor_c", "inverter_c",
                        "cell_v_min", "cell_v_max", "cell_delta", "cell_t_max", "wh_mi", "lat", "lon"])
            with DB_LOCK:
                rows = DB.execute("SELECT t,speed,power,soc,motor,inv,cell_min,cell_max,cell_delta,"
                                  "cell_tmax,wh_mi,lat,lon FROM samples "
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
            self._serve_static(self.path)

    def _serve_static(self, path):
        full = os.path.normpath(os.path.join(FRONTEND, urlparse(path).path.lstrip("/")))
        if not full.startswith(FRONTEND) or not os.path.isfile(full):   # no path traversal
            self._send(404, "not found")
            return
        if full.endswith(".glb"):
            ctype = "model/gltf-binary"
        elif full.endswith(".gltf"):
            ctype = "model/gltf+json"
        else:
            ctype = mimetypes.guess_type(full)[0] or "application/octet-stream"
        with open(full, "rb") as f:
            self._send(200, f.read(), ctype)

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
        elif self.path == "/api/route":
            n = int(self.headers.get("Content-Length", 0) or 0)
            name = json.loads(self.rfile.read(n) or b"{}").get("name")
            if name in ROUTES:
                set_route(name)
                self._send(200, json.dumps({"active": name, "dist_mi": ROUTES[name].get("dist_mi", 0)}))
            else:
                self._send(400, json.dumps({"error": "unknown route"}))
        else:
            self._send(404, "not found")


if __name__ == "__main__":
    print("944 EV head-unit (mock) → http://localhost:8080   (Ctrl-C to stop)")
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
