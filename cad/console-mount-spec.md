# Console Touchscreen Mount + Bezel — design spec

Mounts the **Raspberry Pi head-unit touchscreen** (the app in `../app/`) into the **944
center stack** where the factory radio / cassette + pocket live. Preview: `console-mount.svg`.

## What it must do
- **Drop into the factory center-stack aperture** — reuse the existing radio opening + the
  cubby above it; **keep the HVAC slider controls below** fully usable.
- Hold a **~7" capacitive touchscreen** flush, at a glance-friendly angle, glare-managed.
- Carry the **Pi + screen driver board** behind it with airflow (it gets warm), and route
  **12 V→5 V** power + the CAN/USB lead cleanly.
- Be **removable** (service the Pi) and not rattle — this is interior trim, NVH matters.

## Measure (→ the model)
- Center-stack **aperture** W×H (the radio + pocket opening) and depth behind it to the tunnel.
- Stock radio is ~**DIN width (≈178 mm)**; the 944 opening is a touch wider with the trim — verify.
- Chosen screen's **active area + bezel** and board stack depth.
- Clearance to the **HVAC controls** and the shifter surround.

## Material & build
- **Matte panel** (3D-printed or CNC) — laser/CNC ABS/aluminum bezel + a printed rear cage for the Pi.
- Anti-glare: matte finish + slight downward tilt; recess so the screen isn't proud of the trim.
- Bond/screw to the stock radio cage tabs — **never load the dash plastic** in a way that cracks it.

## Prove-out (acceptance)
1. Cardboard/printed mockup drops into the aperture; HVAC controls still reachable.
2. Screen sits flush + readable in daylight (matte, angle OK).
3. Pi behind stays < ~70 °C in a hot cabin (airflow / vent).
4. One-handed removable for service; no rattles over road input.

## Routes (pick one)
- **A — Bezel in the radio slot (cleanest):** screen replaces the radio; pocket above becomes vent/cable run.
- **B — Full center-stack panel:** one custom panel from cubby to HVAC, screen + a few hard buttons.

> The app is non-safety (ADR-0014) — a screen crash never affects drivability. Keep the VCU/BMS
> on their own harness; the Pi only taps the CAN bus read-only + bounded writes.
