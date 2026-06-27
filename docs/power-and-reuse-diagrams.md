# Power Distribution & Hardware Reuse

How power flows through the converted car, and — the part that makes this plan elegant — how
little of it is actually *new*. You're re-animating a 944 with a wrecked Leaf's organs.

---

## 1. Power distribution (where the watts go)
The HV battery feeds one bus; that bus splits into **traction** (the big load) and a **DC-DC**
tap that runs the whole 12 V car. The charger feeds the bus from the wall.

```mermaid
flowchart LR
  AC["Wall AC<br/>L1 / L2"] --> OBC["Onboard charger<br/>(Leaf PDM)"]
  BATT["HV battery<br/>~350 V"] --> MSD["MSD"] --> FUSE["HV fuse"] --> CTR["Contactors<br/>+ precharge"]
  OBC --> CTR
  CTR --> BUS{{"HV bus ~350 V"}}
  BUS -->|"up to ~110 kW"| INV["Inverter"] --> MOT["EM57 motor"] --> WHL["transaxle → wheels"]
  BUS -->|"~1–2 kW"| DCDC["DC-DC<br/>(Leaf PDM)"]
  DCDC --> LV{{"12 V bus"}}
  LV --> LIGHTS["lights · wipers · horn"]
  LV --> PUMPS["coolant + brake-vacuum pumps"]
  LV --> HEAT["PTC defroster"]
  LV --> AUDIO["stereo + subs<br/>(+ aux 12 V battery)"]
  LV --> VCU["ZombieVerter VCU"]
  LV --> INST["instruments"]
  BMS["BMS (Leaf LBC)"] -. monitors .-> BATT
  VCU -. throttle → torque .-> INV
  VCU -. closes .-> CTR
```

**Reading it:** ~99% of the power goes to traction (up to ~110 kW); everything else in the car
sips ~1–2 kW through the DC-DC. The VCU is the brain — it turns the pedal into inverter torque
and sequences the contactors; the BMS guards the pack.

---

## 2. Hardware reuse map (944 · donor Leaf · new)
Green = kept from the Porsche. Blue = reused from the donor Leaf. Orange = the *only* new parts.

```mermaid
flowchart TB
  subgraph K944["KEPT from the 944 — the great mechanicals"]
    TX["Transaxle + diff"]; TT["Torque tube"]; SUS["Suspension"]
    BR["Brakes"]; STG["Steering"]; CH["Chassis / body / wheels"]
  end
  subgraph LEAF["REUSED from the donor Leaf — the whole HV system"]
    MO["EM57 motor"]; IN["Inverter"]; PDM["Charger + DC-DC (PDM)"]
    BAT["Traction battery (Stage 1)"]; LBC["BMS (LBC)"]; PED["Accelerator pedal"]
    CP["Charge port"]; HVB["Contactors · fuse · HV cable"]; CPMP["Coolant pump"]
  end
  subgraph NEW["NEW — the only things actually bought"]
    ZV["ZombieVerter VCU (~$380)"]; ADP["Adapter + coupler (machined)"]
    SAFE["HV safety extras"]; AUD["Stereo + subs"]
  end
  K944 --> CAR(["944 electric go-kart"])
  LEAF --> CAR
  NEW --> CAR
  classDef k fill:#2f7d32,stroke:#1b5e20,color:#fff
  classDef l fill:#1565c0,stroke:#0d47a1,color:#fff
  classDef n fill:#e65100,stroke:#bf360c,color:#fff
  class TX,TT,SUS,BR,STG,CH k
  class MO,IN,PDM,BAT,LBC,PED,CP,HVB,CPMP l
  class ZV,ADP,SAFE,AUD n
```

---

## 3. Reuse scorecard
| Source | What it provides | Cost |
|---|---|---|
| **Kept from the 944** | transaxle, torque tube, suspension, brakes, steering, chassis, wheels, HVAC, lights | **$0** |
| **Reused from the donor Leaf** | motor, inverter, charger, DC-DC, battery, BMS, pedal, charge port, contactors, fuse, cable, coolant pump | **one donor (~$2.5–4.5k)** |
| **New (bought)** | ZombieVerter VCU, custom adapter + coupler, a few HV safety extras, stereo | **~$1–1.5k** |

**The punchline:** the entire high-voltage powertrain is **two donors deep in reuse** — the
Porsche gives the rolling chassis and the transmission of power; the Leaf gives the *entire*
electrical drivetrain, pre-matched. The only genuinely **new electronics is a ~$380 control
board** (ZombieVerter), and the only **new fabrication is one adapter.** Everything else is a
second life for parts that were headed for scrap.

> That's the whole spirit in one picture: **two cars that were each "done" — a 944 with a dead
> engine and a Leaf with a dead body — become one car that drives.**

Power flow detail: `drivetrain-diagrams.md` §5–6 · System integration: `drive-plan.md` ·
What's removed: `strip-list.md`.
