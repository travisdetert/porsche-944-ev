# ADR-0010: Rear spare-well goes to the subwoofer (not a battery box)

**Status:** Accepted
**Date:** 2026-06-27
**Deciders:** Travis

## Context
Two decisions want the same space: ADR-0005 reserved the **rear spare-tire well** as an
*optional* battery box, and ADR-0009 added **subwoofers** that need an enclosure. They collide
in the rear of the car. Crucially, the committed Stage-2 pack (**14 modules / 74 kWh**) already
fits the **two main boxes** (6 front / 8 main) — the rear well was only ever *optional
expansion beyond_ that. So this costs the range plan nothing.

## Decision
Allocate the **rear spare-well to the subwoofer enclosure.** The traction battery stays in the
**two main boxes** (front bay + fuel-tank bay); no rear battery box.

## Alternatives considered
- **Rear-well battery box** — rejected: the extra ~2 modules of range aren't needed for a
  grocery-getter, and the subs are the priority (ADR-0009).
- **Split the well between subs and a small box** — rejected: compromises both — poor
  enclosure volume *and* a token battery gain.

## Consequences
- **Positive:** great low-rear bass location; **simpler 2-box pack**; no rear-battery weight
  pushing the balance past the ~48% front target; the 74 kWh plan is unaffected.
- **Negative / accepted cost:** forgoes rear expansion room — if a future build ever wants
  >74 kWh, this would need revisiting. The aux 12 V audio battery also lives in the rear.
- **Follow-ups:** aux 12 V audio battery placement; sub-enclosure build; `944-layout-design.md`
  and `parts-list.md` updated.
