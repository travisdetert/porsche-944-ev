# Battery Enclosures — design spec

Two boxes, same design, different size: **FRONT box (6 modules)** in the engine bay and
**MAIN box (8 modules)** in the fuel-tank bay. Model: `battery-enclosure.scad` (set the
module grid; it echoes internal/external dims and a bay-fit check).

## Fit is the first constraint
- **Size to the measured bays.** Put your bay L×W×H into the `.scad` (`bay_*`) — it flags if
  the external box exceeds the bay. Source: `../docs/battery-fit.md`.
- **The 26″ (685 mm) Tesla module is the tight dimension** in the 944. If a box won't fit flat,
  options in the model: change `modules_x/y` orientation, mount modules **on edge** (swap
  `mod_W`/`mod_H`), or use **2 layers** (`layers=2`) — watch ground clearance.
- Stage-1 **Leaf modules are small** — set `mod_*` to the Leaf module and they fit easily.

## Material & build
- **3 mm aluminum** (light, per ADR-0011), welded — or folded + riveted with sealed seams.
- **Mounting flanges bolt to frame rails / floor hardpoints — never sheetmetal** (crash load).
- Mass kept **low** (`../docs/low-cg-packaging.md`); add a **skid plate** under the main box.

## Inside the box
- **Module retention:** foam/spacers + a clamping bar so nothing shifts in a crash.
- **Isolation:** insulating liner between cells and the metal box; **HV isolated from chassis**.
- **Busbars/wiring:** the model adds ~20 mm headroom; bring HV out through a **sealed gland**.
- **Keep the MSD reachable.**

## Sealing & venting
- **Sealed, gasketed lid** + low **vent ports to outside** (off-gas path) — the model stubs 2
  per long side. Don't seal it airtight with no vent path.

## Fit-check (no 3D printer)
- Build a **cardboard box at the echoed EXTERNAL dimensions**, set it in the bay, and confirm
  clearance, lid access, and cable exit **before cutting aluminum.**

## Deliverable
- From the `.scad` external dims, make a **cut list** (panel sizes) + bend lines, or a **DXF
  flat pattern**, for a sheet shop / laser+brake. Hand over this spec with it.

## Verification (Gate G4)
Boxes mounted low to structure, modules retained, **isolation (megger) passes**, lid sealed,
vents clear. → step `011`.
