# Specific Parts — the actual make/model shopping list

The category BOM (`parts-list.md`) says *what*; this says **which** — the specific
community-standard parts to buy. Organized to be shoppable.

> ⚠️ **Confirm before buying.** These are knowledge-based picks (not live-checked this
> session). Verify current **price / stock / exact part number** with the vendor, and **size
> the fuse + precharge to your EM57 inverter** (Pre-Flight PF2). Treat exact P/Ns as
> "confirm," not gospel.

---

## A. Drivetrain & control
| Need | Specific pick | Vendor | ~$ | Note |
|---|---|---|---|---|
| Motor + inverter | **Nissan Leaf EM57 + its inverter** | donor (salvage) | [donor] | 2013–2017 gen — PF1 |
| VCU | **ZombieVerter VCU** | evbmw.com | $380 (350 €) | bare board; "Built" = 750 € |
| BMS — Stage 1 | **reuse Leaf LBC** (read by ZombieVerter) | donor | [donor] | no new BMS yet |
| BMS — Stage 2 | **simpBMS** (Tesla-module open-source) | openinverter / DIYsell | $150–300 | or **Orion BMS 2** (commercial, ~$900) |
| Throttle | **reuse donor Leaf accelerator pedal** (Hall) | donor | [donor] | → ZombieVerter analog in |

## B. HV safety / contactors / protection
| Need | Specific pick | Vendor | ~$ | Note |
|---|---|---|---|---|
| Main contactor | **TE/Tyco EV200** (EV200HAANA) | Mouser/DigiKey | $150–250 | 500 A, 12–900 VDC, economizer coil |
| — alt | **Gigavac GV200 / GX11** | EV West / Mouser | $150–250 | equivalent |
| Precharge contactor | **Gigavac GH12** (or small TE relay) | Mouser | $40–90 | |
| Precharge resistor | **~100 Ω / 100 W wirewound** (Ohmite/Vishay) | Mouser/DigiKey | $10–30 | confirm value vs inverter caps (PF2) |
| Main HV fuse | **Bussmann FWP-xxxA22F** (e.g. ~250 A / 700 VDC) | DigiKey/Mouser | $40–90 | **DC-rated**; size to inverter (PF2) |
| — alt | **Mersen/Ferraz HP** series | — | — | |
| Fuse holder | DC-rated for the FWP body | Mouser | $15–40 | |
| MSD (service disconnect) | **reuse donor Leaf MSD**, or TE HVIL disconnect | donor / Mouser | $0–150 | your lockout |
| Current sensor | **LEM HASS / DHAB**, or reuse donor | Mouser | $0–60 | for VCU/BMS |
| Crash switch | inertia switch (Ford-style) | Amazon/auto | $20–40 | in contactor-coil circuit |

## C. Cabling & terminations
| Need | Specific pick | Vendor | ~$ | Note |
|---|---|---|---|---|
| HV cable | **2/0 AWG flexible welding cable** (Class K, 600 V) | welding supply | $5–8/ft | ~20 ft |
| Lugs | **tinned copper lugs** (Selterm/Temco), 2/0 | Amazon | $40–80 | |
| Crimper | **16-ton hydraulic lug crimper** (Temco/iCrimp) | Amazon | $40–120 | one-time tool |
| Heat-shrink | **adhesive-lined, ≥600 V** (3:1) | Amazon | $20–40 | |
| HV loom | **orange convoluted split loom** | Amazon | $20–40 | HV ID |

## D. Power conversion & charging
| Need | Specific pick | Vendor | ~$ | Note |
|---|---|---|---|---|
| Charger + DC-DC | **reuse Leaf PDM** (OBC + DC-DC) | donor | [donor] | ZombieVerter drives it |
| — charger alt | **Thunderstruck TSM2500** or **TC/Elcon** | Thunderstruck-EV | $500–900 | if not reusing PDM |
| — DC-DC alt | **Meanwell / TDK-Lambda HV→12 V, ~30 A** | DigiKey | $150–300 | |
| Charge inlet | **J1772 inlet** (reuse Leaf port) | donor | $0–120 | mount in fuel-filler door |

## E. Mechanical
| Need | Specific pick | Vendor | ~$ | Note |
|---|---|---|---|---|
| Adapter plate | **custom-machined** (your drawing) | local machine shop | $320–500 | no off-the-shelf 944 part |
| Coupler/hub | **EV Coupler Connection** machined hub, or custom | evcouplerconnection.com | $200–360 | EM57 output → driveshaft |
| Motor mount | **steel plate/tube + poly mounts** to crossmember | local | $60–150 | factory hardpoints |

## F. Re-source (jobs the engine did)
| Need | Specific pick | Vendor | ~$ | Note |
|---|---|---|---|---|
| Brake vacuum | **Hella UP30 vacuum pump** + reservoir + check valve + vac switch | Amazon/auto | $80–200 | electric boost |
| — alt | Bosch **iBooster** (salvage) | salvage | $150–400 | more complex |
| Cabin defrost | **PTC coolant heater** (salvage Volt/Leaf), or aftermarket HV heater | salvage | $80–300 | **required for defrost/registration** |

## G. Battery
| Need | Specific pick | Vendor | ~$ | Note |
|---|---|---|---|---|
| Stage 1 pack | **donor Leaf pack** (24–40 kWh) | donor | [donor] | small modules fit easily |
| Stage 2 modules | **Tesla Model S/X 5.3 kWh** ×14 | **ampREVOLT** ($690), EV West, Stealth EV, Inductive, EVTV | ~$9.7k | ~2× vendor spread — shop it |

## H. Audio (taste — pick to preference)
| Need | Specific pick (example) | ~$ | Note |
|---|---|---|---|
| Head unit | any modern BT unit | $100–300 | |
| Sub amp | **mono class-D** (JL Audio / Rockford / Skar) | $150–400 | |
| Subs | dual 10"/12" in the **rear-well enclosure** (ADR-0010) | $150–400 | |
| Component speakers (front) | your pick | $100–300 | |
| Aux 12 V audio battery | **XS Power** AGM + stiffening cap | $80–200 | bass peaks (ADR-0009) |

## I. Safety / PPE (one-time, reusable)
| Need | Specific pick | ~$ | Note |
|---|---|---|---|
| HV gloves | **Class 0 (1000 V)** Cementex/Salisbury + leather overgloves | $80–150 | inspect for pinholes |
| DC meter | **Fluke 117 / 87V** (CAT III, ≥600 V) | $200–400 | live-dead-live |
| Insulation tester | **Fluke 1507** (or budget megger) | $100–400 | pre-power-up isolation |
| Extinguisher | **DC-rated / CO₂ or ABC** | $40–80 | first power-up |

---

## Where to buy (vendor cheat-sheet)
- **EV-specific:** EV West · ampREVOLT · Thunderstruck EV · EVTV · Stealth EV · Inductive Autoworks · evbmw.com (ZombieVerter) · openinverter shop
- **Electronics:** DigiKey · Mouser (contactors, fuses, resistors, sensors)
- **Generic/tools:** Amazon · local welding supply (cable) · local machine shop (adapter)

> Confirm live prices + stock when the search budget resets — I can turn this into a
> link-by-link cart then. Sizing detail: `hv-bom.md`. Schedule + cash flow: `procurement-plan.md`.
