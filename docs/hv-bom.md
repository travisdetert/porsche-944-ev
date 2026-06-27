# HV Bill of Materials — Stage 1 (with sizing rationale)

The parts that make the pack safe to connect, drive, and charge. **Read `SECURITY.md`
first.** Every HV component here is rated **≥ 500 V DC** so it covers both the Stage-1
donor Leaf pack (~350–400 V) and the Stage-2 Tesla 14S1P pack (~319–365 V) without rework.

> **Verify ratings against your actual inverter/motor specs.** The EM57 peak current,
> capacitor bank size, and your cable runs set the final fuse/contactor/precharge values.
> Numbers below are correct sizing *methodology* with sensible defaults — confirm before buying.

## Sizing basis
- **Pack voltage:** Stage 1 ~350–400 V (Leaf), Stage 2 ~319 V (Tesla 14S1P). Rate **≥500 V DC**.
- **EM57 power:** ~80–110 kW peak. At ~350 V that's **~315 A peak**, ~150–200 A continuous.
- Everything sized to **≥315 A peak / 500 V DC**, DC-rated for arc interruption.

## Safety-critical HV components
| Item | Sizing / spec | Example | Why |
|---|---|---|---|
| **Main contactor** | ≥500 V DC, ~500 A class, with coil economizer + flyback diode | Tyco/TE **EV200**, Gigavac **GV200** | Connects pack to inverter; BMS/VCU must be able to force it open |
| **Precharge contactor** | small HV relay, ≥500 V DC | Gigavac **GH/GX** series | Switches the precharge path before the main closes |
| **Precharge resistor** | ~50–100 Ω, ≥50–100 W wirewound | 100 Ω / 100 W | Soft-charges inverter caps; RC ≈ 100 Ω × ~1.5 mF ≈ 0.15 s → ~0.75 s precharge |
| **Main HV fuse** | **DC-rated** ≥500 V DC, ~250–300 A, fast/semi-fast | Mersen/Ferraz or Bussmann **FWP** | Interrupts a short before cables/pack do; **AC fuses cannot break DC arcs** |
| **Manual Service Disconnect (MSD)** | breaks the pack mid-string; ≥500 V DC, pack-current rated | salvage HV MSD or HV-rated disconnect | Makes the pack inert for any work; your lockout |
| **Inertia/crash switch** | in the contactor-coil (12 V) circuit | inertia switch | Drops HV in a crash |
| **HVIL (optional, recommended)** | low-V loop through HV connectors → drops contactor if any opens | — | Prevents energizing an open connector |
| **Current sensor** | hall sensor sized to ≥400 A, for VCU/BMS | LEM / Isabellenhütte, or reuse Leaf's | Feedback for control + protection |

## HV cabling & terminations
| Item | Spec | Why |
|---|---|---|
| **HV cable** | **2/0 AWG** fine-strand welding cable, ≥600 V insulation | Good for ~315 A peak in open air; flexible |
| **Lugs** | crimp copper lugs to match | Terminations |
| **Hydraulic crimper** | proper die set | A bad crimp = a hot joint = a fire |
| **Adhesive heat-shrink** | ≥600 V | Insulate + strain-relieve every lug |
| **Orange convoluted loom** | — | HV identification (code + sanity) |
| **Terminal covers / boots** | per connector | No exposed live metal |

## Power conversion (reuse from donor where possible)
| Item | Source | Notes |
|---|---|---|
| **DC-DC converter** (HV→12 V, ~30 A) | reuse Leaf **PDM** | Keeps the 12 V car alive; ZombieVerter can drive the PDM |
| **On-board charger** | reuse Leaf **PDM** | AC L1/L2 charging via the Leaf charge port |
| **Charge port + J1772 inlet** | reuse from donor | — |

## Control & monitoring
| Item | Stage 1 | Stage 2 | Notes |
|---|---|---|---|
| **VCU** | **ZombieVerter** | same | Commands inverter, PDM, contactors; reads pedal |
| **BMS** | reuse Leaf **LBC** (read by ZombieVerter) | **simpBMS** for Tesla modules | Stage 1 leans on the Leaf's own BMS — a real simplification |
| **12 V battery** | standard | same | Powers the LV/control side |

## Low-voltage / misc
- Contactor coil supply + economizer + flyback diode; 12 V fusing for the control circuit.
- Accelerator pedal (from donor) → ZombieVerter analog/CAN input.
- Coolant pump + loop for the inverter/motor (reuse Leaf pump).
- Wiring, fuse block, relays, connectors for the 12 V side.

## Safety/PPE gear (if not owned — see `SECURITY.md`)
- **CAT III DC multimeter** rated ≥600 V · **Class-0 (1000 V) insulated gloves** + leather
  overgloves · **insulated tools** · **DC-rated fire extinguisher** · safety glasses ·
  **megger/insulation tester** for the pre-power-up isolation check.

## Reuse-from-donor vs. buy-new (cost reality)
- **Reuse (free with donor):** motor, inverter, PDM (charger+DC-DC), pack, LBC/BMS, charge
  port, pedal, coolant pump, HV cables, contactors (if undamaged).
- **Buy new:** ZombieVerter (~$380), DC-rated main fuse + MSD, fresh cable/lugs/loom, PPE.
- **Net new HV spend beyond the donor:** roughly **$700–1,200** (VCU + fuse + MSD + cable
  + crimper + loom), plus PPE if you don't own it. This is the "HV bits" line in the
  Stage-1 budget.

## Caveats
- The donor's **own contactors/fuse may be reusable** — inspect; many builders reuse them
  for Stage 1 and upgrade later.
- Final **fuse and precharge values depend on the EM57 inverter's capacitor bank** —
  confirm against the inverter spec / openinverter wiki before ordering.
- Stage 2 (Tesla pack) swaps the **BMS to simpBMS** and re-checks fuse sizing for 319 V;
  the contactors/cable/MSD carry over.
