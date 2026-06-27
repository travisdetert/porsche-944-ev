# 944 EV — Battery Pack & Weight Balance (Leaf build)

The pack design and how it lands the converted 944 back on ~50/50. This is the
**committed Leaf-path build**: Nissan Leaf EM57 motor on the reused Leaf inverter,
driven by a ZombieVerter VCU, with a **14S1P Tesla pack at 319 V**.

> Masses are pressure-tested against reference figures (not live-searched this
> session). Confidence flagged. Final balance is corner-scale verified in Phase 7.

---

## Why 14S1P / 74 kWh

A Tesla 5.3 kWh module is fixed at **22.8 V nom / ~25.2 V full / ~55 lb / ~232 Ah**.
The Leaf inverter likes **~350 V**, so a long series string suits it:

- **14S1P = 14 modules = 74 kWh @ 319 V.** Near the Leaf inverter's happy voltage,
  single string (no parallel-matching), full pack HV throughout.
- Range: 74 kWh × ~0.9 usable ÷ 300 Wh/mi ≈ **222 mi** (≈194 mi at worst-case 343).
  Comfortable margin over the 150-mi target — see `range-analysis.md`.
- 16S (365 V / 85 kWh) is the max-range option (+~120 lb); 14S is the
  range/weight sweet spot.

High voltage's payoff is **low current**: EM57 ~110 kW at 319 V ≈ **~345 A peak** →
thin **2 AWG** cable, small lugs, low I²R loss.

---

## Series routing — 14S1P single string

```
   FRONT BOX                          MAIN BOX (fuel-tank bay)
   M1+→M2→M3→M4→M5→M6→M7 ──[series    ──→ M8→M9→M10→M11→M12→M13→M14−
                          link crosses
                          tunnel once]
   one continuous 14S chain = 319 V, 232 Ah
        │
        └─ [MSD] → [main fuse] → [precharge + main contactors] → Leaf inverter
   BMS taps all 14 module junctions; full HV throughout — strict isolation discipline.
```

No parallel junction (single string), so no string-matching — but every connection is
at full pack voltage. The one series link between the front and main boxes routes
through the tunnel alongside the torque tube.

---

## Placement map (numbered — 7 front / 7 main)

```
        FRONT AXLE                                          REAR AXLE
            │                                                   │
   ┌────────┼───────────────────────────────────────────────────┼────────┐
   │ DC-DC, │  [== EM57 ==]   ┌───────────────┐  ░tube░ ┌───────────────┐  │
   │ charger│   +inverter     │ FRONT BOX     │        │ MAIN BOX       │  │
   │ ZVerter│   +adapter      │ M1 M2 M3 M4   │        │ M8  M9 M10 M11 │  │
   │ nose   │                 │ M5 M6 M7      │        │ M12 M13 M14    │  │
   │ ───────┼─────────────────┴───────────────┴────────┴───────────────┴──┤
   │        │            all modules LOW in floor          stock transaxle │
   └────────┼───────────────────────────────────────────────────┼────────┘
        ~49% front                                          ~51% rear
```

---

## Balance worksheet

**"%-to-front" by zone** (fraction of an item's weight carried by the front axle):
front bay ~65% · nose/cooling ~80% · fuel-tank bay ~30% · hatch/spare well ~5%.

| Change | Mass (lb) | Confidence | %F | ΔFront | ΔRear |
|---|---|---|---|---|---|
| **Stock 944** (1987, 2.5L), ~50/50 | 2,900 | high | — | 1,450 | 1,450 |
| − Engine+clutch+flywheel+manifold+starter | −400 | med (≈150 kg dressed) | 65% | −260 | −140 |
| − Cooling/radiator/coolant | −40 | med | 80% | −32 | −8 |
| − Fuel tank + lines + ½ fuel | −75 | med | 30% | −22 | −53 |
| − Exhaust + cats (rear) | −45 | med | 35% | −16 | −29 |
| + EM57 motor (~100) + Leaf inverter (~30) + adapter (~45) | +175 | med | 65% | +114 | +61 |
| + Power electronics (ZombieVerter, DC-DC, contactors, charger) | +80 | med | 65% | +52 | +28 |
| **Subtotal before battery** | **2,595** | — | **49.5%F** | **1,286** | **1,309** |
| + Battery: 14 modules (770 lb cells) + enclosures/BMS (~110) | +880 | high (module 55 lb ×14) | split → | | |
| &nbsp;&nbsp;• 7 in front box (440 lb @65%F) | | | | +286 | +154 |
| &nbsp;&nbsp;• 7 in main box (440 lb @30%F) | | | | +132 | +308 |
| **Final — converted 944 (Leaf)** | **3,475** | — | **49.0%F** | **1,704** | **1,771** |

**Result: ~3,475 lb (+575 over stock), 49.0 / 51.0 front/rear** — essentially 50/50
with a whisker of rear bias (ideal for RWD traction), and a **lower CG than stock**
(mass in the floor, not in a tall iron engine).

### Balance trim (same 14 modules)
| Split (front / main) | Front % | Note |
|---|---|---|
| **7 / 7** | **49.0%** | recommended — even, easy routing |
| 8 / 6 | ~49.8% | true-ish 50/50 |
| 6 / 8 | ~47–48% | more rear bias; **the packaging-realistic choice** |

> **In-car design = 6 front / 8 main (~48% front).** The front bay also holds the inverter,
> PDM, VCU, and contactor/fuse box, so 6 modules up front is the *buildable* number (vs. the
> theoretical 7/7). Concrete placement: `944-layout-design.md`.

---

## Mounting & CG notes
- **Lowest CG wins** — mount every box as low as the floor/bellypan allows; CG height
  matters more for feel than the exact front/rear split.
- **Front box** ties into the engine-mount crossmember / front subframe hardpoints —
  not sheetmetal.
- **Main box (fuel-tank bay)** is the prime low-central real estate where the tank was;
  frame it into the floor/tunnel structure.
- Steel/aluminum enclosures, sealed & vented; HV isolated from chassis; **MSD reachable**.
- Net +575 lb → uprated springs/dampers + brakes sized for the weight (in the budget).

## Verify later
- **944 engine dressed weight (~400 lb)** is the softest input — confirm by weighing on
  removal (Phase 1); it swings the pre-battery balance most.
- Tesla module **55 lb** and EM57 mass are reference figures (med–high confidence).
- **Validate the Leaf inverter runs happily at 319 V with ZombieVerter** at your target
  power before committing all 14 modules.
- Corner-scale the finished car (Phase 7); move 1–2 modules front↔main to trim.
