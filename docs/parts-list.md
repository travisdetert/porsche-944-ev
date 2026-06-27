# Parts List (BOM) — Stage 1 Mule

The realistic, line-item list to get the 944 driving. **[DONOR]** = comes from the salvage
Leaf (no incremental cost — included in the donor price). **BUY** = purchase new/separately.
Prices are typical 2026 ranges; the verified ones are flagged. Stage-2 (Tesla pack) is listed
separately and is **not** in the Stage-1 total.

> The honest takeaway: the drivetrain is cheap because the donor gives it to you. **The cost
> is the long tail** — HV bits, enclosure stock, tools, and the sort phase. Itemized, Stage-1
> all-in lands **~$6–7.5k gross / ~$5–6.5k net** after selling the gas parts.

---

## A. Donor-sourced (one salvage Leaf, ~$2,500–4,500 — counts once)
| Part | Use | Cost |
|---|---|---|
| EM57 motor | drive motor | [DONOR] |
| Inverter | drives EM57 (commanded by ZombieVerter) | [DONOR] |
| PDM (onboard charger + DC-DC) | AC charging + 12 V supply | [DONOR] |
| Traction battery | **Stage-1 pack** | [DONOR] |
| LBC (battery controller) | Stage-1 BMS | [DONOR] |
| Accelerator pedal | throttle input | [DONOR] |
| Charge port + J1772 inlet | charging (mount in old fuel door) | [DONOR] |
| HV cables, coolant pump, contactors (if undamaged) | reuse | [DONOR] |
| **Donor subtotal** | | **$2,500–4,500** |

## B. Control & HV electrical (BUY) — see `hv-bom.md` for sizing
| Part | Qty | Cost | Note |
|---|---|---|---|
| ZombieVerter VCU | 1 | **$380** | 350 EUR bare — *verified* |
| Main contactor (EV200 / GV200) | 1 | $120–250 | or reuse donor |
| Precharge contactor + resistor | 1 | $40–80 | |
| Main HV fuse (DC-rated, ~250–300 A / 500 V) | 1 | $40–90 | **DC-rated only** |
| Manual service disconnect (MSD) | 1 | $50–150 | or reuse donor |
| Inertia / crash switch | 1 | $20–40 | in contactor-coil circuit |
| 2/0 welding cable | ~20 ft | $100–160 | |
| Lugs + adhesive heat-shrink | set | $40–80 | |
| Hydraulic crimper (tool, one-time) | 1 | $40–120 | a bad crimp = a fire |
| Orange convoluted loom | roll | $20–40 | HV ID |
| HV current sensor | 1 | $0–60 | or reuse donor |
| 12 V coil supply, relays, flyback diode, fuse block | set | $40–80 | |
| **Subtotal** | | **~$900–1,200** | |

## C. Mechanical (BUY)
| Part | Qty | Cost | Note |
|---|---|---|---|
| Adapter plate (machined) | 1 | $320–500 | custom — the critical-path item |
| Coupler / hub (machined) | 1 | $200–360 | EM57 output → driveshaft |
| Motor-mount stock + brackets + fasteners | set | $60–150 | to factory hardpoints |
| Coolant hoses + small radiator (or reuse) + coolant | set | $80–200 | inverter/motor loop |
| **Subtotal** | | **~$650–1,200** | |

## D. Battery enclosure & mounting (BUY)
| Part | Qty | Cost | Note |
|---|---|---|---|
| Steel/aluminum sheet + angle (2 boxes) | — | $120–300 | front + main box |
| Mounting hardware, threaded inserts | — | $40–100 | to frame rails, not sheetmetal |
| Vents + seals | — | $30–80 | sealed, vented |
| Skid-plate stock | — | $50–150 | strike protection |
| **Subtotal** | | **~$240–630** | |

## E. Low-voltage & control (BUY)
| Part | Qty | Cost | Note |
|---|---|---|---|
| 12 V battery (small AGM) | 1 | $80–150 | LV/control side |
| Wiring, fuse block, relays, connectors | set | $60–150 | |
| Electric vacuum pump (brake booster) | 1 | $80–150 | no engine vacuum anymore |
| SOC/voltage display | 1 | $0–100 | ZombieVerter can output, or cheap CAN gauge |
| **Subtotal** | | **~$220–550** | |

## F. Safety / PPE (BUY — one-time, reusable forever)
| Part | Cost |
|---|---|
| Class-0 (1000 V) gloves + leather overgloves | $80–150 |
| CAT III DC multimeter (≥600 V) | $40–120 |
| Insulation tester (megger) | $60–150 |
| DC-rated fire extinguisher | $40–80 |
| Insulated tool set | $40–100 |
| **Subtotal** | **~$260–600** |

## G. Consumables (BUY)
Penetrating oil, sealant, dielectric grease, zip ties, heat-shrink assortment, fasteners —
**~$50–100**.

## H. Sort phase (BUY — M5)
| Part | Cost | Note |
|---|---|---|
| Uprated springs/dampers (or torsion-bar adjust) | $300–700 | for the added ~575 lb |
| Brake refresh (pads/fluid) | $80–200 | |
| **Subtotal** | **~$380–900** | |

---

## Stage-1 totals
| Bucket | Range |
|---|---|
| Donor (A) | $2,500–4,500 |
| Buy-new (B–H) | $2,700–4,800 |
| **Gross all-in** | **~$5,200–9,300** (mid ~$6.5–7k) |
| − Gas-parts resale | −$500–1,500 |
| **Net all-in** | **~$4,500–8,000** (realistic mid **~$5.5–6.5k**) |

**Cheapest realistic path** (cheap donor, own some tools, defer the sort phase): **~$4–5k net.**
The "core to driving" (A + B + C, skipping PPE/sort if you have gear) is the **$3.5–5.5k**
headline; the **all-in** is higher because of the long tail — be honest with yourself about it.

---

## Audio system (chosen indulgence — ADR-0009; not in the core driving total)
| Part | ~Cost | Note |
|---|---|---|
| Head unit | $100–300 | |
| Amplifier | $150–400 | |
| Component speakers (front) | $100–300 | |
| Subwoofer(s) + enclosure | $150–400 | rear spare-well (ADR-0010) |
| Aux 12 V audio battery + stiffening cap | $50–200 | so bass peaks don't sag the system |
| Wiring / localized deadening / install | $50–150 | |
| **Audio subtotal** | **~$600–1,750** | powered off the DC-DC — **size it for the amp**; adds ~45 lb |

## Stage 2 — the range upgrade (NOT in Stage-1 total; buy later)
| Part | Qty | Cost | Note |
|---|---|---|---|
| Tesla 5.3 kWh modules | 14 | **~$9,660** | @ $690/ea cheapest vendor — *verified*, ~2× spread |
| simpBMS | 1 | $150–400 | replaces the Leaf LBC for Tesla modules |
| (Contactors, cable, MSD, enclosures) | — | carry over | reused from Stage 1 |
| **Stage-2 add** | | **~$9.8–10.5k** | for ~150 mi — `adr/0003` |

> Schedule + cash flow: `procurement-plan.md`. HV sizing detail: `hv-bom.md`.
> Donor selection: `phase1-donor-hunt.md`.
