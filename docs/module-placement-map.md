# 944 EV — Module Placement Map & Voltage-String Routing

This turns the balance layout into a **concrete electrical + physical plan**: how many
Tesla modules, wired in what series/parallel arrangement, in which box. The new
constraint that drives everything: **the controller's voltage window sets the series
count**, which sets total energy, which sets weight and balance.

> Masses below are **pressure-tested against reference figures** (not live-searched this
> session — you're at the search limit). Confidence flagged per row.

---

## The coupling: system voltage decides module count

A Tesla 5.3 kWh module is **6S internally → 22.8 V nominal, ~25.2 V full, ~55 lb,
~232 Ah**. Series count is capped by your controller:

| Controller (drive path) | DC voltage window | Max modules **in series** | kWh per series string |
|---|---|---|---|
| **HyPer9 std + SME AC-X1** (Path B) | ~96–132 V | **5S** (114 V nom / 126 V full) | 26.5 kWh |
| HyPer9 **HV** + AC-X144 | up to ~180 V | 7S (160 V) | 37 kWh |
| **Leaf inverter + ZombieVerter** (Path A) | ~250–400 V (likes ~350 V) | 14–16S | 74–85 kWh |

**Implication:** Path B (recommended) wants a **low-voltage, parallel** pack; Path A
(Leaf) wants a **high-voltage, long-series** pack — which naturally pushes Path A to
more modules (more range, but more weight + cost). This is why the two paths land on
different pack sizes.

---

## Recommended config — Path B: **10 modules, 5S2P, 53 kWh, 114 V**

Two parallel strings of five series modules. 53 kWh nominal → ~47.7 kWh usable →
**~159 mi @ 300 Wh/mi** — clears the 150-mi target with margin. Clean because **each
string drops into one box**, so wiring and balance align:

```
   STRING A (front box)            STRING B (main box, fuel-tank bay)
   M1+→M2→M3→M4→M5−                M6+→M7→M8→M9→M10−
     │   5S = 114V                   │   5S = 114V
     └────[string fuse]──┐   ┌───[string fuse]────┘
                         ▼   ▼
                    HV JUNCTION (parallel)  ── 2P, 114V, ~106 Ah×2 = 232 Ah
                         │
                  [MSD] [main fuse] [precharge+main contactors]
                         │
                         ▼  to HyPer9 X1 controller
```

### Physical placement (numbered)
```
        FRONT AXLE                                          REAR AXLE
            │                                                   │
   ┌────────┼───────────────────────────────────────────────────┼────────┐
   │ DC-DC, │  [== MOTOR ==]  ┌─────────────┐   ░tube░  ┌─────────────┐    │
   │ charger│   +adapter      │ FRONT BOX   │          │ MAIN BOX     │    │
   │ contact│                 │ M1 M2 M3    │          │ M6  M7  M8   │    │
   │ nose   │                 │ M4 M5       │          │ M9  M10      │    │
   │ ───────┼─────────────────┴─(String A)──┴──────────┴─(String B)──┴────┤
   │        │              all modules LOW in floor       stock transaxle │
   └────────┼───────────────────────────────────────────────────┼────────┘
        ~49% front                                          ~51% rear
```

---

## Pressure-tested mass table & recomputed balance

| Change | Mass (lb) | Confidence | %F | ΔFront | ΔRear |
|---|---|---|---|---|---|
| **Stock 944** (1987, 2.5L) | 2,900 @ ~50/50 | high (well-documented) | — | 1,450 | 1,450 |
| − Engine+clutch+flywheel+manifold+starter | −400 | med (≈150 kg dressed) | 65% | −260 | −140 |
| − Cooling/radiator/coolant | −40 | med | 80% | −32 | −8 |
| − Fuel tank + lines + ½ fuel | −75 | med | 30% | −22 | −53 |
| − Exhaust + cats (rear) | −45 | med | 35% | −16 | −29 |
| + Motor (HyPer9 ~150) + adapter (~40) | +190 | high (mfr 68 kg) | 65% | +124 | +66 |
| + Power electronics (ctrl/DC-DC/contactors/charger) | +95 | med | 65% | +62 | +33 |
| **Subtotal before battery** | **2,625** | — | **49.8%F** | **1,306** | **1,319** |
| + Battery: 10 modules (550 lb cells) + enclosures/BMS (~80) | +630 | high (module 55 lb ×10) | split → | | |
| &nbsp;&nbsp;• 5 in front box (315 lb @65%F) | | | | +205 | +110 |
| &nbsp;&nbsp;• 5 in main box (315 lb @30%F) | | | | +95 | +221 |
| **Final — converted 944** | **3,255** | — | **49.3%F** | **1,605** | **1,650** |

**Result: ~3,255 lb (+355 over stock), 49.3 / 50.7 front/rear** — essentially 50/50
with a whisker of rear bias (ideal for RWD traction), and a **lower CG than stock**
(mass in the floor, not in a tall iron engine).

### Balance trim options (same 10 modules)
| Split (front / main) | Wiring | Front % | Note |
|---|---|---|---|
| **5 / 5** | clean (1 string per box) | **49.3%** | **recommended** — strings stay intact |
| 6 / 4 | one module crosses strings | ~50.0% | true 50/50, slightly messier BMS/wiring |
| 4 / 6 (+1 in hatch well) | — | ~47–48% | more rear bias for launch traction |

---

## Cabling & current (the low-voltage tradeoff of Path B)
- 114 V × ~90 kW peak (HyPer9) → **~790 A peak**. Plan **2/0–4/0 welding cable**,
  proper lugs, and a contactor/fuse rated for it. Low voltage = high current = fat,
  short cable runs and careful lug crimps.
- 2P means **string fuses on each parallel string** (not just one pack fuse) so a fault
  in one string can't be back-fed by the other.
- Keep the two strings **capacity-matched** (same module health) before paralleling.

## If you go Path A (Leaf) instead
- To use the Leaf inverter well, target **~14S** (≈319 V): **14 modules = 74 kWh**,
  ~770 lb of cells. More range (~220 mi) but ~220 lb heavier and ~$2.8k more in modules.
- Higher voltage = **lower current** (~230 A for the same power) = thinner cable, but a
  bigger/heavier/pricier pack. Re-run the balance worksheet with the 14-module mass and
  expect to bias more modules toward the rear/main box.

## Open / verify later
- **944 engine dressed weight (~400 lb)** is the softest input — confirm by weighing on
  removal (Phase 1). It swings the "before-battery" balance most.
- Tesla module **55 lb** and HyPer9 **150 lb** are manufacturer/reference figures, high
  confidence.
- Final balance is **corner-scale verified in Phase 7**; move 1–2 modules to trim.
