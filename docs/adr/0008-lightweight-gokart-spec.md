# ADR-0008: Strip to a lightweight "electric go-kart" spec

**Status:** Accepted
**Date:** 2026-06-26
**Deciders:** Travis

## Context
The project's spirit is cheap, raw, and fun — *"a big RC car you can sit in."* Comfort systems
(A/C, audio, sound deadening, rear seats, extra trim) add weight, cost, and wiring complexity,
and A/C adds parasitic load. The battery adds ~480–880 lb; stripping comfort gear claws much of
that back and sharpens the go-kart character.

## Decision
We will strip the 944 to a **lightweight go-kart spec**: delete **A/C, audio/infotainment,
sound deadening + carpet, rear seats, and non-essential trim**, keeping only the **street-legal
minimum** (lights, brakes, electric defroster, wipers, driver seat + belt, mirrors, horn) for
public-road grocery use.

## Alternatives considered
- **Keep the creature comforts** — rejected: weight, cost, wiring complexity, and parasitic
  A/C load, all against the raw go-kart ethos.
- **Full bare race-car strip (no street equipment)** — rejected *for now*: we still want
  grocery runs on public roads, so the street-legal minimum stays. Revisit if the car becomes
  private-track / off-road only.

## Consequences
- **Positive:** ~150–250 lb lighter; the **Stage-1 mule lands ≈ stock weight** with a lower CG;
  simpler wiring; more parts to sell (funds the donor); more go-kart feel.
- **Negative / accepted cost:** no A/C, spartan interior; an **electric defroster is still
  required** (legal/safety) and must be re-sourced; reversible later if comfort is wanted.
- **Follow-ups:** electric coolant/PTC defroster (`strip-list.md` re-source list); confirm the
  state's street-legal minimum (ties to ADR-0006 / registration).
