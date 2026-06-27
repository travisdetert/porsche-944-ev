# ADR-0003: Stage-2 traction pack — 14S1P Tesla, 74 kWh, ~319 V

**Status:** Accepted
**Date:** 2026-06-26
**Deciders:** Travis

## Context
Stage 2 needs ~150 mi while keeping the stock transaxle. The **reused Leaf inverter prefers
~350 V**, i.e. a long series string. Salvage module options are **Tesla** (5.3 kWh bricks),
**Chevy Bolt** (whole pack), and **Leaf**. Module choice sets voltage, energy, weight, cost,
and how cleanly the pack fits the 944's three bays.

## Decision
We will build the Stage-2 pack from **14 Tesla Model S/X 5.3 kWh modules in 14S1P** —
**74 kWh at ~319 V**.

## Alternatives considered
- **Whole salvage Bolt pack** (~66 kWh, ~$3–4.5k, cheapest per kWh) — rejected: a
  pouch-format *whole* pack is hard to split across the three bays and harder to match to the
  Leaf inverter's preferred voltage. Tesla bricks reconfigure cleanly.
- **Low-voltage pack** (e.g. 5S2P, 53 kWh, ~114 V) — rejected: only suits a low-voltage
  controller; the Leaf inverter wants high voltage, and 53 kWh gives a thin 150-mi margin.
- **16S / 85 kWh** — rejected as the base: more range but more weight/cost; 14S is the
  range-weight-voltage sweet spot.

## Consequences
- **Positive:** ~222 mi typical (comfortable 150-mi margin); 319 V → low current (~345 A) →
  thin 2 AWG cable; uniform bricks pack cleanly into the 6/8 layout (ADR-0005); near the Leaf
  inverter's happy voltage.
- **Negative / accepted cost:** Tesla modules cost more than a Bolt pack (~$9.7k cheapest
  vendor, ~2× vendor spread); full-pack 319 V means **every junction is at full HV** — strict
  isolation discipline (SECURITY.md).
- **Follow-ups:** confirm fuse/precharge values for 319 V (Pre-Flight PF2); simpBMS (ADR-0007).
