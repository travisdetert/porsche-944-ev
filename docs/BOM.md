# 📦 Master BOM — comprehensive, with sourcing links

The single shoppable list to build the Stage-1 EV 944. Consolidates `parts-shopping-list.md`
(specific picks), `hv-bom.md` (sizing), `headunit-bom.md` (Pi), `mvp-sourcing.md` (strategy).
**Links are vendor / category / search pages (stable); confirm exact product, price & stock —
they move.** `[DONOR]` = comes from the salvage Leaf at ~$0 incremental. Read `../SECURITY.md`
before anything orange.

## The strategy that makes it cheap
**One Gen-2 (2018+ ZE1 40 kWh) wrecked Leaf = a complete matched HV system** (motor, inverter,
PDM charger+DC-DC, BMS/LBC, pack, pedal, charge port). Reuse it; buy almost nothing else for HV.
The contactor/fuse/cable picks below are mostly **Stage-2** costs (when you swap to a Tesla pack).
Why Gen-2: ZombieVerter supports the Leaf inverter+motor on all gens but the **charger/PDM only on
Gen2/3** (PF1). Sell the gas parts to offset.

## A. Drivetrain & control
| Part | Source | ~$ | Note |
|---|---|---|---|
| Nissan Leaf **EM57 motor + inverter** | [Copart](https://www.copart.com/vehicle-search-model/nissan/leaf) · [eRepairables](https://erepairables.com/salvage-cars-auction/nissan/leaf) · [Car-Part](https://www.car-part.com) | [DONOR] | 2018+ ZE1 (PF1) |
| **ZombieVerter VCU** (built) | [EVBMW shop](https://www.evbmw.com/index.php/evbmw-webshop/vcu-boards/zombieverter-vcu-built) · [setup wiki](https://openinverter.org/wiki/Nissan_Leaf_VCU) | $380–810 | the brain |
| BMS Stage 1 — **reuse Leaf LBC** | donor (read by ZombieVerter) | [DONOR] | no new BMS |
| BMS Stage 2 — **simpBMS** / Orion 2 | [openinverter](https://openinverter.org) · [Orion](https://www.orionbms.com) | $150–900 | Tesla pack only |
| Accelerator — **reuse Leaf pedal** | donor (dual-Hall → VCU) | [DONOR] | fault-safe |

## B. HV safety / contactors / protection  (mostly [DONOR] in Stage 1 — reuse the Leaf junction box)
| Part | Source | ~$ | Note |
|---|---|---|---|
| Main contactor **TE EV200** / Gigavac GV200 | [Mouser EV200](https://www.mouser.com/c/?q=EV200) · [EV West](https://www.evwest.com) | $150–250 | or [DONOR] |
| Precharge contactor **Gigavac GH12** | [Mouser](https://www.mouser.com/c/?q=GIGAVAC%20GH12) | $40–90 | |
| Precharge resistor **~100 Ω / 100 W** | [DigiKey](https://www.digikey.com/en/products/filter/resistors) | $10–30 | size to caps (PF2) |
| Main HV fuse **Bussmann FWP**, DC-rated | [DigiKey FWP](https://www.digikey.com/en/products/result?keywords=FWP%20fuse) · [Mouser](https://www.mouser.com/c/?q=bussmann%20FWP) | $40–90 | size to inverter (PF2) |
| Service disconnect (MSD) | [DONOR] / [TE @ Mouser](https://www.mouser.com) | $0–150 | lockout |
| Current sensor (LEM) / reuse | [Mouser LEM](https://www.mouser.com/c/?q=LEM%20HASS) | $0–60 | |
| Crash/inertia switch | [Amazon](https://www.amazon.com/s?k=inertia+fuel+cutoff+switch) | $20–40 | in coil circuit |

## C. Cabling & terminations
| Part | Source | ~$ | Note |
|---|---|---|---|
| **2/0 AWG** flexible welding cable | [Amazon](https://www.amazon.com/s?k=2%2F0+welding+cable) · local welding supply | $5–8/ft (~20 ft) | reuse donor orange first |
| Tinned copper lugs 2/0 | [Amazon Selterm](https://www.amazon.com/s?k=selterm+2%2F0+lugs) | $40–80 | |
| 16-ton hydraulic lug crimper | [Amazon](https://www.amazon.com/s?k=hydraulic+lug+crimper+16+ton) | $40–120 | one-time |
| Adhesive heat-shrink ≥600 V (3:1) | [Amazon](https://www.amazon.com/s?k=adhesive+lined+heat+shrink+3%3A1) | $20–40 | |
| Orange split loom (HV ID) | [Amazon](https://www.amazon.com/s?k=orange+split+loom) | $20–40 | |

## D. Power conversion & charging
| Part | Source | ~$ | Note |
|---|---|---|---|
| Charger + DC-DC — **reuse Leaf PDM** | donor (ZombieVerter drives it) | [DONOR] | Gen-2 (PF1) |
| Charger alt **Thunderstruck TSM2500** | [Thunderstruck-EV](https://www.thunderstruck-ev.com) | $500–900 | if not reusing |
| DC-DC alt (HV→12 V ~30 A) | [DigiKey Meanwell](https://www.digikey.com/en/products/filter/dc-dc-converters) | $150–300 | |
| J1772 inlet — **reuse Leaf port** | donor / [EV West](https://www.evwest.com) | $0–120 | in fuel door |

## E. Mechanical (the custom parts — PARTS board)
| Part | Source | ~$ | Note |
|---|---|---|---|
| **Adapter plate** (custom) | local machine shop · [BRAT Industries](https://bratindustries.net/product/leaf-adapter-plate/) | $320–500 | `cad/adapter-spec.md` |
| **Coupler/hub** | [EV Coupler Connection](https://www.evcouplerconnection.com) · [EVcreate](https://www.evcreate.com/shop/drivetrain/flanged-nissan-leaf-motor-coupler/) | $200–360 | EM57 output |
| Motor mounts (steel + poly) | local fab | $60–150 | crossmember hardpoints |

## F. Re-source (jobs the engine did)
| Part | Source | ~$ | Note |
|---|---|---|---|
| Brake vacuum **Hella UP30** + reservoir | [Amazon](https://www.amazon.com/s?k=hella+up30+vacuum+pump) | $80–200 | ⚠ verify before driving |
| Cabin **PTC coolant heater** (salvage) | salvage Volt/Leaf · [Amazon](https://www.amazon.com/s?k=PTC+coolant+heater+12v) | $80–300 | required for defrost |

## G. Battery
| Part | Source | ~$ | Note |
|---|---|---|---|
| **Stage 1 — donor Leaf pack** (40 kWh) | donor | [DONOR] | ~120 mi |
| **Stage 2 — Tesla 5.3 kWh ×14** | [ampREVOLT](https://amprevolt.com) · [EV West](https://www.evwest.com) · [Stealth EV](https://www.stealthev.com) | ~$9.7k | shop the ~2× spread |

## H. Head unit + control computer  → full list in `headunit-bom.md`
| Part | Source | ~$ |
|---|---|---|
| Raspberry Pi 5 (4 GB) | [raspberrypi.com](https://www.raspberrypi.com/products/raspberry-pi-5/) | $60 |
| 7" double-DIN HDMI touch | [Amazon](https://www.amazon.com/s?k=7+inch+double+din+hdmi+touchscreen) | $70–90 |
| **2-ch CAN HAT** (MCP2515/2517) | [Waveshare](https://www.waveshare.com/2-ch-can-hat.htm) | $20 |
| 12 V→5 V buck + UPS HAT | [Amazon](https://www.amazon.com/s?k=raspberry+pi+ups+hat) | $35 |
| USB DAC + 4-ch amp (sub via Kicker) | [Amazon](https://www.amazon.com/s?k=usb+dac) | $10–70 |

## I. Safety / PPE + tools (one-time — do **not** cheap out on gloves/fuse)
| Part | Source | ~$ |
|---|---|---|
| **Class-0 (1000 V) gloves** + leather over | [Amazon](https://www.amazon.com/s?k=class+0+electrical+gloves+1000v) | $80–150 |
| CAT III DC meter (Fluke / budget) | [Amazon](https://www.amazon.com/s?k=fluke+117) | $40–400 |
| Insulation tester (megger) | [Amazon](https://www.amazon.com/s?k=insulation+tester+megohmmeter) | $60–400 |
| CO₂ / ABC extinguisher | [Amazon](https://www.amazon.com/s?k=co2+fire+extinguisher) | $40–80 |

## Totals
| Build | Net cost |
|---|---|
| **Cheapest-viable Stage-1** (cheap donor, reuse all HV, sell gas parts) | **~$2.5–3.5k** |
| **Comfortable Stage-1 MVP** (good Gen-2 donor + new safety bits + head unit) | **~$6.5–8k** |
| Stage-2 (Tesla 74 kWh pack) | +~$9.7k |
| Finish (Toxic Green wrap→paint, ADR-0017) | +$0.6–9k (post-MVP) |

## Vendor cheat-sheet
**EV-specific:** [EV West](https://www.evwest.com) · [ampREVOLT](https://amprevolt.com) · [Thunderstruck-EV](https://www.thunderstruck-ev.com) · [EVBMW](https://www.evbmw.com) · [openinverter](https://openinverter.org) · [EV Coupler Connection](https://www.evcouplerconnection.com) · [BRAT Industries](https://bratindustries.net)
**Electronics:** [Mouser](https://www.mouser.com) · [DigiKey](https://www.digikey.com) · [Waveshare](https://www.waveshare.com)
**Donor / used:** [Copart](https://www.copart.com/vehicle-search-model/nissan/leaf) · [eRepairables](https://erepairables.com/salvage-cars-auction/nissan/leaf) · [Car-Part](https://www.car-part.com)
**Generic / tools:** [Amazon](https://www.amazon.com) · local welding supply · local machine shop

> Live the budget on the **PLAN** tab (per-task cost + spent tracker). Prices/links are estimates —
> verify at purchase; size the fuse + precharge to your inverter (PF2).
