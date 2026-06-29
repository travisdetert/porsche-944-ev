# MVP Sourcing — vetted parts to make the 944 move electrically (Stage 1)

Goal: the **cheapest, lowest-effort, compatibility-safe** path to a driving grocery-mule EV 944.
Prices are **estimates** (2026) — listings expire, so search URLs are given alongside examples.

## The strategy that removes the compatibility risk
**Buy ONE Gen-2 (2018+, 40 kWh "ZE1") salvage Leaf as the donor.** One car gives a **matched,
same-generation set**: EM57 motor + inverter + PDM (charger + DC-DC) + LBC (BMS) + HV pack +
pedal + J1772 charge port. Piecing these from separate sellers is where compatibility goes wrong.

**Why Gen-2 specifically (the PF1 answer):** the ZombieVerter VCU supports the Leaf **inverter+motor**
on Gen1/2/3, but the **charger/DC-DC (PDM) only on Gen2/Gen3**. A Gen-2 donor → reuse the charger
(ADR-0006) with **no extra parts**. A Gen-1 donor → you must add a separate charger + DC-DC.
Source: openinverter wiki.

## The MVP buy list
| # | Item | Where (search + example) | ~$ | Compatibility / vetting |
|---|---|---|---|---|
| 1 | **Donor: 2018+ Leaf 40 kWh (ZE1), salvage** | [Copart](https://www.copart.com/vehicle-search-model/nissan/leaf) · [eRepairables](https://erepairables.com/salvage-cars-auction/nissan/leaf) · [IAAI / car-part.com] | ~4,500–6,500 | Confirm **2018+ ZE1, 40 kWh**. **Check pack SOH with LeafSpy** before bidding (G1). Includes motor+inverter+PDM+LBC+pack — the bulk of the EV. |
| 2 | **ZombieVerter VCU (built)** | [EVBMW webshop](https://www.evbmw.com/index.php/evbmw-webshop/vcu-boards/zombieverter-vcu-built) · [setup wiki](https://openinverter.org/wiki/Nissan_Leaf_VCU) | ~810 (€750) | The brain. No-solder built version; ~4 wk lead. Drives the Gen2 inverter+PDM over CAN. |
| 3 | **Adapter plate + coupler** (Leaf motor → 944 transaxle) | [BRAT plate](https://bratindustries.net/product/leaf-adapter-plate/) · [BRAT coupler](https://bratindustries.net/product/nissan-leaf-motor-coupler/) · [EVcreate flanged coupler](https://www.evcreate.com/shop/drivetrain/flanged-nissan-leaf-motor-coupler/) | ~250–500 +machining | The one precision part (G2). Coupler uses the **944 clutch-disc splines**; plate adapts to the 944 bellhousing — see `cad/adapter-spec.md`. |
| 4 | **HV small parts** (mostly reuse donor) | donor PDM/junction box; [eBay HV fuse/contactor] | ~250–400 | Main HV fuse, contactors (reuse Leaf's), service disconnect, HV cable/lugs, precharge resistor. |
| 5 | **Head unit** | `docs/headunit-bom.md` (Pi 5 + 7″ double-DIN touch + CAN HAT + power) | ~290 | Reads the same CAN bus; non-safety (ADR-0014). |
| 6 | **Mounts / misc** | local steel, coolant, connectors | ~400 | Motor-mount steel (G3), coolant + hose, Dupont/CAN wiring. |
| | | **MVP total** | **≈ $6,500–8,000** | car owned; DIY labor |

## What you do NOT need for the MVP (saves money)
- **No new battery** — the donor's 40 kWh pack *is* Stage-1 (≈120 mi, ADR-0002). Tesla pack is Stage-2.
- **No separate charger/DC-DC** — reused from the Gen-2 PDM (that's the whole point of picking Gen-2).
- **No new amp** — your Kicker powered sub has its own (ADR-0010/0016).
- **No DCFC** — AC L2 only for v1 (ADR-0006/0015).

## Vetting checklist for ANY donor/motor listing (paste me a link and I'll grade it)
1. **Generation** — 2018+ ZE1 40 kWh (ideal) · 2011–17 Gen1 = motor+inverter only (no PDM support).
2. **What's included** — motor **and** inverter **and** PDM **and** LBC? (A bare motor needs all of these sourced separately.)
3. **Pack SOH** — LeafSpy reading; >85% is good for Stage 1.
4. **Damage** — HV pack/components undamaged (side/rear impact = risk to pack).
5. **Price vs whole-donor** — a motor-only deal often isn't cheaper than a whole salvage car once you add inverter+PDM+pack.

Sources: [openinverter Leaf VCU wiki](https://openinverter.org/wiki/Nissan_Leaf_VCU) · [EVBMW ZombieVerter](https://www.evbmw.com/index.php/evbmw-webshop/vcu-boards/zombieverter-vcu-built) · [BRAT Industries](https://bratindustries.net/product/leaf-adapter-plate/) · [EVcreate](https://www.evcreate.com/shop/drivetrain/flanged-nissan-leaf-motor-coupler/) · [Thunderstruck-EV used Leaf drive](https://www.thunderstruck-ev.com/nissan-leaf-drive-system-used.html) · [Copart Leaf](https://www.copart.com/vehicle-search-model/nissan/leaf)
