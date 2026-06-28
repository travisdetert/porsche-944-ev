# Motor Mounts — design spec

Brackets tying the **EM57 to the 944's factory crossmember hardpoints** — locating the motor
and **reacting its torque**. Model: `motor-mount.scad` · preview: `motor-mount.svg` · Gate **G3**.

## What they must do
- Hold the EM57 at the **right height/position** for the adapter + driveline (set by step 010).
- **React motor torque** (and the transaxle's reaction) — triangulated, stiff, fatigue-safe.
- **Isolate NVH** (motor/gear whine) via rubber/poly bushings — firm enough to still locate.
- Bolt to **factory crossmember hardpoints, never sheetmetal.**

## Measure (→ the .scad)
- EM57 mounting-boss positions + bolt pattern.
- 944 crossmember hardpoint locations.
- The **gap/offset** between them (sets base depth + upright height).

## Material & build
- **Steel weldment** (strength for torque reaction) — laser/plasma the plates, then weld.
- **Gussets** at the base↔upright joint (not in the simple model) — this joint carries the load.
- **Poly/rubber isolators** in the base pocket (`iso_bore_d`); choose durometer for NVH vs. precision.
- Make **2–3 mounts** spaced to triangulate against torque.

## Fit-check (no 3D printer)
- **Cardboard/plywood template off the car**; tack-weld and check fit + driveline alignment
  **before** final welding.

## Deliverable
- DXF of the plates (from the .scad faces) for laser/plasma; weld per the template.

## Verification (Gate G3)
Motor mounted, **driveline turns true by hand**, no bind, mounts solid under hand-load. → step `010`.

> Mounts to the kept crossmember (ADR-0004); keep mass low (ADR-0011).
