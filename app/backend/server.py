#!/usr/bin/env python3
"""944 EV head-unit — dev backend (stdlib only, no pip installs).

Serves the web app + a MOCK telemetry/CAN API so you can run the whole thing on a
laptop with no car. On the real Pi, swap MockCan for a SocketCAN reader that decodes
openinverter frames (see the `read()` contract below).

  Run:  python3 app/backend/server.py     then open  http://localhost:8080

SAFETY: this app is NON-safety (ADR-0014). It only reads telemetry and writes BOUNDED
drive-mode presets. The VCU + BMS enforce all hard limits/interlocks independently.
"""
import json
import math
import os
import time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

HERE = os.path.dirname(os.path.abspath(__file__))
FRONTEND = os.path.join(HERE, "..", "frontend")
MODES_FILE = os.path.join(HERE, "..", "drive_modes.json")

with open(MODES_FILE) as f:
    MODES = json.load(f)["modes"]

# Simulated car conditions you can flip between to see the UI react.
SCENARIOS = ["CITY", "HIGHWAY", "CHARGING", "HOT DAY", "LOW BATTERY", "FAULT"]
STATE = {"mode": "NORMAL", "scenario": "CITY", "soc": 78.0, "t0": time.time()}

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

        lat = 37.7749 + 0.012 * math.sin(t / 30)
        lon = -122.4194 + 0.012 * math.cos(t / 30)
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


CAN = MockCan()


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
        else:
            self._send(404, "not found")

    def do_POST(self):
        if self.path == "/api/mode":
            n = int(self.headers.get("Content-Length", 0) or 0)
            data = json.loads(self.rfile.read(n) or b"{}")
            m = data.get("mode")
            if m in MODES:
                STATE["mode"] = m              # bounded: only a known preset (VCU still clamps)
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
                self._send(200, json.dumps({"name": name, "value": p["value"]}))
            else:
                self._send(400, json.dumps({"error": "unknown param"}))
        else:
            self._send(404, "not found")


if __name__ == "__main__":
    print("944 EV head-unit (mock) → http://localhost:8080   (Ctrl-C to stop)")
    ThreadingHTTPServer(("0.0.0.0", 8080), Handler).serve_forever()
