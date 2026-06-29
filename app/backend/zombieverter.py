"""ZombieVerter (openinverter) VCU integration module.

The ZombieVerter is the Vehicle Control Unit. The head-unit talks to it over CAN:
  - READ spot values  -> opmode/state, DC bus V/A, motor rpm, temps, last fault, firmware.
  - WRITE bounded params -> torque/regen/current limits, throttle cal, charge current.
  - SET opmode/drive-mode presets (ECO/NORMAL/SPORT/VALET -> param sets).

NON-SAFETY (ADR-0014): the ZombieVerter enforces ALL hard limits/interlocks itself. This module
only reads, and writes values the firmware re-clamps. On the bench (no board) the server uses
MockCan instead; on the Pi, point the server at ZombieVerterCAN (CAN_IFACE=can0).

openinverter SDO (CANopen-style) — CONFIRM node id + param ids against YOUR board's param db
(the board publishes it; dump with `oic`/the web UI). Defaults below are representative.
  request id 0x601, response 0x581 · read cmd 0x40, write cmd 0x23 · values fixed-point x32 (int32 LE)
"""
SDO_REQ, SDO_RESP = 0x601, 0x581
CMD_READ, CMD_WRITE, RESP_READ, RESP_ACK, RESP_ABORT = 0x40, 0x23, 0x43, 0x60, 0x80
FIXED = 32                                  # openinverter fixed-point scale

OPMODES = {0: "Off", 1: "Run", 2: "Precharge", 3: "PchFail", 4: "Charge", 5: "BoostBuck", 6: "Sine"}

# Tunable params (bounded here; the VCU clamps again). `id` = SDO param id — FILL from your board.
PARAMS = {
    "throtmax":  {"id": None, "min": 0,    "max": 100, "unit": "%", "default": 100, "label": "Max torque"},
    "throtmin":  {"id": None, "min": -100, "max": 0,   "unit": "%", "default": -30, "label": "Throttle regen"},
    "regenmax":  {"id": None, "min": 0,    "max": 100, "unit": "%", "default": 60,  "label": "Brake regen"},
    "idcmax":    {"id": None, "min": 0,    "max": 450, "unit": "A", "default": 350, "label": "DC limit (discharge)"},
    "idcmin":    {"id": None, "min": -250, "max": 0,   "unit": "A", "default": -120,"label": "DC limit (regen)"},
    "udcmin":    {"id": None, "min": 200,  "max": 360, "unit": "V", "default": 300, "label": "HV undervolt cutoff"},
    "udcmax":    {"id": None, "min": 360,  "max": 450, "unit": "V", "default": 410, "label": "HV overvolt cutoff"},
    "chargecur": {"id": None, "min": 0,    "max": 32,  "unit": "A", "default": 16,  "label": "AC charge current"},
}

# ZombieVerter spot value -> head-unit telemetry key (so the app contract is unchanged).
SPOT_TO_TELEMETRY = {
    "opmode": "vcu_state", "udc": "pack_v", "idc": "pack_a", "speed": "motor_rpm",
    "tmphs": "inverter_c", "tmpm": "motor_c", "lasterr": "vcu_fault", "version": "fw",
}

# Map a drive-mode preset (drive_modes.json) onto ZombieVerter params.
def mode_to_params(mode_cfg, pack_v=330):
    cap_kw = mode_cfg.get("power_cap_kw", 80)
    return {
        "throtmax": min(100, mode_cfg.get("throttle", 100)),
        "regenmax": mode_cfg.get("regen", 60),
        "idcmax":   min(450, round(cap_kw * 1000 / max(pack_v, 1))),   # kW cap -> DC amps
    }


def encode_write(param_id, value):
    """Build the 8-byte SDO write frame for an openinverter param (value -> fixed-point int32 LE)."""
    raw = int(round(value * FIXED)) & 0xFFFFFFFF
    return bytes([CMD_WRITE, param_id & 0xFF, (param_id >> 8) & 0xFF, 0,
                  raw & 0xFF, (raw >> 8) & 0xFF, (raw >> 16) & 0xFF, (raw >> 24) & 0xFF])


def decode_value(data):
    """Decode a fixed-point int32 LE value from an SDO read response payload (bytes 4..7)."""
    raw = int.from_bytes(bytes(data[4:8]), "little", signed=True)
    return raw / FIXED


class ZombieVerterCAN:
    """Real ZombieVerter over SocketCAN. Reads spot broadcasts, writes params via SDO.
    Returns the SAME telemetry dict shape as MockCan so the rest of the app is unchanged.
    Requires python-can + a configured can0 + the param ids filled in PARAMS."""

    def __init__(self, iface="can0", node=1):
        import can                                   # python-can (Pi only)
        self.bus = can.interface.Bus(channel=iface, bustype="socketcan")
        self.req_id = 0x600 + node
        self.resp_id = 0x580 + node
        self.spots = {}                              # latest decoded spot values

    def read(self):
        # Drain broadcast spot frames the ZombieVerter emits (map ids -> self.spots in your CAN map),
        # then translate to the head-unit telemetry contract.
        msg = self.bus.recv(timeout=0.02)
        # ... decode mapped spot frames into self.spots here (per can_map.json) ...
        s = self.spots
        return {
            "vcu_state": OPMODES.get(int(s.get("opmode", 0)), "Off"),
            "pack_v": s.get("udc", 0), "pack_a": s.get("idc", 0), "motor_rpm": s.get("speed", 0),
            "motor_c": s.get("tmpm", 0), "inverter_c": s.get("tmphs", 0),
            "vcu_fault": s.get("lasterr", 0), "fw": s.get("version", "?"),
            # speed/soc/gps come from other modules (BMS/GPS) on the real car
        }

    def get_param(self, name):
        p = PARAMS.get(name)
        if not p or p["id"] is None:
            return None
        import can
        self.bus.send(can.Message(arbitration_id=self.req_id, is_extended_id=False,
                                  data=bytes([CMD_READ, p["id"] & 0xFF, (p["id"] >> 8) & 0xFF, 0, 0, 0, 0, 0])))
        r = self.bus.recv(timeout=0.2)
        return decode_value(r.data) if r and r.arbitration_id == self.resp_id and r.data[0] == RESP_READ else None

    def set_param(self, name, value):
        p = PARAMS.get(name)
        if not p or p["id"] is None:
            return False
        value = max(p["min"], min(p["max"], value))     # bounded (firmware clamps again)
        import can
        self.bus.send(can.Message(arbitration_id=self.req_id, is_extended_id=False,
                                  data=encode_write(p["id"], value)))
        r = self.bus.recv(timeout=0.2)
        return bool(r and r.arbitration_id == self.resp_id and r.data[0] == RESP_ACK)

    def set_mode(self, name, cfg):
        for k, v in mode_to_params(cfg).items():
            self.set_param(k, v)
