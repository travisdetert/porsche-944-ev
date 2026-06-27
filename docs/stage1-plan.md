# Stage 1 Mule — Realistic Timeline

The honest version. The 4-week "sprint" (kept below as the **best-case floor**) assumed
every external dependency broke your way and you hit zero commissioning gremlins — which
never happens on a first-time, part-time conversion of a 39-year-old car. **Plan to ~5
months at ~20–30 nominal hrs/week.** Here is why, and the phased plan that gets you there.

**Assumptions:** ~20–30 hrs/week *nominal* · adapter outsourced · fully equipped shop ·
first serious HV/EV build.

---

## Why personal car projects slip (so the number is credible, not padded)
- **Effective hours < nominal.** Life, fatigue, and eaten weekends turn 20–30 "available"
  into **~12–18 effective**. Plan on ~60–70% realization.
- **Learning curve.** First HV build, first ZombieVerter config — every unknown is a few
  evenings of reading/forums before you turn a wrench.
- **Lead times stack.** Finding the *right* donor (not the first), adapter machining **plus
  a test-fit and a likely revision**, parts shipping, and the re-order cycle ("wrong lug,
  need another connector") — these run in series more than you expect.
- **Commissioning gremlins.** CAN comms, throttle calibration, contactor sequencing, BMS
  faults. This is the **widest-variance phase** — it can be a weekend or a month.
- **A 39-year-old car fights back.** Seized fasteners, rust, a transaxle that wants
  attention while it is out.
- **DMV is not on your schedule.** Converted-EV registration/inspection runs weeks to
  months and is mostly out of your hands.

---

## Three-point estimate (heavy part-time)
| Scenario | Duration | What it assumes |
|---|---|---|
| **Stretch (floor)** | **~3 months** | Lucky on donor + adapter, no major gremlins, hours hold |
| **Expected (plan to this)** | **~5 months** | Normal slips, one adapter revision, a real debug phase |
| **Conservative (don't be shocked)** | **~7–9 months** | First-timer reality: lead-time stacking + a stubborn gremlin or two |

**Plan to Expected. Protect it like Stretch. Don't panic at Conservative.**

---

## Phased plan (anchor: Month 1 = July 2026 — shift if you start later)

| # | Phase | Stretch | **Expected** | Conservative | Target done |
|---|---|---|---|---|---|
| 1 | **Plan & source** — donor hunt, adapter design + quotes, order long-lead parts | 2 wk | **4 wk** | 6 wk | **end Jul** |
| 2 | **Teardown & adapter** — engine out + strip; machine adapter + test-fit + revise | 3 wk | **5 wk** | 8 wk | **mid-Sep** |
| 3 | **Mechanical** — mount EM57, align driveline, fit donor pack + mounts | 2 wk | **3 wk** | 5 wk | **early Oct** |
| 4 | **Electrical** — HV box, wiring, VCU config, DC-DC, charger, 12V | 2 wk | **4 wk** | 6 wk | **early Nov** |
| 5 | **Commission & debug** — power-up, on-stands spin, chase gremlins | 2 wk | **4 wk** | 8 wk | **late Nov** |
| 6 | **Shakedown & register** — brakes/suspension, real driving, fixes, DMV | 2 wk | **4 wk** | 6 wk | **Dec–Jan** |

Phases overlap (sourcing/ordering bleeds into teardown), so calendar end is a bit less
than the raw sum. **Expected: drives under its own power ~late Nov/early Dec; registered &
shaken-down ~Dec–Jan 2027.**

### Milestones (expected, to push toward)
- **🏁 End Jul** — donor bought, parts ordered, adapter at the shop, engine coming out.
- **🏁 Mid-Sep** — adapter fitted, EM57 mounted to the transaxle, driveline aligned.
- **🏁 Early Oct** — donor pack fitted; mechanicals done.
- **🏁 Early Nov** — fully wired; ready for first power-up.
- **🏁 Late Nov/Dec** — **drives under its own power; grocery loop on private property.**
- **🏁 Dec–Jan** — registered, shaken down, daily-able.

---

## Still hold *others* to dates (the forcing-function part survives)
Realistic lead times, but you still make these parties commit so *their* slips don't become *your* surprises.

| Party | Commitment | Realistic due | If they slip |
|---|---|---|---|
| Machine shop | Adapter built (expect a revision) | quote says ≤3 wk → hold them to it | Backup shop quoted up front |
| Donor seller | The *right* Leaf, not the first | within Phase 1 | Keep 2–3 listings warm; don't overpay to rush |
| Parts vendors | ZombieVerter + HV bits | order at Phase 1 start | Order early; the re-order cycle is the hidden tax |
| DMV / inspector | Requirements + a slot | ask in Phase 4 | Drive private property until cleared |

---

## What actually buys you speed (levers, not wishful hours)
- **Buy a donor that already runs/drives** — a known-good EM57 + inverter + pack cuts the
  commissioning gremlin phase (your biggest variance) dramatically.
- **Reuse a proven 944 adapter design** if a prior builder shares one — skips a revision.
- **Batch the small-parts order** (lugs, connectors, fuses, fittings) so you're not losing
  weeks to one-at-a-time re-orders. The re-order cycle is the silent killer.
- **Protect a weekly cadence** — steady 15 effective hrs beats sporadic 30s; momentum is
  the whole game on personal projects.

## Stage 1 = done when (target late-Nov → Jan)
- [ ] EM57 on the stock transaxle via the adapter; spins on stands under power
- [ ] Running on the donor Leaf pack through the HV safety loop
- [ ] Charges (Leaf OBC); drives a ~5–15 mi grocery loop
- [ ] (Trailing) registered/inspected for public-road use

---

<details>
<summary><b>Best-case floor — the original 4-week sprint (reference only)</b></summary>

The aggressive version is achievable *only* if: donor in hand week 1, adapter delivered in
≤9 days, zero commissioning gremlins, and ~30 effective hrs/week sustained. Treat it as the
**physical lower bound**, not a schedule. The realistic plan above is what to actually
commit to and communicate.
</details>
