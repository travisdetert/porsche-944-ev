# Reusing the 944 Dashboard for the EV

The classic 1987 944 cluster **stays** — we just re-source what each gauge reads now that gas
and oil are gone. Two gauges are essentially **native**; the rest are driven by a small
**CAN-to-gauge adapter** reading the ZombieVerter. Total new hardware: ~$20–50.

## Gauge-by-gauge mapping
| 944 gauge | Was driven by | EV reuse | How |
|---|---|---|---|
| **Speedometer** | transaxle cable / VSS | **same — wheel speed** | KEEP. The transaxle is kept, so the speedo drive still works. **Free.** |
| **Coolant temp** | engine coolant sender | **EV coolant temp** | Near-native: the inverter/motor still has a **coolant loop** — put a sender in it. |
| **Voltmeter** | 12 V system | **12 V system** | KEEP — still meaningful (DC-DC / 12 V health). |
| **Clock** | — | — | KEEP. |
| **Tachometer** | ignition pulses | **motor RPM** | CAN adapter outputs a scaled frequency to the tach input. |
| **Fuel gauge** | tank float sender | **STATE OF CHARGE** | CAN adapter drives the sender line; map SOC → needle. |
| **Oil pressure** | oil sender | **HV pack voltage** (relabel) | CAN adapter → match the gauge's sender curve. |
| **Oil temp** | oil sender | **battery temp** | CAN adapter → gauge. |
| **Warning lamps** | various | **faults** | batt/alt lamp → DC-DC fault · oil-press lamp → BMS/HV fault · brake lamp → keep. |

## The one new piece: a CAN-to-gauge adapter
- A small **ESP32 + CAN transceiver** (SN65HVD230 / MCP2515) reads the **ZombieVerter /
  openinverter CAN** bus and drives the analog gauges by **mimicking the original sender
  signals** — PWM→filtered voltage, a digital pot, or an op-amp current sink tuned to each
  gauge's curve.
- **~$20–50** in parts; openinverter community has example firmware. The **only** addition —
  cheap, and fully in the reuse spirit.

## Calibration (the fiddly bit, done once)
Each analog gauge wants a specific resistance/voltage for a given reading. For each repurposed
gauge, measure a few points (empty/full, cold/hot), then tune the adapter output so the needle
lands right. **Speedo + coolant-temp need ~none** (native); **tach / fuel / oil-press / oil-temp**
need this tuning — budget an afternoon.

## Relabel the repurposed gauges
A printed gauge-face overlay keeps it honest and classy: **FUEL → CHARGE**, **OIL PRESS → HV V**,
**OIL TEMP → BATT °**, **TEMP** stays. Speedo/voltmeter/clock unchanged.

## Optional
Some builders add a **small digital readout** (SOC %, kW, pack V) alongside for precision and
keep the analog dash for soul. Not required — the cluster alone covers driving + inspection.

## Reuse win
The **entire 944 cluster stays** — original needles now showing EV data. Speedo and coolant-temp
are basically free; everything else rides a **~$30 CAN adapter**. Classic dash, electric heart.

> Decision: `adr/0012` · Power/CAN context: `power-and-reuse-diagrams.md` · Parts: `parts-inventory.md`.
