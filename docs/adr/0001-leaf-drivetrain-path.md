# ADR-0001: Use the Nissan Leaf drivetrain (EM57 + reused inverter + ZombieVerter)

**Status:** Accepted
**Date:** 2026-06-26
**Deciders:** Travis

## Context
The 944's engine is dead (hard-starting); the mission is to get it running again **as
cheaply as possible** while keeping the stock transaxle and the car's mechanicals. The
motor + controller choice drives cost, fabrication effort, system voltage, and — critically
— whether we can prove the build with a cheap "does it drive" mule before spending on a
full traction pack. Options range from salvage-DIY to bolt-on commercial kits.

## Decision
We will use the **Nissan Leaf drivetrain**: a salvage **EM57 motor** on its **reused stock
Leaf inverter**, commanded by a **ZombieVerter VCU**, mated to the stock 944 transaxle via a
custom adapter. The Stage-1 mule runs on the **donor Leaf's own battery**.

## Alternatives considered
- **NetGain HyPer9 + X1 kit (bolt-on)** — plain keyed shaft makes the adapter easy, but the
  kit is **~$5.4k** vs ~$0.9–1.4k for the Leaf motor+controls, runs at low voltage
  (114 V → ~790 A, fat cable), and — decisively — **a kit ships no battery**, so it can't
  seed the free donor-battery mule. Rejected on cost + losing the mule synergy.
- **HyPer9 HV + AC-X144** — same bolt-on simplicity at higher voltage, but still **~$5.6k**
  and no free matched mule battery. Rejected on cost.
- **Tesla drive unit, direct-drive** — fast and high-range, but **replaces the transaxle**
  (a structural redesign) — contradicts "keep the great Porsche mechanics" and costs far
  more. Rejected.

## Consequences
- **Positive:** cheapest drivetrain (~$0.9–1.4k motor+controls); **one salvage Leaf yields
  motor, inverter, charger, DC-DC, BMS (LBC), and a battery — all factory-matched**; the
  donor's own pack enables the Stage-1 mule at **~$0 incremental battery cost**; high pack
  voltage (319 V at 14S1P) → low current → thin 2 AWG cable; ZombieVerter reuses the Leaf
  LBC as the Stage-1 BMS.
- **Negative / accepted cost:** the EM57's **integrated reduction output needs a custom
  machined adapter/coupler** — the main fabrication task and the schedule's critical path;
  we **self-integrate** the inverter/VCU wiring (vs. a plug-and-play kit); the build depends
  on **ZombieVerter support for the exact donor Leaf generation**; full-pack HV (319 V)
  throughout demands strict isolation discipline.
- **Follow-ups:** future **ADR-0002** (two-stage mule-then-pack) and **ADR-0003** (14S1P /
  74 kWh Tesla Stage-2 pack). Verify **ZombieVerter gen support (Pre-Flight PF1)** and the
  **EM57 inverter fuse/precharge values (PF2)** before purchasing — see `docs/drive-plan.md`.
