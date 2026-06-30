# Transaxle & shifting — how the manual works in the EV 944

We keep the 944's stock **transaxle** (ADR-0004). Here's exactly how the manual gearbox, clutch,
and shifting behave once the engine is an electric motor — and why you basically **never shift.**

## The 944 layout (kept intact)
The 944 is **front-motor, rear-transaxle** for ~50/50 balance:
```
motor (front) → adapter/coupler → torque tube (driveshaft inside) → TRANSAXLE (rear) → diff → rear wheels
```
The **transaxle** = the 5-speed gearbox **and** the differential, in one unit at the back. The
torque tube carries a thin driveshaft from the front (where the engine/clutch was) to the rear box.
The app's **🔩 Driveline** view shows this chain.

## The big idea: EVs don't shift — you pick ONE gear
A gas engine has a narrow powerband (~1,000–6,500 rpm), so it needs 5 gears to cover the speed
range. An **electric motor makes full torque from 0 rpm and spins to ~10,500 rpm**, so **one gear
ratio covers ~0 to 90–100+ mph.** That's why every production EV (Leaf, Tesla) is a **single-speed.**

So in the 944 you **leave the manual in one gear and drive it like an automatic** — press the
pedal, go. No clutching, no shifting while moving.

## Which gear to leave it in (the one real tuning choice)
Pick the gear whose **overall ratio (gear × final drive ≈ 3.89)** lands in the streetable sweet
spot the sim found (**~7–8**). On a typical 944 5-speed:

| Leave it in | Overall ≈ | Feel |
|---|---|---|
| **2nd** (~2.06 × 3.89 ≈ 8.0) | ~8 | strongest launch, ~90–95 mph top, busier highway rpm (go-kart) |
| **3rd** (~1.41 × 3.89 ≈ 5.5) | ~5.5 | relaxed highway cruise, still strong off the line — **good all-rounder** |
| 4th (~1.0 × 3.89 ≈ 3.9) | ~4 | calm/efficient, softer launch, higher top |

> **Verify your transaxle's exact gear + final-drive ratios** (they vary by year/model). Start in
> **2nd or 3rd**, drive it, and pick — the motor's flat torque makes either perfectly drivable.

## Reverse, neutral, park
- **Reverse = the motor spins backwards** — electronically, via a **D/N/R selector → the VCU
  direction input** (`control-wiring.md`). You do **not** use the gearbox's mechanical reverse gear.
- **Neutral** = no torque commanded (VCU). **Park = the 944's mechanical handbrake** (kept).
- Reverse is **enabled only at standstill** (VCU interlock).

## The clutch — keep it or delete it
Since you don't shift, the clutch is optional:
- **Keep it** (simplest install, recommended to start): lets you **select the gear at a standstill**,
  gives a mechanical disconnect, and leaves the door open to occasionally pick a different gear or
  even run a **manual "2-speed"** (e.g., 2nd around town, 4th on the highway) if you want. The clutch
  pedal stays.
- **Delete it** (lighter, cleaner): **direct-couple** the motor to the transaxle input — saves
  ~10–15 lb and the pedal, but the car is then **fixed in whatever gear you set** (select it once).
  Common on dedicated single-speed conversions.

Either way, **driving is the same:** select D, press the pedal. You can *leave the H-pattern shifter
in 2nd/3rd and forget it.*

## The catch you already know about
The stock transaxle input is rated to **~350 Nm** (ADR-0004). So in your chosen gear, the VCU caps
torque there — which is exactly why "more motor past 350 Nm is wasted, spend on battery instead"
(the sim's whole point). One gear + that cap = a simple, durable, single-speed EV that still has the
944's balance and rear weight.

## TL;DR
Keep the transaxle, **leave it in 2nd or 3rd**, reverse is electronic (VCU), park is the handbrake,
and the clutch is optional (keep it to start). You drive it like a single-speed automatic — the
manual is there for the **gear ratio + diff + balance**, not for shifting.
