# Step 009 — Machine + dry-fit the adapter (G2)

**Phase:** BUILD · **Task:** #9 · **Gate:** G2 · **Cost:** ~$520–860
**Blocked by:** 002 (shop), 007 (EM57 measured), 000 (flange measured)
**Blocks:** 010

## Do
- [ ] Hand the shop final dimensions; have them machine the **plate + splined coupler**.
- [ ] **Dry-fit** to both the EM57 output and the torque-tube bellhousing flange.
- [ ] If it doesn't seat true, send it back for the (expected) revision.

## Done when
The adapter + coupler dry-fit cleanly to **both** the motor and the bellhousing.

## Refs
`../cad/adapter-spec.md` + `../cad/adapter-plate.scad` (parametric model) ·
`../docs/build-guide.md` §2B · `../images/adapter-joint.svg`

## Notes
- This is the **one custom part** and the schedule's biggest risk — don't rush the fit.

<!-- tips-v1 -->

## Tools
- Machine shop
- Dial indicator + magnetic base
- Calipers, feeler gauges
- Engineer's square

## Time & difficulty
1–2 wks (shop) · hard

## ⚠ Safety
- Spinning driveline later depends on this being true. Measure it.

## Tips & gotchas
- **Dry-fit before final cuts.** Bolt up, then check.
- Verify **concentricity with a dial indicator — runout < 0.1 mm**; faces parallel.
- Let the **register/pilot fit** do the centering, not the bolts.
- Use the app's **🔩 Driveline** view as the visual reference for what aligns to what.

## Avoid
- Trusting bolt-hole clearance to align the shafts.
- Final-machining before a successful dry-fit.
