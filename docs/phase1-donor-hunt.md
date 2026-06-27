# Phase 1 — Donor Hunt & Sourcing Checklist

The single most leverage-rich decision in the build. **The right donor cuts your
commissioning gremlins (your biggest schedule variance) in half;** the wrong one buries
you. One salvage Nissan Leaf yields almost the entire Stage-1 powertrain — motor,
inverter, charger, DC-DC, battery, and the control bits — all factory-matched.

## What one Leaf donor gives you
| Part | Nissan name | Used for |
|---|---|---|
| Traction motor | **EM57** | the drive motor (Stage 1 + final) |
| Inverter | (atop motor) | drives the EM57 — reused, commanded by ZombieVerter |
| On-board charger + DC-DC | **PDM** | AC charging + 12 V supply |
| Traction battery | 24 / 40 / 62 kWh | **Stage-1 mule pack** (free with the donor) |
| Battery controller | **LBC** | pack BMS — readable by ZombieVerter (Stage 1) |
| Charge port + inlet | — | J1772 charging |
| Accelerator pedal | — | throttle signal into ZombieVerter |
| HV cables, coolant pump, contactors | — | reusable HV bits |

## Which Leaf to target

| Year / pack | Motor | Notes | Verdict |
|---|---|---|---|
| 2011–2012 (24 kWh) | EM61 | Older inverter, different VCU support | Avoid unless very cheap |
| **2013–2017 (24/30 kWh)** | **EM57** | Cheapest EM57 donors; well-supported by ZombieVerter | **Best value for the mule** |
| **2018+ (40/62 kWh)** | EM57 | More mule range (~100/150 mi), pricier, gen3 control | Best if you find one cheap |

**Recommendation:** a **2013–2017 EM57 car** is the sweet spot — cheapest, proven
ZombieVerter support, and even a degraded 24 kWh pack is 3–5× a grocery run. Grab a
40 kWh (2018+) only if the price is right.

> Verify current ZombieVerter/openinverter support for the exact year before buying —
> gen1/2/3 differ in CAN and PDM handling. (Couldn't live-check this session.)

## Where to find one
- **Salvage auctions:** Copart, IAAI (often need a broker/dealer for access).
- **eBay Motors** (whole cars + parted-out drivetrains), **Facebook Marketplace**, local
  **pick-n-pull** yards, EV-specific salvage sellers.
- **Forums:** openinverter, MyNissanLeaf, DIY Electric Car classifieds.

## Pre-purchase inspection checklist (bring this)
- [ ] **Crash location** away from the parts you need (see damage map below).
- [ ] No **flood/water** history (corrosion in HV connectors = walk away).
- [ ] Motor/inverter **physically intact**, connectors not sheared.
- [ ] Battery case **not breached, not swollen**, no electrolyte/coolant smell.
- [ ] **PDM** (charger/DC-DC) present and undamaged.
- [ ] Charge port, accelerator pedal, HV cables, **LBC** all present.
- [ ] Can you power up the 12 V system / read the dash? (lets you run LeafSpy)

## Battery health assessment — the most important step
Use **LeafSpy** (phone app + a cheap OBD-II BLE dongle) on the donor before buying:
- [ ] **SOH (State of Health) %** — want **> 70%** for a comfortable mule; lower is fine
      if cheap (even 60% on a 40 kWh = ~60 mi).
- [ ] **Capacity bars / "Hx" health number** — cross-check the SOH.
- [ ] **Cell-pair voltages** — should be tight; a wide spread = a weak/failing module.
- [ ] **QC (rapid) + L1/L2 charge counts** — heavy rapid-charging ages a pack faster.
- [ ] **No active battery DTCs.**
If you cannot run LeafSpy, **price the pack as if it is near end-of-life** and treat any
usable range as a bonus.

## Crash-damage map (match damage to what you don't need)
- **Front-end hit:** risks motor/inverter/PDM — *bad for us.* Inspect closely.
- **Rear/side hit:** risks the pack case — check for breach; the drivetrain is usually fine.
- **Best donor:** clean drivetrain + healthy pack; cosmetic/structural damage elsewhere.

## Price guidance & negotiation
- Reference range from earlier research: **wrecked Leafs ~$4,000–6,000**; degraded-battery
  or higher-mileage cars can be cheaper. **Budget ~$2,500–4,500.**
- **Pack health drives value.** A tired pack is a discount lever, not a dealbreaker for a
  mule (Stage 2 replaces it with Tesla modules anyway).
- Don't overpay to rush — keep 2–3 listings warm; the *right* donor beats the *first* one.

## Parts extraction map (what to pull, in order)
1. **De-energize first** (SECURITY.md): pull the donor's service disconnect, wait, verify dead.
2. Pull the **battery pack** (heavy — hoist/cart; keep it level, terminals covered).
3. Pull the **motor + inverter** assembly.
4. Pull the **PDM** (charger + DC-DC), **charge port**, **accelerator pedal**, **LBC**.
5. Save **HV cables, coolant pump, 12 V harness sections** ZombieVerter needs.
6. Label every connector as you go — photograph the harness *before* cutting.

## Order-in-parallel list (long-lead — start at Phase 1, see `hv-bom.md`)
- [ ] **ZombieVerter VCU** (evbmw.com)
- [ ] **HV safety set:** main + precharge contactors, precharge resistor, DC fuse, MSD
- [ ] **2/0 AWG HV cable, lugs, hydraulic crimper, heat-shrink, orange loom**
- [ ] **CAT III DC meter, Class-0 gloves, insulated tools** (if not already owned)

## Phase 1 = done when
- [ ] Donor bought; LeafSpy SOH recorded; price reflects pack health
- [ ] Powertrain + pack + PDM + LBC + pedal + charge port extracted and labeled
- [ ] Long-lead parts ordered (VCU + HV BOM)
- [ ] Adapter drawing out to 2 machine shops for quotes (see `build-guide.md` Phase 2)
