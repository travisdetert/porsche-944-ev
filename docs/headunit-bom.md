# Head-Unit Hardware BOM — sourcing list

The dash is already **double-DIN**, so no bezel fab. The plan: a **Raspberry Pi behind the
screen** runs the app (`../app/`) in **kiosk Chromium**, reads the drivetrain **CAN** bus, and
acts as the car's **Wi-Fi AP** (phone joins → same URL). Architecture + safety: ADR-0014
(non-safety; VCU/BMS independent). Prices are **estimates** (2025–26), check current vendors.

## Path A — Pi-native screen (recommended: our app runs natively, no Android cruft)
| # | Part | Pick | ~$ | Why |
|---|---|---|---|---|
| 1 | Compute | **Raspberry Pi 5 (4 GB)** | 60 | runs Chromium kiosk + SocketCAN + Wi-Fi AP |
| 2 | Storage | 32 GB A2 microSD | 8 | OS + tile cache |
| 3 | Cooling | Active cooler / case | 10 | hot cabin — keep it cool |
| 4 | **Screen** | **7″ double-DIN capacitive touch, HDMI + USB-touch, 1024×600** | 70–90 | the display; drops into your double-DIN |
| 5 | **CAN** | **2-ch CAN HAT** (Waveshare MCP2515/2517) | 20 | reads openinverter frames → swap MockCan for SocketCAN (`can0`) |
| 6 | Power | 12 V→5 V/5 A car buck (UBEC) | 10 | clean 5 V from the 12 V rail |
| 7 | Clean shutdown | UPS / ignition-shutdown HAT (LiFePO4 UPS or Mausberry) | 25 | graceful power-off on key-off → no SD corruption |
| 8 | GPS | USB u-blox GPS + `gpsd` *(or use the phone)* | 12 | map position |
| 9 | Wiring | inline fuse, CAN/Dupont harness, connectors | 15 | tidy + fused |
| | | **Subtotal** | **~$230–260** | |

## Path B — reuse an Android double-DIN as the display (cheapest if you already have one)
Keep the Android double-DIN as the screen; run the app in a **kiosk browser** (e.g. *Fully
Kiosk Browser*) pointed at the Pi. You still need the **Pi + CAN HAT + power** behind it
(items 1,2,3,5,6,7,9 ≈ **$140**) because the Android unit can't reliably read the drivetrain CAN.

## Bench kit — try it on the desk THIS WEEK (no car, no CAN)
Items 1+2+3+6 (Pi + SD + cooler + USB-C power) and **any HDMI monitor**. Flash Pi OS, run
`python3 app/backend/server.py`, open Chromium fullscreen → the whole app runs on **mock data**.
Add the CAN HAT (5) + a USB-CAN/known-good source later to bring in real frames.

## Setup checklist (once parts arrive)
- [ ] Flash Pi OS (Lite + Chromium kiosk, or Desktop), enable SSH + Wi-Fi.
- [ ] `git clone` this repo; `python3 app/backend/server.py` as a systemd service on boot.
- [ ] Chromium kiosk autostart → `http://localhost:8080`.
- [ ] Bring up SocketCAN (`can0`), set `CAN_IFACE=can0`, fill `app/can_map.json` with the real IDs.
- [ ] Configure the Pi as a Wi-Fi **AP** (hostapd) so the phone joins and opens the same URL.
- [ ] Wire 12 V (switched/ignition) → buck → UPS HAT → Pi; test clean shutdown on key-off.
- [ ] Pre-cache map tiles for offline; verify GPS via `gpsd`.

> Bench it first (mock data) before any HV work — it's the cheap, safe way to shake out the app.
