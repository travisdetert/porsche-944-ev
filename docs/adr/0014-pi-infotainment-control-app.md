# ADR-0014: Custom Pi infotainment + telemetry app (web/PWA), outside the safety loop

**Status:** Accepted
**Date:** 2026-06-27
**Deciders:** Travis

## Context
We want a touchscreen head unit: **monitor the drivetrain, switch drive modes, tune params**,
**plus infotainment** — **maps/navigation and phone connectivity**. The ZombieVerter exposes
tunable params + telemetry on CAN. This must add capability **without** touching safety.

## Decision
Build a **Raspberry-Pi head unit** running a **custom local web app (PWA)** that the **Pi
touchscreen and any phone on the car's WiFi both run.** It provides telemetry, **drive-mode
presets**, bounded tuning, **maps (offline OSM tiles + a gpsd GPS)**, and **phone integration
(Pi WiFi AP + Bluetooth audio + hotspot tethering)**. It reads the openinverter CAN for telemetry
and writes **only bounded** parameter presets. **Strictly outside the safety loop** — the VCU +
BMS retain all hard limits, interlocks, and contactor control.

## Alternatives considered
- **ZombieVerter WiFi web UI only** — rejected: a config page, not a driving/infotainment head unit.
- **Commercial Android-Auto head unit / OpenAuto only** — rejected: no custom EV telemetry or
  drive-mode integration; not ours. (Kept as an optional projection mode.)
- **Put control logic on the Pi** — rejected: a non-safety-rated computer must never be in the
  safety path.

## Consequences
- **Positive:** one web codebase = touchscreen **and** phone; maps + media + telemetry + drive
  modes + **trip logging that validates the range model**; fully custom.
- **Negative / accepted cost:** a software project to build/maintain (~$150–300 hardware); must
  enforce the **safety boundary**, **bounded writes**, **graceful power/shutdown**, and stay
  **offline** (attack surface on the drivetrain CAN).
- **Follow-ups:** dev scaffold in **`app/`** (mock CAN now → SocketCAN on the Pi); offline tile
  cache; gpsd; kiosk + WiFi-AP setup. See `docs/control-computer.md`.
