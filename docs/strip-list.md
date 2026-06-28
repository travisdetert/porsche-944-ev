# What Comes Out (and What Stays) — stripping the 944 into an electric go-kart

We're not just removing the engine — we're **stripping it light like a go-kart.** Going
electric deletes the engine and every system that fed, cooled, ignited, or silenced it; the
**go-kart cut** then deletes the comfort gear we don't want (A/C, audio, sound deadening).
What's left is the RC-car essence — battery → controller → motor → wheels — in a light, low,
raw 944.

Going electric sheds ~**8–10 systems and ~500–600 lb** of ICE (a pile of parts to sell); the
go-kart cut sheds another **~150–250 lb** of comfort gear. A short list of jobs the engine
quietly did (brake vacuum, cabin heat, 12 V charging) must be **re-sourced** electrically.

## The short answer
- **Strip:** ~500–600 lb of ICE hardware — the whole powertrain support stack.
- **Keep:** the entire Porsche chassis/driveline — transaxle, torque tube, suspension, brakes.
- **Re-source:** 4–5 small functions the engine used to provide.
- **Net (go-kart spec):** strip ~560 lb ICE + ~200 lb comfort, add ~285 lb motor/electronics
  + the battery. The **Stage-1 mule on a small donor pack lands ≈ stock weight** with a *lower*
  CG; full Stage-2 (74 kWh) is ~+400 lb but still stripped and low.

---

## STRIP — comes out
| System | Parts removed | ~Weight | Resale? |
|---|---|---|---|
| **Engine** | 2.5L block, head, internals, balance shafts, flywheel | ~330 lb | ✅ core/running |
| **Clutch** | clutch disc/pressure plate, slave/master (clutchless build) | ~25 lb | ✅ |
| **Fuel system** | tank, lines, pump, filter, injectors, rail, evap/charcoal canister | ~75 lb | ✅ |
| **Exhaust** | manifold, downpipe, catalytic converter, muffler, hangers | ~45 lb | ✅ cat has value |
| **Intake** | airbox, AFM/MAF, throttle body, intake manifold | ~15 lb | ✅ |
| **Ignition** | coil, distributor/cap/rotor, plugs, wires | ~5 lb | ✅ |
| **Engine management** | DME/Motronic ECU, crank/cam/knock/temp/O2 sensors | ~5 lb | ✅ ECU sells well |
| **Belt accessories** | alternator, A/C compressor, power-steering pump, engine water pump, belts/pulleys | ~50 lb | ✅ |
| **Starter** | starter motor | ~10 lb | ✅ |
| **Engine cooling** | engine-specific hoses, thermostat housing (radiator repurposed) | ~15 lb | partial |
| **Mounts/brackets/harness** | engine mounts, brackets, most of the engine wiring harness | ~20 lb | scrap/partial |
| **Total** | | **~500–600 lb** | **~$500–1,500 in sales** |

## KEEP — the Porsche stays
Transaxle (gearbox + diff) · torque tube + driveshaft · half-shafts, hubs, wheels · **brakes**
· **suspension** (incl. rear torsion bars) · steering rack · chassis, body, glass · interior ·
lights & most body wiring · **radiator + fans** (repurposed to cool the inverter/motor) ·
HVAC ducting/blower.

## RE-SOURCE — jobs the engine did that you must replace
| Lost function | Was driven by | EV replacement | ~Cost |
|---|---|---|---|
| **Brake boost** | intake-manifold vacuum | **electric vacuum pump** (or iBooster) | $80–250 |
| **Cabin heat / defrost** | engine coolant heat | **electric coolant heater (PTC)** — needed for defrost / registration | $80–300 |
| **12 V charging** | alternator | **DC-DC converter** (reuse Leaf PDM) | [donor] |
| **Power steering** (hydraulic) | belt-driven hydraulic pump | **electric hydraulic pump (EHPS)** feeds the stock rack (ADR-0013) | $80–300 |
| ~~A/C~~ | belt-driven compressor | **DELETE** — go-kart spec, no A/C | $0 |
| **Tach / gauges** | engine signals | driven from the **VCU/CAN** | $0–100 |

> **Don't skip the defroster.** No engine = no free cabin heat. A small electric coolant
> heater keeps the windshield clear — which is also usually a **registration/inspection**
> requirement. Budget item, not optional.

---

## STRIP MORE — the go-kart cut (no A/C, radio, comfort)
| Item | Parts | ~Weight | Note |
|---|---|---|---|
| **A/C system** | condenser, evaporator, dryer, lines (compressor already gone) | ~30–40 lb | delete entirely |
| ~~Audio~~ | **KEPT & UPGRADED** — real stereo + subs | +30–50 lb | the one indulgence — see `adr/0009` |
| **Sound deadening + carpet** | tar mats, carpet, jute | ~40–70 lb | old cars hide real weight here |
| **Rear seats** | frames + cushions | ~25–35 lb | |
| **Non-essential trim** | console, extra panels, cruise | ~20–40 lb | keep it spartan |
| **Spare + jack** (optional) | spare, jack, tools | ~30–40 lb | frees the rear well for a battery box |
| **Go-kart cut total** | | **~135–225 lb** (audio stays) | lighter, simpler wiring, more raw feel |

## The go-kart payoff (weight)
Strip the ICE *and* the comfort gear and the math gets fun — especially the **Stage-1 mule on
a small donor pack**:

```
  stock 944 ................... 2,900 lb
  - ICE removed .............. -  560
  - go-kart cut (audio kept) . -  160
  + motor + electronics ..... +  285
  + Stage-1 donor pack (24kWh) +  480
  + stereo + subwoofers ..... +   45
  ============================================
  = ~2,990 lb  ~= STOCK WEIGHT -- instant torque, lower CG, and it SLAPS
```
A genuine **electric go-kart**: about stock weight, a *lower* CG, and EV punch off the line.
(Full Stage-2 74 kWh adds ~400 lb for range — still stripped and low.)

## The one indulgence — a real stereo + subs
We strip the comfort gear but **keep and upgrade the audio** — proper head unit, amp, speakers,
and subwoofer(s). Two things to plan for:
- **Power:** big bass pulls real current. Size the **12 V / DC-DC** for the amp, and add a
  **stiffening capacitor or a small aux 12 V battery** for the audio so peaks don't sag the system.
- **Install:** EVs are *quiet*, so the stereo is the dominant sound — do it right. Add
  **localized sound deadening** around the subs (a little weight back) for tight bass and no
  rattles. The **sub enclosure competes with the rear-well battery box** for space — pick one.
  See `adr/0009`.

## Keep the street-legal minimum (for grocery runs on public roads)
Light is great; legal matters if it touches the road:
**lights** (head/tail/turn/brake) · **brakes + parking brake** · **electric defroster** ·
**wipers/washer** · **driver seat + seatbelt** · **mirrors** · **horn** · plates/VIN.
> Private-track / off-road only? Then even these are optional — full bare go-kart. For grocery
> runs, keep this short list. Decision recorded in `adr/0008`.

## The two wins
1. **Funding:** the stripped gas parts are worth **~$500–1,500** to other 944 owners — that
   cash directly offsets the donor Leaf (see `procurement-plan.md`).
2. **Weight + space:** ~560 lb of ICE gone and a wide-open engine bay, freeing room for the
   motor, electronics, and the front battery box (`944-layout-design.md`) — all mounted low.

> This *is* the "big RC car" reveal in physical form: nearly everything that made it a
> combustion car comes out, and four simple parts (battery → controller → motor → throttle)
> go in. Strip list ↔ Session 1 teardown (task #8).
