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
Pure stdlib. Three tabs:
- **DRIVE** — live telemetry + a map where the marker **drives a mock GPS route paced by speed**
  (it stops when charging) + drive-mode buttons + a **"Simulate car condition"** row: flip between
  **CITY / HIGHWAY / CHARGING / HOT DAY / LOW BATTERY / FAULT** and watch the dashboard react
  (charging icon, derate + hot warnings, low-battery chip, fault power cut).
- **TUNE** — live **sliders** for the VCU params (max torque/current, regen, throttle deadband +
  curve, ramp, creep, speed limit). **Bounded** — out-of-range values clamp; the VCU clamps again.
- **TRIPS** — **canvas graphs** (no chart library) of speed, power (negative = regen/charge),
  charge %, and motor/inverter temps. Trips are **saved to SQLite** (`app/data/trips.db`,
  gitignored) and **survive restarts** — pick a past trip from the dropdown to review it (distance,
  Wh/mi, duration), or **+ New trip** to segment, or **⤓ CSV** to download a trip's full samples.
  This is the logger that, on the real car, validates actual Wh/mi vs. the range model.
- **CAR** — the **design + handling viewer** (Three.js). The **real glTF 944** loads as a
  **ghostable shell** (toggle "Realistic body" off for the schematic with **animated pop-up
  headlights**) with the **EV components placed inside** (motor, front + main packs, transaxle,
  subs) — labeled, toggleable, ghost-opacity slider. It also computes:
  - **Balance/CG** — a yellow CG marker + live **front/rear weight split** from each part's
    `mass_kg`; toggle a component to *see* its effect, with a plain-language handling note.
  - **Drivetrain** — the kept driveline drawn (motor → **adapter** → **torque tube** → transaxle).
  - **Motor selector** — apply any motor (HyPer9 / Leaf EM57 / HiTorque / Dual EM57); the box,
    mass, and balance update, and it shows the **torque the transaxle actually takes** (capped at
    350 Nm, ADR-0004).
  - **Tires** — grip + inflation sliders compute a grip factor fed to the **GAME** (drive the
    difference). Edit **`app/frontend/ev_layout.json`** (metres, +X = front; `mass_kg` drives CG).

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
| `GET /api/params` · `POST /api/params {name,value}` | tunable params (bounded; clamps to min/max) |
| `GET /api/history` | in-memory live samples for the trip graphs |
| `GET /api/trips` · `GET /api/trip?id=N` | saved trip summaries / one trip's samples (SQLite) |
| `POST /api/trip/new` | end the current trip, start a new one |
| `GET /api/trip.csv?id=N` | download a trip's samples as CSV |
| `GET /api/route` | the mock GPS route waypoints |

## Deploy to the Pi (later)
SocketCAN (`can0`) + swap in the real CAN reader · kiosk Chromium full-screen · Pi as WiFi **AP**
(phone joins → same app) · **gpsd** for GPS · offline tile cache · 12 V→5 V + UPS for clean shutdown.
