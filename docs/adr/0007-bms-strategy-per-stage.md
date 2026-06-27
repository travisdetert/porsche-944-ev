# ADR-0007: BMS strategy — Leaf LBC for Stage 1, simpBMS for Stage 2

**Status:** Accepted
**Date:** 2026-06-26
**Deciders:** Travis

## Context
The pack needs a BMS that **ZombieVerter can read** and that can **force the contactors open**
on fault (a SECURITY.md non-negotiable). Stage 1 runs on the donor Leaf pack; Stage 2 runs on
Tesla modules. The two packs have different native monitoring.

## Decision
For **Stage 1** we will **reuse the Leaf's own LBC** (battery controller), read by
ZombieVerter. For **Stage 2** (Tesla modules) we will use **simpBMS**.

## Alternatives considered
- **Buy a commercial BMS up front for both stages** — rejected: unnecessary spend in Stage 1,
  where the **Leaf LBC already monitors the donor pack** and ZombieVerter speaks to it.
- **Run no / minimal BMS** — rejected: unsafe. The BMS must be able to force the contactors
  open on over/under-voltage or over-temp (SECURITY.md).

## Consequences
- **Positive:** ~$0 BMS for Stage 1 (reuse the LBC); **simpBMS** is the proven open-source
  choice for Tesla modules; spend stays staged.
- **Negative / accepted cost:** a BMS swap at Stage 2; must validate **ZombieVerter ↔ LBC
  comms** for the exact donor Leaf generation.
- **Follow-ups:** Pre-Flight PF1 (generation support); simpBMS configuration at Stage 2.
