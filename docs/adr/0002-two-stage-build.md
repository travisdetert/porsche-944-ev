# ADR-0002: Two-stage build — grocery mule, then 150-mile pack

**Status:** Accepted
**Date:** 2026-06-26
**Deciders:** Travis

## Context
This is a first-time, part-time, budget-driven conversion. The two biggest risks are the
**custom motor-to-transaxle adapter** and **commissioning gremlins**, and the single most
expensive item is the **~$10k Tesla traction pack**. We want a cheap checkpoint that proves
the car actually drives *before* committing the big spend.

## Decision
We will build in **two stages**: Stage 1 a **"grocery mule"** running on the **donor Leaf's
own battery** (free with the motor/inverter), then Stage 2 swap in a **Tesla 74 kWh pack**
for ~150 mi. The mule *becomes* the final car — a battery swap, not a rebuild.

## Alternatives considered
- **Build it once with the full Tesla pack** — rejected: puts ~$10k at risk before the
  adapter and commissioning are proven, with no cheap "does it drive?" checkpoint.
- **Keep the donor Leaf pack forever (no Stage 2)** — kept as a *fallback*, not the plan:
  fine for a mule but range is limited/degraded; Stage 2 is the path to the 150-mile goal.

## Consequences
- **Positive:** ~$0 incremental battery for Stage 1; de-risks the adapter + commissioning
  before the big spend; fast path to "it drives"; the mule is the final car.
- **Negative / accepted cost:** a second battery-build phase later; the donor pack must be
  packaged so it (or its modules) reuse the **same boxes** the Tesla pack will use (ADR-0005).
- **Follow-ups:** ADR-0003 (Stage-2 Tesla pack), ADR-0007 (BMS per stage).
