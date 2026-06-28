# 944 EV — Head-Unit App

The custom touchscreen **head unit**: live telemetry, **drive modes**, **maps**, and (on the Pi)
phone connectivity. Built as a **local web app** — the Pi touchscreen runs it full-screen, and
any phone on the car's WiFi opens the same URL. Design: `../docs/control-computer.md` · decision:
`../docs/adr/0014-pi-infotainment-control-app.md`.

> ⚠️ **Non-safety (ADR-0014).** This app only **reads** telemetry and **writes bounded** drive-mode
> presets. The **VCU + BMS enforce all hard limits/interlocks** independently — the app can crash
> and the car stays safe and drivable. Keep it **offline** (it's on the drivetrain CAN bus).

## Run the dev mock (no car, no installs)
```
python3 app/backend/server.py      # then open http://localhost:8080
```
Pure stdlib. You'll see live telemetry, a moving map, drive-mode buttons, and a **"Simulate car
condition"** row — flip between **CITY / HIGHWAY / CHARGING / HOT DAY / LOW BATTERY / FAULT** and
watch the dashboard react (charging icon, derate + hot warnings, low-battery chip, fault power cut).

## What's mocked vs real
- `backend/server.py` → **`MockCan`** generates scenario-driven telemetry. On the Pi, replace
  `MockCan.read()` with a **SocketCAN** reader that decodes openinverter frames — same return
  contract, everything else unchanged.
- `drive_modes.json` → the presets (power cap, regen, throttle, speed cap). Edit freely; writing a
  mode = sending its params to the VCU (which still clamps to hard limits).
- Maps use **OpenStreetMap tiles via CDN** for dev. In the car, **pre-cache tiles** for offline use.

## Files
```
app/
├── backend/server.py     # stdlib web server + MockCan + telemetry/mode/scenario API
├── frontend/index.html   # touchscreen UI: telemetry + map + drive modes + condition sim
├── drive_modes.json      # drive-mode presets (version-controlled)
└── README.md
```

## API
| Route | Returns |
|---|---|
| `GET /api/telemetry` | live telemetry (speed, kW, SOC, temps, pack, GPS, status, warnings) |
| `GET /api/modes` · `POST /api/mode {mode}` | drive modes / set mode |
| `GET /api/scenarios` · `POST /api/scenario {scenario}` | mock conditions / set condition |

## Deploy to the Pi (later)
SocketCAN (`can0`) + swap in the real CAN reader · kiosk Chromium full-screen · Pi as WiFi **AP**
(phone joins → same app) · **gpsd** for GPS · offline tile cache · 12 V→5 V + UPS for clean shutdown.
