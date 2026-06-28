"""Telemetry sources for the head unit.

- `MockCanSource` lives in server.py (scenario-driven sim; the laptop-dev default).
- `SocketCanSource` (here) reads the **real openinverter CAN bus** on the Pi via
  `python-can`, decoding frames per `app/can_map.json`.

server.py picks SocketCAN when `CAN_IFACE` is set (e.g. `CAN_IFACE=can0`) and
python-can + the interface are available; otherwise it falls back to the mock so the
app always runs.

⚠️ The openinverter CAN message IDs / bit positions are **configured in YOUR
ZombieVerter** (its "CAN mapping"), so they are NOT universal. Set `can_map.json` to
match your mapping. The values here are placeholders.
"""
import json
import threading


def extract_signal(data, start, length, endian="little", signed=False):
    """Pull an integer signal out of a CAN payload.

    data: up to 8 bytes. start: bit offset (from LSB for little-endian). length: bits.
    Little-endian (Intel) is fully supported; big-endian is approximate — verify.
    """
    raw = int.from_bytes(bytes(data).ljust(8, b"\x00"), byteorder=endian)
    val = (raw >> start) & ((1 << length) - 1)
    if signed and (val & (1 << (length - 1))):
        val -= (1 << length)
    return val


class SocketCanSource:
    """Reads real openinverter telemetry off a SocketCAN interface (Pi)."""

    def __init__(self, iface, map_path):
        import can  # python-can — only needed on the Pi; imported lazily

        with open(map_path) as f:
            self.signals = json.load(f)["signals"]
        # group signal definitions by CAN id for fast lookup
        self.by_id = {}
        for s in self.signals:
            self.by_id.setdefault(s["id"], []).append(s)

        self.vals = {}          # latest decoded value per field
        self.lock = threading.Lock()
        self.bus = can.interface.Bus(channel=iface, bustype="socketcan")
        threading.Thread(target=self._loop, daemon=True).start()

    def _loop(self):
        for msg in self.bus:                       # blocking iterator over frames
            ents = self.by_id.get(msg.arbitration_id)
            if not ents:
                continue
            with self.lock:
                for e in ents:
                    raw = extract_signal(msg.data, e["start"], e["len"],
                                         e.get("endian", "little"), e.get("signed", False))
                    self.vals[e["field"]] = raw * e.get("scale", 1) + e.get("offset", 0)

    def read(self):
        """Assemble the telemetry dict the frontend expects, from latest CAN values."""
        with self.lock:
            v = dict(self.vals)
        speed = v.get("speed_mph", 0)
        power = v.get("power_kw", 0)
        soc = v.get("soc_pct", 0)
        motor = v.get("motor_c", 0)
        inv = v.get("inverter_c", 0)
        charging = power < -0.5 and speed < 1
        warnings = []
        if soc and soc <= 10:
            warnings.append("LOW BATTERY")
        if inv >= 78:
            warnings.append("INVERTER HOT — derating")
        if motor >= 95:
            warnings.append("MOTOR HOT")
        status = "Charging" if charging else ("Driving" if speed > 1 else "Ready")
        return {
            "scenario": "LIVE", "status": status, "charging": charging, "warnings": warnings,
            "speed_mph": round(speed), "power_kw": round(power, 1), "soc_pct": round(soc, 1),
            "range_mi": round(soc / 100 * 74 * 0.9 / 0.30) if soc else 0,
            "motor_c": round(motor), "inverter_c": round(inv),
            "pack_v": round(v.get("pack_v", 0)), "pack_a": round(v.get("pack_a", 0)),
            "wh_mi": round(v.get("wh_mi", 0)),
            # GPS comes from gpsd (separate), not CAN — placeholder until wired:
            "lat": v.get("lat", 37.7749), "lon": v.get("lon", -122.4194),
        }

    # --- writes: drive-mode / param presets back to the VCU ---
    # The exact mechanism depends on your ZombieVerter config (CAN/serial/WiFi).
    # These are bounded by server.py; wire the actual frames here. NON-safety (ADR-0014).
    def set_mode(self, name, preset):
        pass  # TODO: send the preset's params to the VCU

    def set_param(self, name, value):
        pass  # TODO: send a single bounded param to the VCU
