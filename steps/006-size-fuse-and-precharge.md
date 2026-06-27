# Step 006 — Size the fuse + precharge (PF2)

**Phase:** BUY · **Task:** #2 · **Gate:** PF2 · **Cost:** $0 (research)
**Blocked by:** 005 (know the exact inverter), or do from the wiki anytime
**Blocks:** 008 (ordering the HV fuse + precharge)

## Do
- [ ] Get the **EM57 inverter capacitor spec** (openinverter wiki / datasheet).
- [ ] Size the **precharge resistor** (RC vs the cap bank — ~100 Ω/100 W default) and the
      **DC-rated main fuse** (~250–300 A, ≥500 V) to your pack current.

## Done when
You have specific, justified fuse + precharge values to order against.

## Refs
`../docs/hv-bom.md` · `../docs/parts-shopping-list.md`

## Notes
- **Don't order the fuse/precharge until this is closed** — they're sized to *your* inverter.
- DC-rated fuse only — an AC fuse won't interrupt a DC arc.
