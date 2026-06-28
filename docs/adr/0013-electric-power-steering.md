# ADR-0013: Retain power steering via an electric hydraulic pump

**Status:** Accepted
**Date:** 2026-06-27
**Deciders:** Travis

## Context
The 1987 944 has **hydraulic, engine-belt-driven** power steering. Removing the engine removes
the pump. We want to keep light, assisted steering on a street car (especially for parking),
without a bigger mechanical change.

## Decision
Keep the **stock 944 hydraulic rack** and drive it with a **salvage electric hydraulic
power-steering pump (EHPS)** — e.g. a Volvo / Toyota MR2 / Saab / VW electro-hydraulic unit —
wired to switched 12 V (on with the car).

## Alternatives considered
- **Accept manual steering** — rejected: heavy at parking speeds; the owner wants assist (the
  light stripped car softens it, but not enough).
- **Electric-assist column (EPS) swap** — rejected: a bigger change (column/rack swap) than
  simply pressurizing the existing rack with an EHPS.

## Consequences
- **Positive:** keeps the stock rack and steering feel; salvage EHPS is cheap (~$80–300);
  largely bolt-in + plumb to the existing lines.
- **Negative / accepted cost:** a **real 12 V load** — EHPS pumps pull ~20–50 A, so the
  **DC-DC must be sized** to cover it alongside the stereo + heater; needs a bracket + hose
  routing; optional speed-sensitive assist.
- **Follow-ups:** source the EHPS unit; **size the DC-DC** (`control-wiring.md`); add to the BOM;
  wire to switched 12 V.
