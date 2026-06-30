# Pi ↔ ZombieVerter (motor-controller) integration

How the Raspberry Pi head unit physically and logically joins the **drivetrain CAN bus** to read
the ZombieVerter VCU + BMS + inverter + charger and write bounded drive-mode presets. Pulls
together: `control-computer.md` (architecture), `control-wiring.md` (LV control), `../app/backend/
zombieverter.py` (SDO + params), `../app/can_map.json` (decode), `../deploy/` (Pi setup).

> **NON-safety (ADR-0014).** The Pi is one more **node** on the bus. The VCU + BMS run the safety
> loop in real time. The Pi only **listens** + writes values the firmware re-clamps. Pi off = car
> drives fine.

## Bus topology
One **500 kbit/s** drivetrain CAN bus links the nodes; the Pi (via a CAN HAT) is just another node.
```mermaid
flowchart LR
  subgraph BUS["Drivetrain CAN @ 500 kbit/s (twisted pair CANH/CANL)"]
    VCU["ZombieVerter VCU"]
    INV["Leaf inverter"]
    BMS["BMS / LBC"]
    PDM["PDM (charger + DC-DC)"]
    GAUGE["CAN→gauge adapter (ADR-0012)"]
    PI["Raspberry Pi + CAN HAT (MCP2515)"]
  end
  VCU --- INV --- BMS --- PDM --- GAUGE --- PI
  T1["120 Ω term"]:::t --- VCU
  PI --- T2["120 Ω term"]:::t
  classDef t fill:#1a1a1a,stroke:#555,color:#9aa;
```
The two **120 Ω terminators live at the two physical ends** of the bus — not at every node.

**Wiring diagram:** `../images/pi-vcu-can-wiring.svg` (bus, terminators, nodes, ground, power).

## Physical hookup (CAN HAT → bus)
- **CANH ↔ CANH, CANL ↔ CANL**, as a **twisted pair**, tapped into the VCU's CAN connector (or a
  bus junction). Keep the pair **away from the inverter/HV cables** (noise) and short stubs.
- **Termination:** the bus needs **120 Ω at each end**, ~60 Ω total measured across CANH–CANL with
  power off. The CAN HAT usually has a **selectable 120 Ω jumper** — enable it **only if the Pi sits
  at a bus end**; otherwise leave it off. The VCU end is typically already terminated.
- **Ground reference:** tie the Pi/HAT **0 V (GND) to the VCU's signal ground** (the LV/12 V return),
  not just chassis — CAN needs a common reference. Use the same 12 V→5 V supply ground.
- **Bus speed:** set the ZombieVerter and `can0` to the **same bitrate (500 k default)** — mismatch =
  no comms / bus-off. `deploy/can0.service` brings `can0` up at 500 k.
- **Power:** 12 V **switched/ignition** → buck (5 V/5 A) → Pi, with the **ignition-shutdown UPS HAT**
  for clean power-off (no SD corruption). See `headunit-bom.md`.

### Option B — isolated infotainment bus (later, optional)
To keep the Pi fully off the safety-critical bus, run a **second CAN** and have the VCU **re-broadcast**
only the frames the Pi needs onto it. More wiring/config; cleaner isolation. Not needed for v1 — the
Pi is already read-mostly + bounded.

## Logical / data contract
- **Read:** the VCU (and BMS/PDM) **broadcast spot frames**; the Pi decodes them per `app/can_map.json`
  (`id` / bit offset / length / scale / offset) into the head-unit telemetry fields. On the Pi set
  `CAN_IFACE=can0` (+ `CAN_DRIVER=zombieverter` to use the VCU module).
- **Write (bounded):** drive-mode presets → ZombieVerter params via **CANopen-style SDO** (req `0x601`
  / resp `0x581`, values fixed-point ×32) — see `zombieverter.py`. The firmware **re-clamps** to hard
  limits. The Pi never touches contactor/precharge/interlock logic.
- **Param ids:** the SDO `id`s and the spot-frame mappings are **specific to YOUR VCU config** — dump
  the board's param db / CAN map and fill `app/can_map.json` + `PARAMS[].id`.

## Bring-up / bench-verify (gate G5, step 012)
1. Wire CANH/CANL + common ground; set both ends terminated; power the Pi from 12 V.
2. `ip -details link show can0` → up @ 500 k. `candump can0` → you should see the VCU's frames.
3. Match each frame to a field → fill `app/can_map.json`; confirm the **DATA/DASH** tabs read live.
4. Test **one bounded SDO write** (e.g. a low `throtmax`) → confirm the VCU accepts + re-clamps, and
   `opmode/faults` show in **TUNE**.
5. Only then proceed to power-up on stands (G6).

## What the Pi does NOT do (by design)
Contactor/precharge sequencing · HVIL/interlock · BMS limits · charge inhibit · torque safety — **all
the VCU + BMS**, independently and in real time (`control-wiring.md` interlocks). The Pi is the
**dashboard + tuner + logger**, nothing more.
