# Can a Tier-2 944 (~50 kWh, stock transaxle) actually do 150 miles?

**Short answer:** Yes, comfortably. The committed **Leaf-path pack is 74 kWh (14 Tesla
modules)** → **~222 mi** at the realistic 300 Wh/mi, and **~194 mi** even at worst-case
343 Wh/mi. That's 45–70 mi of margin over the 150-mi target — enough to absorb cold,
highway speed, and years of battery fade. (The high-voltage Leaf inverter wants a long
series string, which is *why* the pack is this big — range margin is a happy side effect.)

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

Road load at a steady **65 mph (29 m/s)**, converted 944 ≈ **1,575 kg** (~3,475 lb
after engine-out / EM57 + 880 lb pack in — aero dominates at speed, so the exact mass
barely moves the highway number):

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
| 50 kWh (10 Tesla modules) | 45 kWh | 150 mi | 131 mi |
| 58 kWh (11 modules) | 52.3 kWh | 174 mi | 152 mi |
| **74 kWh (14 modules — this build)** | **66.6 kWh** | **222 mi** | **194 mi** |

**Reading the table:**
- A 50 kWh pack hits 150 mi *only* at the favorable 300 Wh/mi rate, and battery fade
  erodes that. It would be the floor, not a cushion.
- **The committed 74 kWh build clears 150 mi at every rate**, holds ~150 even after
  heavy degradation, and leaves real margin for cold and highway speed. The big pack
  isn't over-building for range — it's what the 319 V Leaf inverter wants electrically.

---

## Verdict & recommendation
- **150 miles is comfortably met by the committed 74 kWh Leaf build** (~222 mi typical,
  ~194 worst-case). The "no documented 944 keeps the transaxle *and* does 150 mi" finding
  was a *blueprint* gap, not a physics one — the energy budget closes with room to spare.
- **The pack size is driven by electrics, not range padding:** the Leaf inverter wants
  ~319 V, i.e. a 14-module series string, which happens to deliver ~70 mi of margin.
- **Confidence:** medium-high. Two of three inputs are real-world; the third is
  first-principles and lands in the same band. Driving style and climate are the only
  real variables, and the margin absorbs them.

## Caveats (honest limits of this analysis)
- Data point 2 (48 kWh / 140 mi) is a single *estimate*, not a logged result.
- CdA uses Cd≈0.35 and an estimated frontal area; real 944 figures vary by year/trim.
- Converted weight is an estimate; a heavier pack/enclosure pushes Wh/mi up slightly.
- The only way to *prove* it is Phase 7's range test — log real Wh/mi and update this doc.
