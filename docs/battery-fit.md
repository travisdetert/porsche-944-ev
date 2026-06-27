# Battery Fit — can enough battery physically fit a 944 to drive?

The make-or-break feasibility question: with the rear well now given to the subs (ADR-0010),
do enough cells **physically fit** the 944's two remaining bays to support real driving?

## Short answer: yes — comfortably
- **Minimum to drive** is tiny and fits trivially (a handful of modules → ~50 mi).
- **The full 74 kWh plan fits** across the two boxes (front bay + fuel-tank bay).
- **The rear-well → subs choice costs zero driving range** — the well was only ever *optional
  expansion beyond_ the 74 kWh, which already lives in the two main boxes.
- **One real catch:** Tesla's long 26" bricks are awkward in the compact fuel-tank bay. The
  small Leaf modules (Stage 1) sidestep it entirely.

> Dimensions below are **design estimates — confirm on the car** (these come straight out of
> teardown). The *conclusion* (it fits, it drives) is robust; the exact counts need a tape measure.

## The two available volumes
| Bay | Approx usable (verify on car) | Shares with |
|---|---|---|
| **Front engine bay** (freed corner) | ~30" × 20" × 12" | motor + inverter + DC-DC + VCU + contactors |
| **Fuel-tank bay** (tank removed, low/central) | ~24" × 22" × 10" | nothing — the prime battery spot |
| ~~Rear spare-well~~ | — | **subwoofer** (ADR-0010) |

## Module dimensions
| Module | Size (≈) | Weight | Energy |
|---|---|---|---|
| **Tesla 5.3 kWh** (Stage 2) | **26" × 12" × 3"** | 55 lb | 5.3 kWh |
| **Leaf module** (Stage 1, donor) | **12" × 8" × 1.4"** | 8.5 lb | ~0.5 kWh |

## Fit per bay (the math)
**Stage 2 — Tesla bricks (the tight case):**
- **Front bay** (~30"×20"): a 26" module lies along the 30" dimension easily — **~6 modules**
  in two stacked layers fit beside the motor.
- **Fuel-tank bay** (~24"×22"): here's the catch — a **26" module is longer than either side.**
  Options: lay them **diagonally** (the bay's diagonal ≈ 32" > 26"), stand them **on edge**, or
  confirm the bay is actually longer once the tank's out. Two layers → **~8 modules**.
- **Total ≈ 14 modules / 74 kWh** across the two boxes → ~222 mi. *Tesla orientation in the
  fuel-tank bay is the one thing to verify carefully.*

**Stage 1 — Leaf modules (the easy case):**
- At 12"×8"×1.4" and ~0.5 kWh each, Leaf modules **fit almost any orientation** and reconfigure
  freely into both bays. A 24–40 kWh donor pack drops in with room to spare → ~50–100 mi.
- **This is a real Stage-1 advantage:** the small modules make "does it fit?" a non-issue while
  you prove the build.

## What that supports — "any driving"
| Pack | Modules | Fits? | Range | Use |
|---|---|---|---|---|
| Minimum-to-move | 3–4 Tesla | trivially (one bay) | ~50–70 mi | proof it drives |
| **Stage-1 donor Leaf** | small, ~24–40 kWh | **easily** | ~50–100 mi | **the mule — any local driving** |
| Stage-2 full | 14 Tesla, 74 kWh | yes (two boxes, orient care) | ~222 mi | road trips |

**"Any driving" is never the binding constraint.** Even the minimum fits with room to spare;
the question was only *how much* range, and the two boxes hold enough for ~222 mi.

## The honest catch + the fix
The **26" Tesla module length vs. the compact fuel-tank bay** is the only real fit risk. Fixes,
in order of preference: (1) confirm the bay length on the car — it may take them flat; (2)
mount modules **on edge**; (3) **diagonal** layout; (4) shift one module to the front bay.
**Stage 1's Leaf modules dodge this completely** — another reason the mule comes first.

## Verify on the car (the few measurements that settle it)
- [ ] Fuel-tank bay clear **length** (after tank removal) vs. the 26" Tesla module
- [ ] Fuel-tank bay **depth** → single vs. double module layer (and ground clearance, `low-cg-packaging.md`)
- [ ] Front-bay clear envelope **around the mounted motor**
- [ ] Donor Leaf module/stack dimensions (Stage 1) vs. both bays

## Conclusion
**Batteries fit to support real driving in a standard 944 — Stage 1 trivially, Stage 2 with a
bit of Tesla-orientation care.** Giving the rear well to the subs cost nothing, because the
full pack already lives in the two main boxes. The only homework is a tape measure during
teardown.

> Placement design: `944-layout-design.md` · Low/CG: `low-cg-packaging.md` ·
> Balance: `battery-pack-and-balance.md`.
