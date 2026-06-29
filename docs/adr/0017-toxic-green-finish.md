# ADR-0017: Final finish — "Toxic Green" (wrap-first, respray optional)

**Status:** Accepted
**Date:** 2026-06-28
**Deciders:** Travis
**Supersedes:** the "black" default in [[black-944]] note (car is currently black; planned finish is Toxic Green)

## Context
The car is currently black. The desired final look is a vivid, luminous lime — **"Toxic Green"**,
inspired by the Moog Little Phatty "Toxic" edition. Twin preview hex **`#62E32B`** (tunable). It's
**not a factory color**, so it's a custom mix or a vinyl wrap, and high-vis green needs a white
ground coat for even coverage.

## Decision
Finish the 944 in **Toxic Green**, **vinyl wrap first** (reversible, cheaper, exact-match, protects
the shell), with a **custom respray** as the later permanent option if the color earns it. Cosmetics
are a **post-MVP** milestone — finish color **after** the car drives, so it never blocks the build.
Keep **black wheels + black/dark trim** as the accent. Plan: `docs/paint-toxic-green.md`.

## Alternatives considered
- **Respray now** — rejected for v1: cost (~$4–9k) + downtime before the car even moves; do it later.
- **Keep it black** — rejected: the whole point is the Toxic Green look; black stays as a fallback swatch.
- **Other greens** (Viper/Irish/BRG) — kept as swatches in the app, but Toxic Green is the target.

## Consequences
- **Positive:** distinctive look, reversible/affordable via wrap, color decided + previewable on the twin.
- **Negative / accepted cost:** neon greens need a ground coat (more $/time); wrap lifespan ~5–7 yr;
  a true respray is a bigger later spend.
- **Follow-ups:** match `#62E32B` to a real sprayout/wrap swatch; add a cosmetic "finish" task to the
  PLAN board (parallel/after DRIVE); optional Toxic-Green logo variant.
