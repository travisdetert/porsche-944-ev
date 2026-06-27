# 1987 Porsche 944 — Motor & Battery Layout Design

The concrete placement design for *this* car: where the EM57, the power electronics, and the
battery actually go, worked around the 944's real geometry. Same boxes serve **Stage 1**
(donor Leaf modules) and **Stage 2** (Tesla modules) — only the cells inside change.

> Dimensions below are design intent. **Measure your actual car** (the "Verify on the car"
> list) before cutting metal — body tolerances and trim vary.

---

## The 944's real spaces (and their constraints)
| Zone | What's there | Use | Constraint to respect |
|---|---|---|---|
| **Front engine bay** | held the 2.5L I4 | **Motor + all electronics + front battery box** | strut towers, steering rack, brake booster |
| **Centre tunnel** | **torque tube** runs through it | nothing — boxes flank it | the spinning driveshaft lives here; keep clear |
| **Fuel-tank bay** (ahead of rear axle, under floor) | fuel tank (removed) | **Main battery box** — prime low/central spot | floor depth vs. ground clearance |
| **Rear hatch / spare well** | cargo + spare | optional trim/expansion box | **rear torsion-bar cross-tube** sits here on the 944 |

**944-specific gotchas:**
- **Rear torsion-bar suspension:** the transverse torsion-bar tube crosses the car near the
  rear axle. The **main box sits *forward* of it** (in the fuel-tank bay) — don't try to
  cram a low box on top of it.
- **Ground clearance:** the 944 is already low. The main box drops only as far as a **skid
  plate + safe clearance** allow (see `low-cg-packaging.md`).
- **Free win:** put the **J1772 charge inlet where the fuel filler was** — reuse the fuel
  door. Cheap, clean, and period-correct in spirit.
- Relocate the **12V battery**; added rear mass may want a **torsion-bar ride-height** tweak.

---

## The design

### Motor + power electronics — front engine bay
The EM57 is compact, so it occupies only the centre-front of the bay where the engine's nose
was; everything else packs around it, **all mounted low to the subframe**.

```
  FRONT ENGINE BAY (top-down detail)
  +---------------------------------------------+
  |   [radiator / cooling up front]             |
  |   +-----------+    +-------------------+     |
  |   | FRONT BOX |    |  EM57 motor       |     |
  |   | 6 modules |    |  + inverter       |=====|===> torque tube -> transaxle
  |   | (low)     |    +-------------------+     |
  |   +-----------+    +------+ +------+ +-----+ |
  |                    |DC-DC | | PDM  | | ZVCU| |
  |                    +------+ +------+ +-----+ |
  |                    +-------------------+     |
  |                    | contactor/fuse box|     |
  |                    +-------------------+     |
  |        EM57 on centreline to the torque tube |
  +---------------------------------------------+
```
- **EM57 + inverter:** centreline, bolted via the adapter to the torque-tube bellhousing.
- **PDM (charger + DC-DC), ZombieVerter, contactor/fuse box:** around the motor, low.
- **Front battery box (6 modules):** the bay's free corner, low.

### Battery — three zones, all low

```
                       1987 PORSCHE 944 — LAYOUT (top-down)
  FRONT                                                                       REAR
  +==========================================================================+
  |  ENGINE BAY               CABIN FLOOR            FUEL-TANK BAY    HATCH    |
  |                                                  (tank removed)   /WELL    |
  |  +------------------+   ::::: torque tube :::::  +-------------+  +------+  |
  |  | EM57 + inverter  |===::: (centre tunnel) :::==|  MAIN BOX   |  | opt. |  |
  |  +------------------+                            |  8 modules  |  | trim |  |
  |  | FRONT BOX 6 mod  |                            |  (low,      |  +------+  |
  |  | DC-DC|PDM|ZVCU   |                            |   central)  |  torsion |
  |  | contactor/fuse   |                            +-------------+  bar tube |
  |  +------------------+                                              (clear) |
  |  --O---------------------------------------------------------O----------- |
  |    front axle                                           rear axle         |
  +==========================================================================+
       ~48% front                                               ~52% rear
```

| Box | Location | Modules | ~kWh (Tesla) | Why here |
|---|---|---|---|---|
| **Front box** | engine bay, beside motor | **6** | ~32 | adds weight forward (engine was heavy; motor is light) |
| **Main box** | fuel-tank bay, low/central | **8** | ~42 | the prime low spot; bulk of the mass, lowest CG |
| **Rear well** | spare-tire well | 0 | — | **subwoofer enclosure** (ADR-0010), not a battery box |
| **Total** | | **14** | **~74** | **~48% front / 52% rear** — slight rear bias, ideal RWD |

**Stage 1 (mule):** the **donor Leaf modules** reconfigure into these *same two boxes* (the
Leaf pack is modular). **Stage 2:** swap in **Tesla modules**, same boxes, same mounts.

### Side view — everything low (the CG story)
Detail in `low-cg-packaging.md`; in short: motor low in the bay, both boxes in/under the
floor between the frame rails → **CG lower than stock** despite +575 lb.

---

## Why 6 front / 8 main (not the theoretical 7/7)
`battery-pack-and-balance.md` showed 7/7 ≈ 49% front *on paper*. In the real bay, the front
also holds the inverter, PDM, ZombieVerter, and the contactor/fuse box — so **6 modules up
front is the packaging-honest number.** 6/8 lands **~48% front** — still the slight rear bias
you want for a rear-drive car, and it leaves the front bay buildable rather than crammed.

---

## Verify on the car (measure before cutting)
- [ ] Front-bay usable envelope **around the mounted EM57** (L×W×H) — confirms 6 modules + electronics fit
- [ ] **Fuel-tank bay** envelope after tank removal (L×W×H) — confirms 8 modules (single vs. double layer)
- [ ] **Clearance under the fuel-tank-bay floor** — sets how low the main box drops + skid-plate room
- [ ] **Rear torsion-bar tube** position — confirms the main box clears it
- [ ] Spare-well dimensions — if you want the optional rear trim box
- [ ] Tesla module footprint (~26"×12"×3") vs. each bay — confirms arrangement/layers

> Companion docs: `low-cg-packaging.md` (vertical/CG) · `battery-pack-and-balance.md`
> (weights + balance math) · `drivetrain-diagrams.md` (mechanical) · `drive-plan.md` (system).
