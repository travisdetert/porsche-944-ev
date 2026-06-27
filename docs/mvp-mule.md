# 944 EV — Stage 1: The Grocery-Getter Mule (prove-it-first)

**Idea:** build the committed Leaf drivetrain, but **defer the 14-module Tesla pack** and
drive the car first on the **donor Leaf's own battery**. Prove the risky, fab-heavy parts
cheaply before spending ~$10k on the final pack. The mule *becomes* the final car — a pack
swap, not a rebuild.

## Why this is the cheapest possible minimal battery
You're buying a salvage Leaf for the **EM57 motor + inverter + charger** regardless. That
donor **ships with its own 24–40 kWh traction battery**, already **voltage- and
CAN-matched to its inverter**. So the mule's battery costs **$0 incremental** — you simply
don't buy the Tesla modules yet. It's *deferred* spend, not *extra* spend.

## Range — groceries many times over
| Donor pack | Health | Usable | Range @300 Wh/mi |
|---|---|---|---|
| 24 kWh Leaf | ~70% | ~15 kWh | **~50 mi** |
| 40 kWh Leaf | ~85% | ~30 kWh | **~100 mi** |

A grocery run is 5–15 mi round trip → **5–10× margin** even on a tired pack.

## What Stage 1 proves (and it all carries forward)
- The **custom EM57 → torque-tube adapter** + driveline alignment — the one real fab task
- **ZombieVerter** driving the reused **Leaf inverter**
- The **HV safety loop** (contactor, precharge, fuse, MSD, isolation)
- Throttle calibration, 12V/DC-DC, brakes/booster, first drive

## Cost to a driving car — nothing thrown away
| Item | Cost | Reused in final build? |
|---|---|---|
| Salvage Leaf donor (motor+inverter+charger **+ battery**) | ~$2,500–4,500 | ✅ all but the battery |
| ZombieVerter VCU | $380 | ✅ |
| Custom EM57 adapter + coupler | ~$520–760 + machining | ✅ |
| HV safety bits (contactor, precharge, fuse, MSD) | ~$300–500 | ✅ |
| Wiring / misc | ~$200 | ✅ |
| **Stage 1 total** | **~$3.5–5.5k** | the mule *is* the final car |

The donor is already in the plan, so the **true extra cost of Stage 1 ≈ $0** — it's purely
a sequencing choice.

## Can't be skipped, even for a mule
- **The adapter must be made** — no shortcut to turning the transaxle (but that's the point).
- **The HV safety loop is mandatory** — a 350 V Leaf pack hurts exactly like a Tesla one.
  No "just a test car" exceptions on fuse/contactor/precharge/MSD/isolation.
- **Registration** if it'll do grocery runs on public roads.

## Stage 1 → Stage 2 upgrade (a clean swap)
The Leaf pack runs ~350 V; the committed **Tesla 14S1P runs ~319 V** — compatible window.
When you want the full 150 mi, **build the Tesla pack and swap the battery only.** Motor,
inverter, VCU, adapter, and HV wiring all stay. See `battery-pack-and-balance.md` for the
Stage 2 pack.

## Stage 1 "done"
- [ ] EM57 on the stock transaxle via the custom adapter; spins on stands under power
- [ ] Running on the donor Leaf pack through the HV safety loop
- [ ] Charges (Leaf OBC) and drives a real ~5–15 mi grocery loop
- [ ] (If road-driven) registered/inspected
