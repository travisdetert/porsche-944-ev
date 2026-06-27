# ADR-0005: Low, split battery layout — 6 front / 8 main

**Status:** Accepted
**Date:** 2026-06-26
**Deciders:** Travis

## Context
~880 lb of battery has to go somewhere. The 944 offers three usable volumes — engine bay,
fuel-tank bay, rear well — each with constraints (the **torque tube** down the tunnel, the
**rear torsion-bar cross-tube**, and **ground clearance**). Pulling the heavy front engine
left the car light up front. We want to preserve ~50/50 and **lower the CG**.

## Decision
We will **split the 14-module pack 6 front (engine bay) / 8 main (fuel-tank bay)**, mounted
**as low as ground clearance + a skid plate allow**, with the rear well reserved for trim.

## Alternatives considered
- **All mass in the rear** (the common DIY instinct) — rejected: biases the car too far rear
  and, if stacked, raises the CG; it also ignores that the removed front engine left the nose
  light, so the battery is needed *forward* to rebalance.
- **Theoretical even 7/7 split** — rejected: the front bay also holds the inverter, PDM, VCU,
  and contactor/fuse box, so **6 modules up front is the buildable number**; 6/8 lands ~48%
  front — still the slight rear bias a RWD car wants.

## Consequences
- **Positive:** CG **lower than stock** despite +575 lb; ~48% front (planted RWD balance);
  leaves the front bay actually buildable; the **same boxes serve Stage 1 and Stage 2**.
- **Negative / accepted cost:** main-box depth is limited by ground clearance + skid plate;
  the main box must sit **forward of the torsion-bar tube**; final fit needs on-car measurement.
- **Follow-ups:** `944-layout-design.md`; on-car measurements (during teardown);
  corner-balance during commissioning.
