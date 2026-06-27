# Procurement & Rollout — getting it moving (Stage 1)

The actionable, money-aware plan to actually start: **what to buy, when, how much, and how
to pay for it** — overlaid on the ~5-month timeline. Pairs with `stage1-plan.md` (the
phase/effort estimate); this is the **buy-what-when + cash-flow** view.

**Anchor:** Month 1 = **July 2026** → driving mule ~**Nov–Dec 2026**. Shift the anchor if you
start later; keep the sequence.

---

## The money, honestly
- **Core build** (drivetrain + battery + HV): **~$3.5–5.5k**.
- **+ one-time safety gear** (PPE, DC meter, megger — reusable forever): **~$400**.
- **+ sort & register** (suspension tweak, fees): **~$1k**.
- **− gas-parts resale** (engine, ECU, intake, exhaust, fuel system, rad, A/C): **~$0.5–1.5k in**.
- **Realistic all-in net: ~$4–6k**, and **the donor Leaf is the only big single hit** —
  everything else is spread out.

## Cash flow at a glance (anchored)
| Month | Buy / sell | Out | In | Running net |
|---|---|---|---|---|
| **M1 Jul** | HV safety gear / PPE | $400 | | −$400 |
| **M1 Jul** | **Sell the gas parts** | | +$1,000 | +$600 |
| **M1 Jul** | **Donor Leaf** (the big one) | $3,500 | | −$2,900 |
| **M1 Jul** | ZombieVerter + HV BOM | $950 | | −$3,850 |
| **M2 Aug** | Adapter machining | $700 | | −$4,550 |
| **M3 Sep** | Enclosures + small parts | $400 | | −$4,950 |
| **M4 Oct** | Commissioning consumables | $150 | | −$5,100 |
| **M5 Nov** | Suspension + registration | $800 | | −$5,900 |

> Net **~$4.9k** at these mid-range numbers — **~$3.5–4k** with a cheap donor + strong parts
> sales. Selling the gas parts in M1 **funds the safety gear and softens the donor hit.**

---

## The buy list (scheduled — long-lead first)
Buy in *this* order; the early items gate everything downstream.

| # | Item | Buy when | ~Cost | Why then / note | Reused in Stage 2? |
|---|---|---|---|---|---|
| 1 | **HV safety gear** (Class-0 gloves, CAT III DC meter, megger, extinguisher) | M1, first | $400 | Needed before any HV work; one-time | ✅ |
| 2 | **Donor Leaf** (EM57 + inverter + charger + battery + LBC) | M1, after PF1 | $2.5–4.5k | **Gates extraction, adapter measurement, the whole build** | ✅ (all but the battery) |
| 3 | **ZombieVerter + HV BOM** (contactors, precharge, DC fuse, MSD, 2/0 cable, lugs, loom) | M1, after PF2 | $700–1.2k | Shipping is its own lead time; **batch it** to dodge the re-order cycle | ✅ |
| 4 | **Adapter machining** (service, not a part) | M2, after teardown + extraction | $500–900 | Critical path — quote at PF3, expect a revision | ✅ |
| 5 | **Enclosure stock + small parts** (steel/ally, fittings, connectors) | M3 | $200–500 | When building the pack boxes | ✅ |
| 6 | **Suspension / brakes** (uprated springs/dampers, pads) | M5 | $400–800 | During the sort phase, once weight is real | ✅ |
| — | ~~Tesla 14S1P pack~~ | **NOT NOW** | — | **Stage 2 only.** Run on the donor battery first. | — |

---

## Month-by-month (execution + procurement together)

### M0 / pre-start (late June – early July) — close gates, spend almost nothing
- Close **Pre-Flight** (free): PF1 ZombieVerter gen support, PF2 fuse/precharge values, PF3 adapter quotes.
- **Buy:** HV safety gear (~$400).
- **Start teardown** (#8) — free.

### M1 · July — teardown, sell, and the big buy
- Pull the engine; **sell the gas parts** (cash *in*).
- **Buy the donor Leaf**; extract motor/inverter/charger/pack/LBC/pedal/charge port.
- **Order ZombieVerter + HV BOM** (batched).
- Measure the bays + torque-tube flange; **send the adapter to the machine shop**.

### M2 · August — adapter & mechanical
- Pay for + receive the **adapter** (expect one revision); **mount the EM57**, verify driveline true.

### M3 · September — pack & HV wiring
- Build the **donor pack into the boxes** (6 front / 8 main layout); buy enclosure stock + small parts.
- Wire the **HV safety loop** (parts already on hand); DC-DC, charger, 12V.

### M4 · October — commission
- Bench-verify control → first spin on stands → first low-speed drive. Minor consumables.

### M5 · November — sort & register
- **Suspension/brakes** for the added weight; **registration/inspection**; the grocery loop.

---

## Procurement critical path & risks
- **The donor purchase gates everything** — extraction, adapter measurement, and the whole
  downstream build wait on it. Buy the *right* one (LeafSpy SOH), but don't dawdle.
- **Adapter is the lead-time risk** — it's a *service*, not a shelf part. Quote two shops at
  Pre-Flight; expect a test-fit + revision.
- **Batch the HV order** — the one-at-a-time "oops, wrong lug" re-order cycle is the silent
  schedule killer.
- **Do not buy the Tesla pack** — Stage 2. The whole point is to drive on the free donor
  battery first.

> Methodology + three-point estimate (stretch/expected/conservative): `stage1-plan.md`.
> Tracked, gated tasks: the session task list (#1–#15).
