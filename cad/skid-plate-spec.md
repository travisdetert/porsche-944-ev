# Skid Plate — design spec

Protects the **low main battery box** from road strikes. The pack sits as low as ground
clearance allows (ADR-0005/0011), so a sacrificial plate under it is mandatory. Model:
`skid-plate.scad` · preview: `skid-plate.svg` · Gate **G4**.

## What it must do
- **Take a road strike** without the pack feeling it — deflect/absorb, then be **replaceable.**
- Cover the **main box footprint + margin**; **turned-up lip** to deflect (not catch) obstacles.
- Set the practical **ground clearance / breakover** — the box drops only as low as this allows.

## Measure (→ the .scad)
- Main box footprint (from `battery-enclosure.scad`) + margin → `plate_L` / `plate_W`.
- Mounting points on the frame rails / box.
- Available clearance under the bay (`../docs/low-cg-packaging.md`, `battery-fit.md`).

## Material & build
- **Steel 3–5 mm** (best strike resistance) under the pack — or thick aluminum to save weight
  (lighter, ADR-0011, but less tough). Steel is the safer call directly under cells.
- **Lip** brake-bent up around the edge.
- **Bolt to frame rails / box mounts** (sacrificial — meant to take hits and be swapped).

## Fit-check (no 3D printer)
- Print `skid-plate.svg` 1:1 as a template; or cardboard mock — confirm coverage + clearance
  + breakover before cutting steel.

## Deliverable
- **DXF flat** from the .scad → laser/waterjet, then brake the lip.

## Verification (Gate G4)
Plate fits under the mounted main box, covers it with margin, clears the ground acceptably,
bolts solid. → step `011`.
