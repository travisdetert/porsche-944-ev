<!--
  PROJECT.md — the project charter. One scannable file that answers
  "what is this, and how do we know when it's done?"
  Status values: Idea · Building · Usable · Done · Parked
-->
# 944 EV Conversion — Charter

**Status:** Building
**Updated:** 2026-06-26

> ✅ **Prices verified against 2026 vendor pages** (deep-research pass, June 2026).
> Figures marked _(unverified)_ are sourced leads that didn't clear the fact-check —
> treat as ballpark. See **Key findings** for an important caveat on the 150-mi target.

## Goal
Convert a 1987 Porsche 944 (currently sidelined by a hard-starting issue) into a
street-legal, daily-drivable EV with **~150 miles of real-world range** and
performance noticeably better than the stock car — built **"Tier 2": as cheaply as
possible without giving up the stock transaxle.** The north star is a registered,
reliable EV that road-trips 150 miles on a charge, built mostly with salvaged parts
and DIY labor.

## The build (Tier 2 spec)

| System | Choice | Notes |
|---|---|---|
| **Motor** | NetGain HyPer9 *(bolt-on)* **or** Nissan Leaf EM57 *(cheaper, more fab)* | Decision pending — see Now/Next |
| **Controller/VCU** | HyPer9 controller, **or** ZombieVerter VCU + stock Leaf inverter | Pairs with motor choice |
| **Drivetrain** | **Keep stock 944 transaxle** (adapter plate, run in one gear) | The Tier 2 cost-saver |
| **Battery** | Path B: **10 modules, 5S2P, 53 kWh, 114 V** (~159 mi). HV/Leaf: **14 modules, 74 kWh** (7S2P 160 V / 14S1P 319 V), ~222 mi | Voltage window sets count — see `docs/module-placement-map.md` + `docs/module-placement-leaf-hv.md` |
| **BMS** | Open-source (simpBMS) or budget commercial | Sized to module count |
| **Charger** | Used Leaf OBC or aftermarket (Elcon/TC) | AC L1/L2 to start |
| **DC-DC** | Salvage or new (12V system) | Required |
| **HV plumbing** | Main contactor, precharge resistor, HV fuse, wiring | Common to all builds |

**Target range:** ~150 mi · **Est. 0–60:** ~7–8 s · **Est. added weight:** ~+400 lbs

## Budget (parts only, DIY labor — verified June 2026)

Two drive paths. **Path A (Leaf + ZombieVerter)** = cheapest, more fabrication.
**Path B (HyPer9 kit)** = bolt-on motor+controller, ~$4.5k more.

| Item | Path A — Leaf | Path B — HyPer9 | Source basis |
|---|---|---|---|
| Motor | Leaf EM57 ~$550–1,030 _(unverified)_ | — | eBay/salvage listings |
| Controller / VCU | ZombieVerter bare $380 (assembled $810) + reuse stock Leaf inverter | — | evbmw.com (350/750 EUR, verified) |
| Motor + controller (kit) | — | HyPer9 + X1 120V kit **$5,400** | EV West (verified, in stock) |
| Battery ~50 kWh | **Tesla:** 10–11× 5.3 kWh modules, **$6,900–$15,000** (huge vendor spread — ampREVOLT $690/ea vs EV West/Stealth ~$1,400–1,500/ea) · **Bolt:** whole 60+ kWh pack **$3,000–4,500** _(unverified)_ | same | ampREVOLT/EV West/Stealth (Tesla verified); Bolt forum data |
| BMS | $300–1,000 (simpBMS / Orion 2) | same | — |
| 944 adapter plate + coupler | **No off-the-shelf part exists** — custom fab. Forum parts: plate ~$320–400 + coupler ~$200–360 _(unverified)_, + machine-shop alignment | same | EV West catalog (verified: no 944 part); DIYEC forums |
| Charger / DC-DC / HV plumbing / wiring | $1,000–2,000 | same | _(not separately verified)_ |
| Suspension (added weight) | $400–800 | same | _(not researched)_ |
| **Realistic total** | **~$6.5k–11k** | **~$11k–16k** | cheapest = Leaf motor + Bolt pack |

_Cheapest verified bench-to-battery core: HyPer9 kit $5,400 + ZombieVerter $380 + ~10 Tesla modules @ $690 ≈ **$12,700**, before adapter fab, BMS, charger, donor. The Leaf-motor + Bolt-pack route undercuts this but is more fabrication._

## Key findings (research pass, June 2026)
- **The 150-mi + stock-transaxle combo isn't documented anywhere.** Every 944 build
  the research found does one or the other: high-range builds (e.g. the well-documented
  85 kWh Tesla-LDU 944) **replace** the transaxle; transaxle-retaining builds are
  low-range DC (the best-itemized one — WarP11 + Soliton1 + 64 CALB cells, ~$18k —
  only carried ~22 kWh / ~60 mi). **No one has published our exact recipe with a cost.**
  It's still plausible on paper: ~50–53 kWh is more than double that DC build's pack, so
  150 mi should be reachable — but treat it as unproven, not a copy-able blueprint.
- **No off-the-shelf 944 transaxle adapter exists.** EV West/canEV sell Porsche
  911/914 adapters, not 944. The 944's torque-tube/remote transaxle needs a **custom
  adapter plate** (forum builders machine their own). This is the main fabrication risk.
- **Battery is the budget swing.** Tesla module prices have a ~2× vendor spread
  ($690 vs ~$1,500 each) — shopping vendors is the single biggest lever. A whole
  salvage Bolt pack (~$3–4.5k for 60+ kWh) is cheapest per kWh but harder to repackage.
- **Controller voltage caps the pack (Path B).** HyPer9-std's ~132 V ceiling limits
  Tesla modules to **5S**, so the clean pack is **5S2P = 10 modules / 53 kWh** (~159 mi
  @ 300 Wh/mi; ~139 at worst-case 343). For guaranteed worst-case 150-mi margin, the
  higher-voltage **HV or Leaf path** allows more series modules → more kWh. See
  `docs/module-placement-map.md`.
- **Converted balance ≈ 49.3 % front / 50.7 % rear at ~3,255 lb** (10 modules split
  5 front / 5 main), with a lower CG than stock. Pulling the heavy engine means the
  battery is used to add weight *forward*. See `docs/weight-balance-layout.md`.
- **HyPer9 controller availability:** standalone X1 controller noted on backorder to
  ~April 2026 at some vendors; full kits were in stock at EV West.

## Definition of Done
v1 is done when all of these are true:
- [ ] Motor mounted to stock transaxle, spins under power on the bench/stand
- [ ] ~50 kWh pack assembled, BMS monitoring all modules, safely packaged & balanced for ~50/50
- [ ] Charges from a standard L2 EVSE
- [ ] Drives under its own power; **150 mi verified on a real drive**
- [ ] Brakes & suspension sorted for the added weight
- [ ] Street-legal: passes state inspection / registration (weight, brakes, lighting)
- [ ] HV safety reviewed (interlocks, fusing, isolation); wiring documented
- [ ] Build documented well enough to fault-find from a fresh look (README/wiring diagram)

## Now / Next
- **Now:** Tier 2 spec'd; 2026 prices verified (see Budget + Key findings). Open
  decision: Path A (Leaf, cheaper, more fab) vs. Path B (HyPer9, bolt-on).
- **Next:**
  1. Decide motor path: HyPer9 (bolt-on) vs. Leaf+ZombieVerter (cheaper, more fab).
  2. Source a battery donor and confirm module count for ~50 kWh.
  3. Source a 944 transaxle adapter plate.
- **Later:** CCS DC fast charging; range/efficiency tuning; interior gauges/telemetry.

## Open questions
- Fab comfort level (machining/welding adapter, self-integrating wiring)?
- Garage/tools available (engine hoist, welder, HV-rated PPE & meter)?
- State registration requirements for a converted EV?

## Links
Decisions: `docs/adr/` · Security/HV-safety: `SECURITY.md` · Usage: `README.md`
