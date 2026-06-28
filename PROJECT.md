<!--
  PROJECT.md — the project charter. One scannable file that answers
  "what is this, and how do we know when it's done?"
  Status values: Idea · Building · Usable · Done · Parked
-->
# 944 EV Conversion — Charter

**Status:** Building (planned end-to-end; teardown active)
**Updated:** 2026-06-27

> ✅ **Prices verified against 2026 vendor pages** (deep-research pass, June 2026).
> Figures marked _(unverified)_ are sourced leads that didn't clear the fact-check.
> **Build committed: the Leaf path** (see The build).

## Goal
**Get this 1987 Porsche 944 running again — as cheaply as possible.** It's been benched by
a hard-starting engine; rather than scrap a great car or rebuild a 39-year-old motor, give
it an electric heart from salvaged parts, keep everything that makes it a Porsche, and get
it driving again — starting with a grocery run. *Resurrection on a budget.*

In engineering terms: convert it to a street-legal, daily-drivable EV — **"Tier 2": as
cheap as possible without giving up the stock transaxle** — proving it out as a cheap mule
first (Stage 1), then growing to **~150 miles of real-world range** (Stage 2), built mostly
with salvaged parts and DIY labor.

**Character:** stripped to a lightweight **electric go-kart** — no A/C, carpet, or rear seats
(the gas parts fund the build) — but with a proper **stereo + subwoofers**. Light, low, raw,
and loud. See `docs/strip-list.md` and ADR-0008/0009/0010.

**The one rule (ADR-0011):** every part taken out saves money *and* weight, and **both go
straight into the drivetrain** — more battery (range) or more motor (power) — held at ≈ stock
weight and **true 50/50** (motor up front + transaxle at the rear are the balance anchors).
*Strip the fat, feed the muscle.*

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
**Est. weight:** Stage 1 ≈ **stock (~2,990 lb, stripped)**; Stage 2 ~3,320 lb · **~48 % front**
(6 front / 8 main, two bays)

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
  pouch-format and harder to split across the 944's **two battery bays** (rear well → subs).
- **Leaf inverter at 319 V** (14S) is near its happy zone and gives low current
  (~345 A) → thin 2 AWG cable. **Validate inverter + ZombieVerter at 319 V / target
  power before committing all 14 modules.**
- **Converted balance ≈ 48 % front / 52 % rear**, lower CG than stock (stripped, mass in the
  floor). Pulling the heavy engine means the battery adds weight *forward* — split **6 front /
  8 main** across two bays. See `docs/944-layout-design.md` + `docs/battery-fit.md`.

## Definition of Done
v1 is done when all of these are true:
- [ ] EM57 mounted to stock transaxle via custom adapter, spins under power on the stand
- [ ] **74 kWh (14S1P) Tesla pack** assembled (6 front / 8 main), BMS monitoring all modules, ~48 % front
- [ ] Stripped to go-kart spec; **stereo + subwoofers** installed and powered (ADR-0008/0009)
- [ ] Charges from a standard L2 EVSE
- [ ] Drives under its own power; **150 mi verified on a real drive**
- [ ] Brakes & suspension sorted for the added ~575 lb
- [ ] Street-legal: passes state inspection / registration (weight, brakes, lighting)
- [ ] HV safety reviewed (interlocks, fusing, isolation); wiring documented
- [ ] Build documented well enough to fault-find from a fresh look (README/wiring diagram)

## Now / Next
- **Now:** Leaf path committed; **Stage 1 is a realistic ~5-month build** (~20–30 hrs/wk) —
  see `docs/stage1-plan.md`. Expected: drives ~late Nov/Dec 2026, registered ~Dec–Jan.
  (4-week "sprint" is the best-case floor, not the plan.)
- **Next — Phase 1 (plan & source, ~4 wks):** follow `docs/phase1-donor-hunt.md` +
  `docs/hv-bom.md`; full procedure in `docs/build-guide.md`. **Read `SECURITY.md` first.**
  1. Hunt the **right Leaf donor** (LeafSpy SOH check; one that already runs cuts debug later).
  2. Finalize + quote the **EM57 adapter** at 2 shops; line up a backup.
  3. Batch-order **ZombieVerter + HV bits + small parts** (the re-order cycle is the hidden tax).
- **Then (Stage 2):** build the **Tesla 14S1P / 74 kWh** pack and swap the battery for 150 mi.
- **Later:** CCS DC fast charging; range/efficiency tuning; interior gauges/telemetry.

## Open questions
- Fab comfort level (machining the EM57 adapter, self-integrating the inverter wiring)?
- Garage/tools available (engine hoist, welder, HV-rated PPE & meter)?
- State registration requirements for a converted EV?

## Links
**▶ Start here:** `docs/next-steps.md` (one-page runbook) · **`steps/`** (step-by-step, `000-…`) ·
**Safety (read first):** `SECURITY.md` · **Build guide:** `docs/build-guide.md` ·
**Parts ledger (master):** `docs/parts-inventory.md` ·
**Money:** `docs/procurement-plan.md` + `docs/parts-list.md` + `docs/parts-shopping-list.md` · **Phase 1:** `docs/phase1-donor-hunt.md`
+ `docs/hv-bom.md` · **Timeline:** `docs/stage1-plan.md` · **Drive plan:** `docs/drive-plan.md` ·
**Strip list:** `docs/strip-list.md` ·
**Design:** `docs/944-layout-design.md`, `docs/battery-fit.md`, `docs/battery-pack-and-balance.md`, `docs/low-cg-packaging.md`,
`docs/drivetrain-diagrams.md`, `docs/control-wiring.md`, `docs/power-and-reuse-diagrams.md`, `docs/dashboard-reuse.md`, `docs/range-analysis.md` ·
**Sim:** `sim/` · **Custom parts (CAD):** `cad/` · **Head unit app:** `docs/control-computer.md` + `app/` · **Sequence:** `docs/build-order.md` ·
**Why staged:** `docs/mvp-mule.md` · **Decisions:** `docs/adr/`
