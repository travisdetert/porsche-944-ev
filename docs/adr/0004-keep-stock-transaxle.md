# ADR-0004: Keep the stock transaxle (Tier 2 conversion)

**Status:** Accepted
**Date:** 2026-06-26
**Deciders:** Travis

## Context
The 944 is a transaxle car: front motor location, a torque tube to a **rear-mounted gearbox +
differential**, and near-50/50 balance. The engine is dead, but the **driveline (torque tube,
transaxle, diff, half-shafts, suspension) is excellent**. Conversion approaches range from
"mount a motor to the existing transaxle" to "replace the whole rear end with a Tesla drive
unit." This is the foundational architecture decision — the mission is to *keep the Porsche,
change only the engine.*

## Decision
We will **keep the stock 944 transaxle and driveline**, mounting the electric motor to it via
a custom adapter and running it in a **single gear** — the "Tier 2" approach.

## Alternatives considered
- **Tesla rear drive unit, direct-drive (Tier 3)** — rejected: replaces the transaxle,
  requires a custom rear subframe + axles (a structural redesign), costs far more, and
  **discards the very mechanicals that make it a 944.**
- **Multi-speed / retain shifting** — rejected: unnecessary. EV torque from 0 rpm means one
  gear is fine, and clutchless operation simplifies the build.

## Consequences
- **Positive:** reuses ~all of the driveline (the core cost saving); preserves the 944's
  balance and character; aligns with the project's spirit; simplest fabrication path.
- **Negative / accepted cost:** power and top speed are capped by the stock transaxle's
  limits; the **custom motor-to-torque-tube adapter** becomes the main fab task and critical
  path (no off-the-shelf 944 part exists).
- **Follow-ups:** ADR-0001 (Leaf drivetrain on this transaxle); adapter design (build-guide §2B).
