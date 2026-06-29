# Project Plan — 944 gas → EV (MVP grocery mule)

The **execution** plan (charter is `../PROJECT.md`; the app **PLAN** tab renders
`../app/frontend/tasks.json`, this doc's source of truth in summary form). Realistic, part-time.

## Phases & gates
The build is a spine of four phases with **gates** (PF = pre-flight checks, G = build gates) you
must pass before spending the next chunk of money/time. Two tracks run **in parallel** (the
head-unit app and the trips/charging research) so they never block the car.

```
NOW ──▶ BUY ──▶ BUILD ──▶ DRIVE
 │       │        │         │
 PF1✓    G1       G2 G3 G4  G6 G7
 PF3,4   PF2      G5
 (strip,quote,    (donor,   (adapter,mount, (power-up,
  safety,sell)     extract,  pack,wire HV)   drive,register)
                   order)
APP track:  build app ✓ → order Pi → bench (mock) → wire real CAN
TRIPS track: route study → charging map → strategy/DCFC → routes in-app
```

## Critical path (what actually gates "it drives")
1. **000 Pull engine + measure + weigh** → unlocks adapter quote, part sales, mounting dims.
2. **G1 Donor Leaf** (the long pole — hunting a good Gen-2 salvage can take weeks).
3. **G2 Adapter machined + dry-fit true** (machining lead + the one precision part).
4. **G3 Motor mounted on-axis** → **G4 Pack mounted + isolation pass** → **G5 HV wired + VCU bench-verified**.
5. **G6 Power-up on stands** → **G7 First drive** → register.

Everything else (app, trips, charging) is parallel and **must not** block this chain.

## Realistic timeline (part-time evenings/weekends — honest, not optimistic)
| Phase | Work | Calendar (realistic) | Long pole |
|---|---|---|---|
| NOW | strip, quote, safety, sell | 3–6 weeks | fastener fights, getting quotes back |
| BUY | donor hunt, extract, order | 1–3 months | **finding a clean Gen-2 salvage** |
| BUILD | adapter, mounts, pack, HV wiring | 2–4 months | **adapter machining**, first-time HV wiring |
| DRIVE | power-up, drive, register | 2–4 weeks | brake/vacuum sort-out, DMV |
| **Total** | | **~8–14 months** | donor + machining dominate |

First-time DIY EV conversions commonly run **1–2 years**; 8–14 months assumes steady weekend
pace and a donor found early. Treat dates as ranges, not promises.

## Risks & mitigations
- **Donor hunt drags** → start it now (parallel), set a SOH/price bar, use a salvage broker.
- **Adapter alignment** → dry-fit + dial-indicator < 0.1 mm before final machining (gate G2).
- **HV safety** → PPE + verify-dead procedure before *any* orange (PF4); never work alone on HV.
- **Brakes** (no engine vacuum) → confirm the electric booster/vacuum pump *before* the first drive.
- **Estimates vs reality** → 3 measurements collapse the unknowns: stripped-car weight (000), a real
  Wh/mi (G7), bay dims (000). Plug them into `ev_layout.json` + the sim.

## Definition of done (MVP)
Drives under its own power, completes the grocery loop, brakes/steers safely, charges on AC L2,
and is registered/insured. Stretch (Stage 2): Tesla pack for ~150 mi (separate plan).

## Status
See the **PLAN** tab (live board) or `tasks.json`. As of now: NOW phase, teardown in progress,
PF1 resolved (Gen-2 donor). Next concrete move: **pull the engine + weigh the stripped car**.
