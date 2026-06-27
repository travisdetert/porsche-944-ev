# ADR-0009: Keep a real stereo + subwoofers (supersedes the audio delete in ADR-0008)

**Status:** Accepted
**Date:** 2026-06-26
**Deciders:** Travis

## Context
ADR-0008 stripped the car to a lightweight go-kart spec and deleted the audio. On reflection,
**a solid stereo with subwoofers is a must-have** for this build's enjoyment — the one comfort
that earns its weight. EVs are near-silent, which actually makes good audio *more* worthwhile.

## Decision
We will **keep and upgrade the audio** — a proper head unit, amplifier, speakers, and
**subwoofer(s)** — superseding the audio-deletion clause of ADR-0008. The rest of the go-kart
strip (A/C, rear seats, most sound deadening, non-essential trim) **still stands**.

## Alternatives considered
- **Stay fully stripped (ADR-0008 as written)** — rejected: the owner wants great sound; it's
  the indulgence worth its weight.
- **Bring A/C and full comfort back too** — rejected: *only* audio returns; the go-kart ethos
  otherwise holds.

## Consequences
- **Positive:** the car is light and raw *and* sounds great — and a quiet EV shows off a good
  system. Weight cost is small (~30–50 lb).
- **Negative / accepted cost:** ~30–50 lb back; the **12 V / DC-DC must carry the amp's current**
  (bass peaks) — plan a **stiffening cap or small aux 12 V battery**; **localized sound
  deadening** around the subs adds a little weight; the **sub enclosure competes with the
  rear-well battery box** for space — one or the other.
- **Follow-ups:** size the DC-DC for the audio load; decide rear-well = subs *or* battery box;
  `strip-list.md` updated.
