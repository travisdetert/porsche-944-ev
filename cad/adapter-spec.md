# Adapter Plate + Coupler — design spec

The one precision custom part. It bolts the **EM57 motor** to the **944 torque-tube
bellhousing** and locates the shafts **concentric**. Model: `adapter-plate.scad`.

## Two parts, two jobs
1. **Adapter plate** — bolts motor face ↔ bellhousing flange; centers both via register fits.
2. **Coupler / hub** — joins the EM57 output to the driveshaft (torque transfer). Often best
   **sourced** (EV Coupler Connection) rather than machined from scratch — the EM57 output is
   an integrated reduction-gear interface, not a plain shaft.

## Measurements to take → fill into the .scad
| Variable | What / where | Tool | Value |
|---|---|---|---|
| `motor_bc` / `motor_bolts` / `motor_bolt_d` | EM57 face bolt circle, count, hole | calipers, bolt gauge | ___ |
| `motor_reg_d` / `motor_reg_depth` | EM57 spigot/register (centers motor) | calipers, depth gauge | ___ |
| `bell_bc` / `bell_bolts` / `bell_bolt_d` | torque-tube bellhousing bolt circle, count, hole | calipers | ___ |
| `bell_reg_d` | bellhousing register dia (0 if none) | calipers | ___ |
| `bore_d` | central clearance for coupler/pilot | calipers | ___ |
| `plate_OD` / `plate_t` | outer dia / thickness (choose) | — | ___ |
| **Working length** | motor-face → flange gap (sets plate + coupler stack) | depth gauge | ___ |

## Material & tolerances
- **Material:** 6061-T6 aluminum (light, ADR-0011) **or** steel if torque margin demands.
- **Thickness:** ~12–20 mm — stiff enough to not flex under motor torque.
- **Register fits:** machine the centering diameters to a **slip/locating fit** (≈ H7/h6) — this
  is what guarantees concentricity. **This is the make-or-break dimension.**
- **Flatness / parallelism** of the two faces: tight — a wedge = driveline vibration.
- **Bore concentric** to the registers within ~0.05 mm.

## Fit-check before machining metal
- Laser/print the **2D hole pattern on paper or 3 mm acrylic**, lay it on both faces — confirms
  bolt circles + bore before spending on billet.
- Or 3D-print a **PLA proxy** of the full plate for a physical dry-fit on the bench.

## Deliverable to the machine shop
- **DXF** (2D profile + holes) exported from the .scad, **+ this spec** (material, thickness,
  register fits, flatness callouts), **+ a dimensioned PDF** drawing.
- Or a **STEP** solid if the shop prefers 3D.

## Verification (Gate G2)
The machined plate + coupler **dry-fit cleanly to both** the EM57 and the bellhousing, shafts
concentric, no bind by hand. → step `009`, then mount at step `010` (G3).
