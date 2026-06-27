# Architecture Decision Records

Decisions behind the 944 EV conversion. One file per decision, **immutable once Accepted**;
a reversal gets a new ADR that supersedes the old one. The value is the *why* and the
*alternatives rejected*. Template: `~/.claude/templates/ADR.md`.

| ADR | Decision | Status |
|---|---|---|
| [0001](0001-leaf-drivetrain-path.md) | Use the Nissan Leaf drivetrain (EM57 + reused inverter + ZombieVerter) | Accepted |
| [0002](0002-two-stage-build.md) | Two-stage build — grocery mule, then 150-mile pack | Accepted |
| [0003](0003-stage2-tesla-pack.md) | Stage-2 pack: 14S1P Tesla, 74 kWh, ~319 V | Accepted |
| [0004](0004-keep-stock-transaxle.md) | Keep the stock transaxle (Tier 2 conversion) | Accepted |
| [0005](0005-low-split-battery-layout.md) | Low, split battery layout — 6 front / 8 main | Accepted |
| [0006](0006-ac-l2-charging-v1.md) | AC Level-2 charging for v1 (defer DC fast charge) | Accepted |
| [0007](0007-bms-strategy-per-stage.md) | BMS: Leaf LBC for Stage 1, simpBMS for Stage 2 | Accepted |
| [0008](0008-lightweight-gokart-spec.md) | Strip to a lightweight "electric go-kart" spec | Accepted |

## Decisions still open (future ADRs)
- DC fast charging (CCS) if road-tripping becomes a goal — supersedes part of ADR-0006.
- Final HV protection values (fuse/precharge) once the EM57 inverter spec is confirmed (PF2).
