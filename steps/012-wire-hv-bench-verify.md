# Step 012 — Wire HV + bench-verify control (G5)

**Phase:** BUILD · **Task:** #12 · **Gate:** G5 · **Cost:** (parts from 008)
**Blocked by:** 011 (pack in), 008 (parts), 003 (safety gear)
**Blocks:** 013

## Do
- [ ] Build the HV path: pack → **MSD → fuse → precharge + main contactors → inverter**.
- [ ] Crimp all 2/0 lugs (hydraulic crimper); tug-test + heat-shrink every one.
- [ ] Wire **DC-DC + charger (PDM)**, 12 V system, throttle, interlocks (BMS-healthy + crash switch).
- [ ] Configure ZombieVerter (openinverter wiki); **bench-test precharge→main + pedal at low voltage**.

## Done when
Isolation passes; control **sequences precharge→main** and reads pedal/inverter/BMS on the bench.

## Refs
`../docs/build-guide.md` §5 · `../docs/drivetrain-diagrams.md` §6 · `../docs/power-and-reuse-diagrams.md`

## Notes
- ⚠️ Build this **de-energized**. A bad crimp is a fire; verify control before the full pack is live.
