# 944 EV — Module Placement: HV & Leaf (high-voltage) Paths

Companion to `docs/module-placement-map.md` (the low-voltage HyPer9-std / Path B map).
Both higher-voltage paths land on **14 Tesla modules ≈ 74 kWh**, but with **different
topologies** because the controller voltage windows differ. Higher voltage buys range
and worst-case margin, at the cost of ~250 lb and ~$2.8k more modules than Path B.

> Masses pressure-tested against reference figures (not live-searched this session).
> Confidence flagged.

---

## Two topologies, same 14 modules / 74 kWh

| Path | Controller | Topology | Voltage | Strings |
|---|---|---|---|---|
| **HV** | HyPer9 HV + AC-X144 | **7S2P** | 160 V nom | two strings of 7 |
| **Leaf** | EM57 + Leaf inverter + ZombieVerter | **14S1P** | 319 V nom | one string of 14 |

- **7S2P (HV):** like Path B's 5S2P but with 7 — each parallel string drops into one box.
  Needs **per-string fuses**; keep strings capacity-matched before paralleling.
- **14S1P (Leaf):** one long series chain, full pack voltage (319 V). No parallel
  matching, but **everything is HV-rated** and the series link between boxes crosses the
  tunnel once. The Leaf inverter likes ~350 V, so 14S is near its happy zone (16S → 365 V
  / 85 kWh is the max-range option, +~120 lb).

---

## Placement map (numbered, 7 front / 7 main)

```
        FRONT AXLE                                          REAR AXLE
            │                                                   │
   ┌────────┼───────────────────────────────────────────────────┼────────┐
   │ DC-DC, │  [== MOTOR ==]  ┌───────────────┐  ░tube░ ┌───────────────┐  │
   │ charger│   +adapter      │ FRONT BOX     │        │ MAIN BOX       │  │
   │ ZVerter│                 │ M1 M2 M3 M4   │        │ M8  M9 M10 M11 │  │
   │ nose   │                 │ M5 M6 M7      │        │ M12 M13 M14    │  │
   │ ───────┼─────────────────┴───────────────┴────────┴───────────────┴──┤
   │        │            all modules LOW in floor          stock transaxle │
   └────────┼───────────────────────────────────────────────────┼────────┘
        ~49% front                                          ~51% rear
```

### HV path — 7S2P series/parallel routing
```
   STRING A (front box)              STRING B (main box)
   M1+→M2→M3→M4→M5→M6→M7−            M8+→M9→…→M14−
     │  7S = 160V                     │  7S = 160V
     └───[string fuse]──┐     ┌───[string fuse]──┘
                        ▼     ▼
                 HV JUNCTION (parallel, 2P) ─ 160V, 2×232Ah
                        │ MSD → main fuse → contactors → AC-X144
```

### Leaf path — 14S1P single-string routing
```
   FRONT BOX                          MAIN BOX
   M1+→M2→…→M7 ───[series link        ──→ M8→M9→…→M14−
                  crosses tunnel]
   one continuous 14S chain = 319V, 232Ah
        │ MSD → main fuse → contactors → Leaf inverter (ZombieVerter VCU)
   (no parallel junction; BMS taps all 14 module junctions; full HV throughout)
```

---

## Balance recompute (14 modules ≈ 880 lb pack)

Subtotal before battery is ~the same as Path B (motor mass differs by ≤20 lb between
HyPer9-HV ~150 lb and Leaf EM57+inverter ~170 lb — negligible vs. the battery swing):
**≈ 1,306 lb front / 1,319 lb rear (2,625 lb, 49.8 %F).**

| Battery split | Mass | ΔFront | ΔRear |
|---|---|---|---|
| 7 modules front box (440 lb @65%F) | +440 | +286 | +154 |
| 7 modules main box (440 lb @30%F) | +440 | +132 | +308 |
| **Final — converted 944 (HV/Leaf)** | **3,505 lb** | **1,724** | **1,781** |

**Result: ~3,505 lb (+605 over stock), 49.2 / 50.8 front/rear.** Same balance as Path B,
**~250 lb heavier** (more brake/suspension demand). Trim with 8/6 → ~49.8 %F (true-ish
50/50) or 6/8 (+hatch) → more rear bias.

---

## Cabling & current — the upside of going high-voltage
Higher voltage = **lower current for the same power** = thinner cable, smaller lugs,
less I²R loss than Path B's 114 V / ~790 A:

| Path | Voltage | ~Peak power | ~Peak current | Cable |
|---|---|---|---|---|
| Path B (HyPer9-std) | 114 V | 90 kW | **~790 A** | 2/0–4/0 |
| HV (HyPer9-HV) | 160 V | 88 kW | **~550 A** | 1/0–2/0 |
| Leaf (EM57) | 319 V | ~110 kW | **~345 A** | 2 AWG |

The Leaf path's 319 V makes the cleanest HV wiring — but full-pack HV everywhere demands
strict isolation discipline and a single well-managed series string.

---

## Path comparison (so the choice is concrete)

| | **Path B — HyPer9-std** | **HV — HyPer9-HV** | **Leaf — EM57** |
|---|---|---|---|
| Modules / topology | 10 · 5S2P | 14 · 7S2P | 14 · 14S1P |
| Pack | 53 kWh @ 114 V | 74 kWh @ 160 V | 74 kWh @ 319 V |
| Range @300 / worst-case 343 | 159 / 139 mi | **222 / 194 mi** | **222 / 194 mi** |
| Curb weight | **3,255 lb** | 3,505 lb | 3,505 lb |
| Front balance | 49.3 %F | 49.2 %F | 49.2 %F |
| Peak current / cable | 790 A / fat | 550 A / med | **345 A / thin** |
| Motor+controls cost | $5.4k (kit) | ~$5.6k (kit) | **~$0.9–1.4k** (salvage+ZVerter) |
| +4 modules cost | — | ~+$2.8k | ~+$2.8k |
| Fab difficulty | low (bolt-on) | low (bolt-on) | **higher** (EM57 shaft adapt + self-integrate) |

### Read
- **Want the lightest, simplest, cheapest-to-integrate 150-mi car:** **Path B.** Accepts
  a thinner worst-case margin and fat cables.
- **Want big range + guaranteed worst-case margin, still bolt-on:** **HV path** (+$2.8k,
  +250 lb).
- **Want lowest parts cost and cleanest HV wiring, accept fabrication:** **Leaf path** —
  the motor+controls are ~$4.5k cheaper than the kits, offsetting the extra modules, but
  you fabricate the EM57 adapter and integrate the inverter yourself.

## Verify later (same as Path B)
- 944 engine dressed weight (~400 lb) — confirm on removal; biggest swing on pre-battery balance.
- Corner-scale the finished car (Phase 7); move 1–2 modules to trim.
- Leaf 14S1P: validate the Leaf inverter runs happily at 319 V with ZombieVerter for your
  target power before committing the full module count.
