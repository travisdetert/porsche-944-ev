# Parts Inventory — the full ledger

Every significant part and its disposition, in one place. The strip list, reuse map, and BOMs
are the detail; **this is the master ledger** — update the **Status** as parts actually move.

**Status legend:** 🔴 REMOVED→SOLD · ⚪ REMOVED→strip/scrap · 🟢 KEPT (944) · 🔵 REUSED (Leaf) · 🟠 NEW (bought)

## Money rollup (the bottom line)
| Flow | Items | $ |
|---|---|---|
| **Income** | gas parts sold + stripped comfort parts | **+$600 – 1,900** |
| **Donor** | one salvage Leaf (yields all 🔵) | −$2,500 – 4,500 |
| **New parts** | all 🟠 (excl. one-time PPE) | −$1,000 – 1,500 |
| **PPE / tools** | one-time, reusable | −$300 – 600 |
| **Net to driving** | | **≈ $2.5 – 5k** |

---

## 🔴 REMOVED → SOLD  (the gas parts that fund the build)
| Part | Disposition | ~Value |
|---|---|---|
| 2.5L engine (core/running) | sell | $300–800 |
| DME/Motronic ECU | sell | $100–300 |
| Intake (airbox, AFM, throttle body, manifold) | sell | $50–150 |
| Exhaust + catalytic converter | sell | $80–250 |
| Fuel system (tank, pump, injectors, rail) | sell | $50–150 |
| Alternator · starter · A/C compressor · PS pump | sell | $80–250 |
| Ignition (coil, dist, plugs, wires) | sell | $20–80 |
| **Subtotal income** | | **+$500–1,500** |

## ⚪ REMOVED → strip / scrap  (go-kart cut + ICE leftovers)
| Part | Disposition | Note |
|---|---|---|
| A/C system (condenser, evaporator, dryer, lines) | sell/scrap | go-kart cut (ADR-0008) |
| Carpet · sound deadening · rear seats · extra trim | sell/scrap | ~+$100–400 if sold |
| Spare tire + jack | store/sell | frees rear well for subs |
| Engine mounts, brackets, partial engine harness | scrap/recycle | — |
| Engine coolant hoses, thermostat housing | scrap | radiator is **kept** (🟢) |

## 🟢 KEPT from the 944  (the great mechanicals — $0)
Transaxle + differential · torque tube + driveshaft · half-shafts + hubs · wheels/tires ·
**brakes** · **suspension** (incl. rear torsion bars) · steering rack · chassis / body / glass ·
doors · driver seat + belts · lights · wipers/washer · horn · HVAC ducting + blower ·
instruments (repurposed) · **radiator + fans** (repurposed to cool the inverter/motor).

## 🔵 REUSED from the donor Leaf  (the entire HV powertrain — one donor)
| Part | Into the build |
|---|---|
| EM57 motor | drive motor |
| Inverter | driven by ZombieVerter |
| PDM (onboard charger + DC-DC) | AC charging + 12 V supply |
| Traction battery | Stage-1 pack |
| LBC | Stage-1 BMS |
| Accelerator pedal | throttle input |
| Charge port + J1772 inlet | charging (in old fuel door) |
| HV contactors · pack fuse · HV cable | HV junction (Stage 1) |
| Coolant pump · CAN harness bits | cooling + comms |

## 🟠 NEW — purchased  (the only genuinely new parts)
| Part | $ | Note |
|---|---|---|
| ZombieVerter VCU | $380 | the only new electronics "brain" |
| CAN→gauge adapter (ESP32 + transceiver) | $20–50 | reuses the 944 cluster (ADR-0012) |
| Control computer (Pi + CAN HAT + 7" touch + GPS + UPS) | $150–300 | optional head unit: telemetry/maps/drive modes (ADR-0014; app in `app/`) |
| Adapter plate + coupler (machined) | $520–860 | the only new fabrication |
| HV safety extras (DC fuse/MSD if not reused, lugs, crimper, loom) | $150–400 | size to inverter (PF2) |
| Motor-mount stock + fasteners | $60–150 | |
| Electric vacuum pump (brakes) | $80–200 | replaces engine vacuum |
| Electric hydraulic PS pump (EHPS, salvage) | $80–300 | retains power steering (ADR-0013); ~20–50 A 12 V |
| D/N/R selector switch | $10–40 | electronic reverse (`control-wiring.md`) |
| PTC defroster | $80–300 | required for defrost/registration |
| 12 V battery + aux audio battery | $160–350 | LV + audio |
| Stereo: head unit, amp, subs, speakers | $500–1,400 | ADR-0009 (taste) |
| Enclosure stock + skid plate | $170–450 | aluminum, light (ADR-0011) |
| Consumables (sealant, heat-shrink, ties) | $50–100 | |
| **PPE/tools (one-time):** gloves, DC meter, megger, extinguisher | $300–600 | reusable forever |

---

## Stage 2 (later) — the range swap
| Part | Status | $ |
|---|---|---|
| 14× Tesla 5.3 kWh modules | 🟠 NEW | ~$9,700 |
| simpBMS | 🟠 NEW | $150–300 |
| Leaf traction battery + LBC | retire/sell | recover some $ |

> Detail: `strip-list.md` (removed) · `power-and-reuse-diagrams.md` (reuse map) ·
> `parts-list.md` + `parts-shopping-list.md` (buy) · `procurement-plan.md` (schedule).
