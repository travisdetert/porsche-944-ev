# ADR-0006: AC Level-2 charging for v1 (defer DC fast charge)

**Status:** Accepted
**Date:** 2026-06-26
**Deciders:** Travis

## Context
Charging options span **reusing the donor Leaf's onboard charger (AC L1/L2)** to adding
**CCS / DC fast charging** (significant cost and control-system complexity). The v1 goal is a
cheap car that drives and charges for daily/grocery use, charged at home.

## Decision
We will charge via the **reused Leaf PDM (AC L1/L2)** for v1, with the **J1772 inlet in the
old fuel-filler door**. DC fast charging is **deferred**.

## Alternatives considered
- **Add CCS / DC fast charging now** — rejected: meaningful added cost and control complexity
  for a home-charged grocery car; it can be retrofitted later if road-tripping becomes a goal.

## Consequences
- **Positive:** ~$0 charger (reuse the donor PDM); simple; reuses the fuel door for the inlet
  (cheap and clean); perfectly adequate for overnight/home charging.
- **Negative / accepted cost:** no fast charging in v1; slower charge rate; a CCS retrofit
  later is non-trivial.
- **Follow-ups:** a future ADR if/when DC fast charging is added.
