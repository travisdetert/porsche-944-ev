# Step 011 — Mount the pack + isolation check (G4)

**Phase:** BUILD · **Task:** #11 · **Gate:** G4 · **Cost:** ~$240–630 (enclosures)
**Blocked by:** 010 (driveline true), 007 (have the pack)
**Blocks:** 012

## Do
- [ ] Build sealed, vented **aluminum** enclosures; mount the donor pack **low, to structure**
      (front box + fuel-tank-bay box — 6/8 split, `../docs/944-layout-design.md`).
- [ ] Keep the **LBC** connected (Stage-1 BMS).
- [ ] **Megger isolation check** — HV must be isolated from chassis.

## Done when
Pack mounted low + secure, terminals covered, LBC connected, **isolation check passes**.

## Refs
`../docs/944-layout-design.md` · `../docs/low-cg-packaging.md` · `../docs/battery-fit.md`

## Notes
- Confirm the **fuel-tank-bay length vs the modules** here (the one fit risk — `battery-fit.md`).

<!-- tips-v1 -->

## Tools
- Megger / insulation tester (500–1000 V)
- Torque wrench
- Skid plate (PARTS)

## Time & difficulty
2–4 days · moderate (HV)

## ⚠ Safety
- Pass a megger isolation test before the pack ever sees the contactors.

## Tips & gotchas
- Mount **low + central** (ADR-0005) for the CG; flanges to **frame rails/floor hardpoints**.
- **Megger the pack-to-chassis isolation** — should read many MΩ; investigate anything low.
- Vent the enclosure; protect the low main box with the **skid plate**.
- Strain-relieve every HV cable; nothing rubbing or pinched.

## Avoid
- Bolting a crash load to sheetmetal.
- Skipping the isolation test 'just to see if it runs'.
