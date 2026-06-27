# 944 EV — Structural Layout & Weight Balance

The 944's stock ~50/50 balance (front engine, **rear transaxle**) is the asset we're
protecting. This lays out the motor and battery modules as a **balance budget**: every
part we remove or add is a weight at a position, and the module split is the *output*
that lands the converted car back on ~50/50 (or a deliberate slight rear bias for RWD
traction).

> All masses and the "%-to-front" lever fractions are **planning estimates**. The real
> number comes from corner-balancing on scales after the build (Phase 7). This is the
> design target to aim at.

---

## Stock baseline
- Curb weight ≈ **2,900 lb**, distribution ≈ **50 / 50** → **1,450 lb front / 1,450 lb rear**.
- Wheelbase ≈ 2,400 mm. Engine sits *front-mid* (behind the front axle) — that's why
  it balances. Transaxle + diff at the rear is the counterweight.

## "%-to-front" by zone (lever-arm estimate)
How much of an item's weight the **front axle** carries, by where it sits:

| Zone | Location | % to front axle |
|---|---|---|
| **Front bay** | engine/motor area, behind front axle | ~65% |
| **Cooling/nose** | ahead of front axle | ~80% |
| **Fuel-tank bay** | low, just ahead of rear axle | ~30% |
| **Hatch / spare well** | behind rear axle | ~5% |

---

## Balance worksheet

**Remove (ICE bits):**
| Item | Weight | Zone (%F) | ΔFront | ΔRear |
|---|---|---|---|---|
| Engine + clutch + flywheel + manifold | −420 | 65% | −273 | −147 |
| Cooling / radiator / ICE misc | −40 | 80% | −32 | −8 |
| Fuel tank + lines + ½ fuel | −75 | 30% | −22 | −53 |
| Exhaust + cats (rear runs) | −45 | 35% | −16 | −29 |

**Add (EV drive, non-battery):**
| Item | Weight | Zone (%F) | ΔFront | ΔRear |
|---|---|---|---|---|
| Motor + adapter plate | +190 | 65% | +124 | +66 |
| Power electronics (controller, DC-DC, contactors, charger) | +95 | 65% | +62 | +33 |

**Subtotal before battery:** **≈ 1,292 lb front / 1,313 lb rear** (2,605 lb, **49.6% front**).

> Key insight: pulling the heavy front engine and replacing it with a lighter
> motor + electronics leaves the car **slightly rear-biased and ~300 lb lighter
> before any battery**. So the battery is what we use to *add weight back toward the
> front* and dial the final balance — the opposite of the usual "stuff the pack in
> the back" instinct.

---

## Battery layout = the balancing lever (~700 lb, 11–12 Tesla modules)

Target pack ≈ **58 kWh ≈ 11 modules** (~627 lb cells) + enclosures/BMS ≈ **~700 lb total**.
Two design targets:

### Option A — true 50/50 (sharpest handling)
Battery CG must carry ~51% on the front axle → **front-bias the pack**:
| Box | Weight | ≈ modules |
|---|---|---|
| Front bay (around/beside motor) | ~420 lb | ~7 |
| Fuel-tank bay (low, central) | ~280 lb | ~5 |
| Hatch/spare well | 0 | 0 |

→ **≈ 1,649 / 1,656 lb = ~49.9% front. Bang on 50/50.** Tight packaging up front
(motor shares the bay), but the purest balance.

### Option B — ~47/53 rear bias (better RWD traction, easier packaging)
Shift mass low-and-central/rear:
| Box | Weight | ≈ modules |
|---|---|---|
| Front bay | ~200 lb | ~3–4 |
| Fuel-tank bay (low, central) | ~400 lb | ~7 |
| Hatch/spare well | ~100 lb | ~2 |

→ **≈ 47% front / 53% rear.** Slight rear bias aids rear-drive traction and launch,
keeps the heavy boxes low and central (best for CG height), and is far easier to fit.
**Recommended default** unless you're chasing track balance.

---

## Structural layout (side view, with axles & balance)

```
        FRONT AXLE                                          REAR AXLE
            │                                                   │
   ┌────────┼───────────────────────────────────────────────────┼────────┐
   │ COOL/  │  ┌─────────┐   ┌──────────┐                ┌──────────┐  ┌──┐│
   │ charger│  │ E-MOTOR │   │ FRONT    │  ░░ torque ░░  │  MAIN    │  │HW││
   │ nose   │  │ +adapter│   │ BATT BOX │  ░░  tube  ░░  │ BATT BOX │  │well
   │        │  │ +power  │   │ (low)    │                │ (low,    │  │mods
   │        │  │ elec    │   │          │                │ central) │  │  ││
   │ ───────┼──┴─────────┴───┴──────────┴────────────────┴──────────┴──┴──┤
   │        │         keep all boxes LOW = low CG          stock transaxle │
   └────────┼───────────────────────────────────────────────────┼────────┘
            │                                                   │
        ~47–50% front                                      ~50–53% rear
```

```
                        ── TOP-DOWN (module distribution) ──
   ┌───────────────────────────────────────────────────────────────────────┐
   │  [nose: DC-DC,      ┌──────────────┐   ┌──────────────┐                 │
   │   charger,    [== MOTOR ==]        │   │              │                 │
   │   contactors] │ FRONT BOX          │░ tunnel ░│ MAIN BOX (fuel-tank bay)│=TXAXLE
   │               │ A: ~7 mod / B: 3–4 │   │ A: ~5 / B: ~7 mod │  [HATCH:   │
   │               └──────────────┘     │   └──────────────┘     B: ~2 mod]  │
   └───────────────────────────────────────────────────────────────────────┘
        front axle ▲                                          ▲ rear axle
```

---

## Mounting & CG notes (the structural part)
- **Lowest CG wins.** Mount every box as low as the floorpan/bellypan allows — a low CG
  matters more for how the car feels than the exact front/rear split.
- **Front box:** ties into the engine-mount crossmember / front subframe points. Don't
  hang mass off shemetal — use the factory hardpoints.
- **Main box (fuel-tank bay):** the prime real estate — low, central, between the axles,
  right where the tank was. Frame it into the floor/tunnel structure; this box does most
  of the balancing work in Option B.
- **Hatch/spare-well box:** only for trim weight (Option B). Keep it modest or it
  rear-loads the car past traction-useful into tail-happy.
- **Crash & stiffness:** steel/aluminum enclosures bolted to structure double as a small
  stiffness gain; keep the MSD reachable and HV isolated from the chassis.
- **Net result:** ~3,300 lb (≈ +400 over stock), CG lower than stock (mass is in the
  floor, not up high in an iron engine), balance tunable 47–50% front via the split above.

## How to actually hit it
1. Build to the **Option B split** (easier, traction-friendly).
2. After assembly, **corner-balance on scales**; move 1–2 modules between the front and
   main boxes to trim toward your preference.
3. Log the measured corner weights here and update the worksheet with real numbers.
