# ADR-0016: Pi head unit replaces the Pioneer; audio via Pi → amp → subs

**Status:** Accepted
**Date:** 2026-06-28
**Deciders:** Travis
**Relates to:** [ADR-0014](0014-pi-infotainment-control-app.md) (the app), [ADR-0009](0009-keep-stereo-and-subs.md) / [ADR-0010](0010-rear-well-to-subs.md) (audio)

## Context
The dash is already modified for a **standard double-DIN**, and there's an existing **Pioneer
AVH-X1600DVD** on hand. Question: flash/reuse the Pioneer to run the custom head-unit app?
The AVH-X1600DVD is a **closed embedded appliance** — proprietary RTOS, no Android/browser/SDK,
no custom firmware path. It cannot run the web app. There is **one** double-DIN slot, so the
screen and a separate stereo can't both live in it.

## Decision
**Remove the Pioneer.** Put a **Raspberry Pi + 7″ double-DIN capacitive touchscreen** in the slot
as the head unit (runs the app per ADR-0014). Because the Pi has no power amplifier, route
**Pi audio → USB DAC (or Bluetooth) → a compact 4-channel class-D amp → the subwoofers**
(ADR-0009/0010). The Pioneer is kept as a spare / resold — not flashed, not wired in.

## Alternatives considered
- **Flash the Pioneer to run the app** — rejected: closed appliance, no app platform; not possible.
- **Composite video-in (display only)** — rejected: 480i and, fatally, the Pioneer's touch can't
  drive the Pi, so the touch-first app is unusable.
- **Keep the Pioneer for audio, mount the Pi screen elsewhere** — rejected: only one double-DIN
  aperture and no clean second-screen location.

## Consequences
- **Positive:** one integrated unit, full control of the UI, app-native on the Pi; audio still
  hits the subs via a cheap amp.
- **Negative / accepted cost:** adds a **4-ch amp (~$40–70) + USB DAC (~$10)** to the BOM; the
  Pioneer is removed (no DVD/CD — acceptable for an EV go-kart build); Pi 5 has no 3.5 mm jack so
  a USB DAC or BT link is required.
- **Follow-ups:** confirm amp fit/power tap behind the dash; pick a USB DAC with clean line-out;
  `docs/headunit-bom.md` carries the audio line items.
