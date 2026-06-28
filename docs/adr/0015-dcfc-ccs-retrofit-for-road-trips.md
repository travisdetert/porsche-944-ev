# ADR-0015: DC fast charging (CCS) — a v2 retrofit for long trips, not v1

**Status:** Accepted
**Date:** 2026-06-28
**Deciders:** Travis
**Supersedes:** part of [ADR-0006](0006-ac-l2-charging-v1.md) (the "deferred DCFC" follow-up)

## Context
A trip-coverage simulation (`sim/trip_coverage.py`) ran real road distances from Menomonee
Falls against the planned **EM57 + 74 kWh** build at highway speed (10% arrival reserve,
**AC L2 only**). Result:

| Trip | 1-way | Verdict on AC L2 only |
|---|---|---|
| Lake Geneva (56 mi) | 56 | ✓ round-trip on one charge |
| Wisconsin Dells (119 mi) | 119 | ✓ reach it, overnight L2 at destination |
| Green Bay (118 mi) | 118 | ✓ reach it, overnight L2 |
| Door County (153 mi) | 153 | ✓ reach it, overnight L2 |
| **Minocqua (236 mi)** | 236 | ✗ needs an en-route charge |
| **Bayfield / Apostle Is. (353 mi)** | 353 | ✗ needs an en-route charge |

Two findings drove this decision:
1. **The motor is never the limit** — coverage is set by battery + charging (confirms ADR-0011).
2. **More battery does not unlock the far-north trips** — 74→90 kWh still can't reach Minocqua
   or Bayfield one-way; both still need a mid-trip charge. On 6.6 kW L2 that charge is **4–8 hours**,
   which is impractical. The unlock is **charge speed**, not pack size.

## Decision
Keep **v1 AC L2 only** (ADR-0006) — it covers the entire weekend-getaway radius with overnight
destination charging. Treat **CCS / DC fast charging as a planned v2 retrofit**, justified
specifically by **long northern-Wisconsin trips** (Northwoods, Lake Superior), not daily use.
Do **not** buy more battery to chase those trips.

## Alternatives considered
- **Bigger pack (90 kWh+) instead of DCFC** — rejected: doesn't reach the far-north destinations
  one-way, adds weight/cost/packaging for trips it still can't do without stopping.
- **Accept multi-hour L2 lunch stops / 2-day drives** — viable as a stopgap with zero hardware
  cost; the far-north trips are rare. This is the **v1 answer** until the retrofit lands.
- **DCFC now (in v1)** — rejected: cost + control complexity (ADR-0006) for trips that are the
  exception, not the rule.

## Consequences
- **Positive:** v1 stays cheap and covers ~everything you'll actually drive; the road-trip gap
  is named, scoped, and deferred rather than over-built for up front.
- **Negative / accepted cost:** no fast charging until the retrofit; the two deep-north trips are
  "plan around it" (overnight stops) in v1.
- **Follow-ups / when we retrofit:** confirm the pack/BMS supports the CCS charge rate and the
  contactor/precharge for DCFC current; price a CCS inlet + control (ZombieVerter CCS support or a
  dedicated charge controller); re-run `sim/trip_coverage.py` with DCFC stop times to confirm the
  far-north trips become practical. Tracked by backlog #18.
```
