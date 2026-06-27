<!--
  PROJECT.md — the project charter. One scannable file that answers
  "what is this, and how do we know when it's done?"
  Status values: Idea · Building · Usable · Done · Parked
-->
# 944 EV Conversion — Charter

**Status:** Building
**Updated:** 2026-06-26

> ✅ **Prices verified against 2026 vendor pages** (deep-research pass, June 2026).
> Figures marked _(unverified)_ are sourced leads that didn't clear the fact-check.
> **Build committed: the Leaf path** (see The build).

## Goal
Convert a 1987 Porsche 944 (currently sidelined by a hard-starting issue) into a
street-legal, daily-drivable EV with **~150 miles of real-world range** and
performance noticeably better than the stock car — built **"Tier 2": as cheaply as
possible without giving up the stock transaxle.** The north star is a registered,
reliable EV that road-trips 150 miles on a charge, built mostly with salvaged parts
and DIY labor.

## The build (Leaf path)

| System | Choice | Notes |
|---|---|---|
| **Motor** | **Nissan Leaf EM57** (salvage) | Cheapest serious motor; integrated reduction output → custom adapter |
| **Controller/VCU** | **ZombieVerter VCU** + reused **stock Leaf inverter** | ~$0.9–1.4k all-in; the budget hero |
| **Drivetrain** | **Stock 944 transaxle**, run in one gear; **custom EM57→torque-tube adapter** | The Tier 2 cost-saver + the main fab task |
| **Battery** | **14S1P Tesla, 74 kWh, 319 V** (~222 mi) | High voltage suits the Leaf inverter → low current/thin cable. See `docs/battery-pack-and-balance.md` |
| **BMS** | simpBMS / Orion (14 module taps) | Monitors full series string |
| **Charger** | Leaf OBC or aftermarket (Elcon/TC) | AC L1/L2 to start |
| **DC-DC** | Salvage or new (12V system) | Required |
| **HV plumbing** | MSD, HV fuse, main + precharge contactors, wiring | Build/test first — see `docs/drivetrain-diagrams.md` §6 |

**Target range:** ~150 mi (build is capable of ~222) · **Est. 0–60:** ~7 s ·
**Est. weight:** ~3,475 lb (+575 over stock), **49 / 51 front/rear**

### Two stages (prove it cheap, then scale the pack)
- **Stage 1 — grocery-getter mule (~$3.5–5.5k):** build the full Leaf drivetrain but run
  on the **donor Leaf's own battery** (free with the motor/inverter, ~50–100 mi). Proves
  the adapter, transaxle, VCU, and HV loop. **True extra cost ≈ $0** — deferred, not extra
  spend. See `docs/mvp-mule.md`.
- **Stage 2 — 150-mi pack:** build the **Tesla 14S1P / 74 kWh** pack and **swap the battery
  only** (~319 V is compatible with the Leaf inverter). Everything else carries forward.

## Budget (parts only, DIY labor — verified June 2026)

| Item | Cost | Source basis |
|---|---|---|
| Motor — Leaf EM57 | $550–1,030 _(unverified)_ | eBay/salvage listings |
| ZombieVerter VCU + reuse stock Leaf inverter | $380 bare ($810 assembled) | evbmw.com (350/750 EUR, verified) |
| **Battery — 14 Tesla modules (74 kWh)** | **~$9,700** @ ampREVOLT $690/ea (up to ~$19.6k premium vendors) | ampREVOLT/EV West/Stealth (verified) |
| &nbsp;&nbsp;_budget alt:_ whole salvage Bolt pack (~66 kWh) | _~$3,000–4,500 (unverified)_ | Bolt forum data — cheaper, harder to repackage |
| BMS (simpBMS / Orion 2) | $300–1,000 | — |
| EM57 adapter plate + coupler (custom) | ~$520–760 parts + machining _(unverified)_ | DIYEC forums; no off-the-shelf 944 part |
| Charger / DC-DC / HV plumbing / wiring | $1,000–2,000 | _(not separately verified)_ |
| Suspension (added weight) | $400–800 | _(not researched)_ |
| **Realistic total** | **~$8.5k (Bolt pack) – ~$14k (cheap Tesla modules)** | battery is the swing |

## Key findings (research pass, June 2026)
- **150 mi is comfortably met by this build.** 74 kWh × ~0.9 usable ÷ 300 Wh/mi ≈
  **~222 mi** (~194 even at worst-case 343). The earlier "no 944 keeps the transaxle
  *and* hits 150 mi in any published build" caveat stands as a documentation gap, not a
  physics problem — our pack is >3× the best transaxle-retaining DC build's ~22 kWh.
  See `docs/range-analysis.md`.
- **No off-the-shelf 944 transaxle adapter exists** (vendors sell 911/914). The EM57's
  integrated reduction output needs a **custom adapter/coupler** — the build's main
  fabrication task and primary schedule risk.
- **Battery is the budget swing.** 14 Tesla modules run ~$9.7k at the cheapest vendor
  (~2× spread to premium); a whole salvage **Bolt pack (~$3–4.5k)** is far cheaper but
  pouch-format and harder to split across the 944's three bays.
- **Leaf inverter at 319 V** (14S) is near its happy zone and gives low current
  (~345 A) → thin 2 AWG cable. **Validate inverter + ZombieVerter at 319 V / target
  power before committing all 14 modules.**
- **Converted balance ≈ 49.0 % front / 51.0 % rear at ~3,475 lb**, lower CG than stock.
  Pulling the heavy engine means the battery adds weight *forward* — split 7 front / 7
  main. See `docs/battery-pack-and-balance.md`.

## Definition of Done
v1 is done when all of these are true:
- [ ] EM57 mounted to stock transaxle via custom adapter, spins under power on the stand
- [ ] **74 kWh (14S1P) Tesla pack** assembled, BMS monitoring all modules, balanced 7/7 for ~49/51
- [ ] Charges from a standard L2 EVSE
- [ ] Drives under its own power; **150 mi verified on a real drive**
- [ ] Brakes & suspension sorted for the added ~575 lb
- [ ] Street-legal: passes state inspection / registration (weight, brakes, lighting)
- [ ] HV safety reviewed (interlocks, fusing, isolation); wiring documented
- [ ] Build documented well enough to fault-find from a fresh look (README/wiring diagram)

## Now / Next
- **Now:** Leaf path committed; staged plan set — **Stage 1 mule first** (run on donor
  battery), Tesla pack deferred to Stage 2.
- **Next (Stage 1):**
  1. Source the **Leaf donor** (EM57 motor + inverter + OBC + **its battery**) and a **ZombieVerter VCU**.
  2. Design + machine the **EM57→torque-tube adapter** (the main fab task).
  3. Build the **HV safety loop** and bench-spin the EM57 on the donor pack.
  4. First grocery-loop drive; (if road-driven) register.
- **Then (Stage 2):** build the **Tesla 14S1P / 74 kWh** pack and swap the battery for 150 mi.
- **Later:** CCS DC fast charging; range/efficiency tuning; interior gauges/telemetry.

## Open questions
- Fab comfort level (machining the EM57 adapter, self-integrating the inverter wiring)?
- Garage/tools available (engine hoist, welder, HV-rated PPE & meter)?
- State registration requirements for a converted EV?

## Links
Stage 1 mule: `docs/mvp-mule.md` · Drivetrain & HV diagrams: `docs/drivetrain-diagrams.md`
· Pack & balance: `docs/battery-pack-and-balance.md` · Range: `docs/range-analysis.md` ·
Build order: `docs/build-order.md` · Decisions: `docs/adr/` · Security/HV-safety: `SECURITY.md`
