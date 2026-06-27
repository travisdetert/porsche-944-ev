# Can a Tier-2 944 (~50 kWh, stock transaxle) actually do 150 miles?

**Short answer:** Yes — but ~50 kWh is the *floor*, not a cushion. To hit 150 miles
*reliably* (cold, highway, and after a few years of battery fade), size the pack to
**~55–58 kWh nominal (11 Tesla 5.3 kWh modules)**, not the round "50."

This conclusion is triangulated from three independent sources: two real-world data
points and a first-principles energy model. They agree within a sensible band.

---

## Data point 1 — Real 944 conversions report ~300 Wh/mi
Multiple DIY 944 EV builds cite **~300 Wh/mile for "fun but not fast" mixed driving**,
optimizable lower with gentle driving. This is the most directly relevant figure we
have: same body, same conversion class.
- Source: [Electrified Porsche 944 — Stuttcars](https://www.stuttcars.com/electrified-porsche-944-electric-classic-cars-doing-it-right/),
  [DIY Electric Car — 1986 944 Turbo EV conversion](https://www.diyelectriccar.com/threads/1986-porsche-944-turbo-ev-conversion.195065/)

## Data point 2 — A Tesla-drive 944 with 48 kWh was estimated at ~140 miles
A converted 944 on a Tesla drive unit with a **48 kWh pack was estimated at ~140 mi**.
Back-solving: 48,000 Wh ÷ 140 mi ≈ **343 Wh/mi** (and that's likely *nominal* pack, so
usable Wh/mi is a touch lower). This is the conservative end — heavier Tesla-drive
build, and an estimate rather than a logged result.
- Source: [Electrified Porsche 944 — Stuttcars](https://www.stuttcars.com/electrified-porsche-944-electric-classic-cars-doing-it-right/)

## Data point 3 — Industry envelope for context
Modern EVs run ~253 Wh/mi (efficient) to ~535 Wh/mi (heavy/inefficient); the best
*highway* numbers sit near **255 Wh/mi**. A coupe with the 944's low drag should beat
the average at speed, since aero dominates highway draw.
- Source: [EV Database — energy consumption cheatsheet](https://ev-database.org/cheatsheet/energy-consumption-electric-car),
  [InsideEVs — EPA efficiency comparison](https://insideevs.com/news/567087/bev-epa-efficiency-comparison-february2022/)

---

## First-principles check (so we're not just trusting forum numbers)

Road load at a steady **65 mph (29 m/s)**, converted 944 ≈ **1,500 kg** (~3,300 lb
after engine-out / motor + ~600 lb pack in):

| Force | Formula | Value |
|---|---|---|
| Aerodynamic drag power | ½·ρ·CdA·v³, with ρ=1.2, **CdA≈0.66 m²** (Cd 0.35 × ~1.88 m²) | ½·1.2·0.66·29³ ≈ **9.7 kW** |
| Rolling resistance power | Crr·m·g·v, Crr≈0.011 | 0.011·1500·9.81·29 ≈ **4.7 kW** |
| **Road load** | sum | **≈ 14.4 kW** |
| At the battery | ÷ ~0.88 driveline/inverter/motor eff. + ~0.3 kW accessories | **≈ 16.7 kW** |

Energy per mile at 65 mph = 16,700 W ÷ 65 mph ≈ **~257 Wh/mi steady-state highway.**

Real driving (acceleration, stops, HVAC, wind, not-perfectly-steady) lands **above**
the steady number — which is exactly why the real 944s report ~300 and the Tesla-drive
estimate implies ~343. **The physics and the forum data agree.**

---

## Putting it together — range vs. pack size

Using a **planning figure of 300 Wh/mi** (the measured 944 mixed-driving number), and
~90% usable depth-of-discharge:

| Pack (nominal) | Usable (~90%) | Range @ 300 Wh/mi | Range @ 343 Wh/mi (worst case) |
|---|---|---|---|
| 50 kWh (10 Tesla modules) | 45 kWh | **150 mi** | 131 mi |
| 55 kWh | 49.5 kWh | 165 mi | 144 mi |
| **58 kWh (11 modules)** | **52.3 kWh** | **174 mi** | **152 mi** |

**Reading the table:**
- **50 kWh** hits 150 mi *only* at the favorable 300 Wh/mi rate. On a cold highway at
  ~343 Wh/mi you'd see ~130 — and battery fade over years only makes that worse.
- **58 kWh (11 modules)** clears 150 mi even at the worst-case rate, and still holds
  ~150 after ~15% degradation. That's an honest, durable 150-mile car.

---

## Verdict & recommendation
- **150 miles is realistic for the Tier-2 (stock-transaxle) build** — this is *not*
  contradicted by the "no documented 944 does both" finding; that gap was about a
  published *blueprint*, not about physics. The energy budget closes comfortably.
- **Size to 11 Tesla 5.3 kWh modules (~58 kWh nominal)**, not 10. The extra module is
  the cheapest insurance against cold weather, highway speed, and battery aging — at
  ampREVOLT's ~$690/module that's ~$690 to turn "150 on a good day" into "150 always."
- **Confidence:** medium-high. Two of three inputs are real-world; the third is
  first-principles and lands in the same band. The remaining variance is driving style
  and climate, which the 11-module margin absorbs.

## Caveats (honest limits of this analysis)
- Data point 2 (48 kWh / 140 mi) is a single *estimate*, not a logged result.
- CdA uses Cd≈0.35 and an estimated frontal area; real 944 figures vary by year/trim.
- Converted weight is an estimate; a heavier pack/enclosure pushes Wh/mi up slightly.
- The only way to *prove* it is Phase 7's range test — log real Wh/mi and update this doc.
