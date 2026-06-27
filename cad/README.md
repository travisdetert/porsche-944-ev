# Custom Parts — design process

Most of the 944 EV is reused (Leaf) or kept (944). These are the few parts we **make**.

## The custom parts
| Part | Type | Precision | How | Gate |
|---|---|---|---|---|
| **Adapter plate** | machined | **HIGH (concentric)** | parametric CAD → DXF/STEP → machine shop | G2 |
| **Coupler / hub** | machined | HIGH | source (EV Coupler Connection) **or** machine | G2 |
| Battery enclosures ×2 | sheet / weldment | low–med | cardboard template → sheet metal | G4 |
| Motor mounts | weldment | med | template off the car → weld | G3 |
| Skid plate | sheet | low | template → bend/laser | G4 |

## Workflow (every custom part)
1. **Measure** the mating hardware (teardown / donor extraction).
2. **Model** it parametrically — fill the measured values into the model.
3. **Fit-check cheaply** — cardboard / plywood mock, or a 3D-printed PLA proxy.
4. **Export** a DXF (2D profile) or STEP + a dimensioned drawing for the shop / your bender.
5. **Make it**, then **dry-fit** — that's the gate (adapter = G2).

## Toolchain (cheap + repo-friendly)
- **OpenSCAD** — free, text-based, parametric, version-controlled. Used here for the round
  precision parts. Edit the measured variables → render → export DXF/STL.
- **FreeCAD** / **Fusion 360 (free hobby)** — GUI option for organic/complex parts.
- **Cardboard + marker** — the honest first prototype for enclosures and mounts.

## Files
- `adapter-plate.scad` + `adapter-spec.md` — EM57 → torque-tube adapter (the critical part).
- enclosures / mounts / skid: specs added when we design them.

## Using the .scad models
Install OpenSCAD → open the file → replace every `// MEASURE` placeholder with your real
number → **F5** preview, **F6** render → **File ▸ Export ▸ DXF** (2D) or **STL**. Send the DXF +
the matching `*-spec.md` to the machine shop.
