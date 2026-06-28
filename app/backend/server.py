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

# Mock GPS route — road-routed SE-Wisconsin loop (OSRM), ~128 mi.
# Menomonee Falls -> Pike Lake -> Holy Hill -> Sheboygan Dunes -> back to Menomonee Falls.
# Snapped to real roads; baked in (no runtime routing dependency — works offline on the Pi).
ROUTE = [
    [43.17889, -88.11700], [43.17930, -88.11415], [43.17923, -88.11218],
    [43.17926, -88.10748], [43.17915, -88.10440], [43.17975, -88.10357],
    [43.18112, -88.10295], [43.18270, -88.10208], [43.18375, -88.10210],
    [43.18432, -88.10233], [43.18421, -88.10316], [43.18450, -88.10549],
    [43.19168, -88.12101], [43.21063, -88.14395], [43.24366, -88.18101],
    [43.26004, -88.18151], [43.26920, -88.18328], [43.28202, -88.19323],
    [43.28264, -88.19333], [43.28196, -88.19505], [43.28165, -88.19605],
    [43.28088, -88.20038], [43.28094, -88.21465], [43.28095, -88.21848],
    [43.28101, -88.23123], [43.28109, -88.24632], [43.28115, -88.25582],
    [43.29062, -88.26082], [43.29566, -88.26685], [43.29571, -88.27667],
    [43.29586, -88.29351], [43.29724, -88.30010], [43.30321, -88.29994],
    [43.28987, -88.30026], [43.27718, -88.30057], [43.26379, -88.30091],
    [43.25484, -88.30104], [43.25086, -88.30412], [43.25124, -88.29951],
    [43.25127, -88.29164], [43.25228, -88.28603], [43.25136, -88.28134],
    [43.25138, -88.26363], [43.25128, -88.26177], [43.25131, -88.25465],
    [43.25116, -88.23562], [43.25093, -88.21272], [43.25084, -88.19669],
    [43.25078, -88.19150], [43.25070, -88.19100], [43.25077, -88.18714],
    [43.25062, -88.18071], [43.25064, -88.17740], [43.25018, -88.15136],
    [43.24315, -88.12971], [43.23869, -88.12120], [43.23617, -88.11742],
    [43.23552, -88.10707], [43.23553, -88.10170], [43.23554, -88.08371],
    [43.23564, -88.06679], [43.23583, -88.05005], [43.23598, -88.03537],
    [43.23613, -88.01389], [43.23625, -88.00404], [43.23902, -88.00358],
    [43.25058, -88.00366], [43.25075, -87.99427], [43.25069, -87.97842],
    [43.25062, -87.96216], [43.25066, -87.95602], [43.25073, -87.94655],
    [43.25073, -87.93949], [43.25051, -87.92581], [43.25029, -87.91953],
    [43.27343, -87.91999], [43.29226, -87.92047], [43.31827, -87.91957],
    [43.32757, -87.92024], [43.33912, -87.92447], [43.37512, -87.92580],
    [43.38947, -87.92830], [43.39110, -87.92825], [43.40059, -87.92547],
    [43.40597, -87.91806], [43.41092, -87.89447], [43.41154, -87.87419],
    [43.41525, -87.86367], [43.43691, -87.84077], [43.45067, -87.83250],
    [43.49007, -87.83076], [43.51012, -87.82594], [43.52844, -87.82132],
    [43.53409, -87.81821], [43.54183, -87.81209], [43.55738, -87.80551],
    [43.59155, -87.78471], [43.61637, -87.77022], [43.64465, -87.76890],
    [43.66647, -87.76196], [43.67445, -87.75960], [43.67507, -87.75711],
    [43.67387, -87.75549], [43.67333, -87.74736], [43.67305, -87.74038],
    [43.67278, -87.72555], [43.67262, -87.71813], [43.67253, -87.71794],
    [43.67211, -87.71792], [43.67161, -87.71819], [43.67134, -87.71830],
    [43.67111, -87.71839], [43.67038, -87.71893], [43.66862, -87.71935],
    [43.66797, -87.71769], [43.66688, -87.71721], [43.66789, -87.71753],
    [43.66860, -87.71924], [43.67022, -87.71902], [43.67108, -87.71842],
    [43.67133, -87.71798], [43.67151, -87.71776], [43.67207, -87.71746],
    [43.67225, -87.71744], [43.67247, -87.71756], [43.67262, -87.71776],
    [43.67266, -87.71808], [43.67280, -87.72642], [43.67310, -87.74166],
    [43.67336, -87.74819], [43.67406, -87.75591], [43.67578, -87.75778],
    [43.67202, -87.76123], [43.66618, -87.76251], [43.65251, -87.76890],
    [43.64466, -87.76934], [43.63030, -87.76987], [43.61956, -87.77052],
    [43.61283, -87.77134], [43.60368, -87.77699], [43.58966, -87.78642],
    [43.56936, -87.79873], [43.55012, -87.81031], [43.54423, -87.81185],
    [43.53795, -87.81492], [43.53133, -87.82064], [43.51367, -87.82477],
    [43.48579, -87.83080], [43.45378, -87.83261], [43.43879, -87.83906],
    [43.41739, -87.86188], [43.41257, -87.87012], [43.41177, -87.87601],
    [43.41127, -87.89394], [43.40647, -87.91751], [43.40105, -87.92850],
    [43.39104, -87.92927], [43.37922, -87.92708], [43.34851, -87.92510],
    [43.33437, -87.92399], [43.32409, -87.91964], [43.31077, -87.92078],
    [43.28357, -87.92152], [43.26930, -87.92005], [43.23590, -87.92007],
    [43.21977, -87.92155], [43.20986, -87.92119], [43.19312, -87.92441],
    [43.18151, -87.91979], [43.17764, -87.91834], [43.17702, -87.91902],
    [43.17709, -87.92669], [43.17787, -87.94464], [43.17821, -87.95465],
    [43.17854, -87.95916], [43.17859, -87.96197], [43.17835, -87.96596],
    [43.17785, -87.96947], [43.17780, -87.97366], [43.17780, -87.98020],
    [43.17779, -87.98455], [43.17788, -87.99229], [43.17790, -87.99650],
    [43.17796, -88.00211], [43.17795, -88.00880], [43.17794, -88.01146],
    [43.17790, -88.01591], [43.17786, -88.02077], [43.17781, -88.02530],
    [43.17772, -88.03462], [43.17846, -88.04109], [43.17876, -88.04426],
    [43.17840, -88.04735], [43.17734, -88.05325], [43.17705, -88.06347],
    [43.17735, -88.07275], [43.17734, -88.07750], [43.17754, -88.08137],
    [43.17826, -88.08736], [43.17776, -88.09128], [43.17719, -88.09484],
    [43.17756, -88.09704], [43.17852, -88.10001], [43.17907, -88.10164],
    [43.17926, -88.10344], [43.17927, -88.10608], [43.17924, -88.11097],
    [43.17932, -88.11368], [43.17900, -88.11622], [43.17889, -88.11700],
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
            self._send(200, json.dumps({"route": ROUTE, "dist_mi": round(_TOTAL / 1609.34, 1)}))
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
        else:
            self._send(404, "not found")


if __name__ == "__main__":
    print("944 EV head-unit (mock) → http://localhost:8080   (Ctrl-C to stop)")
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
