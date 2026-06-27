# 944 EV — Performance Simulation

A first-principles model (tractive force vs. aero + rolling drag) for comparing build
configs. Run it: `python3 sim/ev_944_sim.py` (pure stdlib, no deps).

## What it models
- **0-60 mph** via time-step integration, limited by **RWD traction** (μ × rear weight)
  *and* the **stock-transaxle input-torque cap** (~350 Nm, ADR-0004).
- **Top speed** (rpm- or power-limited).
- **Range** from steady road-load consumption (highway + mixed).

## Swap motors, batteries & gearing
- Edit the **`MOTORS`** dict to add/change a motor (torque, power, rpm, mass, $).
- Change `TX_TORQUE_LIMIT` (transaxle cap) and `USD_PER_KWH` (battery cost) once confirmed.
- Sweeps: `motor_sweep(batt=…)`, `battery_sweep(motor=…)`, `gear_sweep(motor=…, batt=…)`.

## Headline findings (default run)
- **Reinvest in BATTERY, not motor** (ADR-0011): a 220 kW "power" build is only ~1.7 s
  quicker to 60 than the 110 kW EM57, but gives up ~half the range.
- **The transaxle is the wall:** past ~350 Nm, launch torque is identical — a bigger motor
  can't put more down. The **Leaf EM57 (320 Nm) already nearly maxes the transaxle.**
- **Range scales ~linearly with kWh**, and battery weight barely touches 0-60
  (~0.1 s per 20 kWh) — so range costs a **flat ~$40 per mile** of range, kept forever.
- **Gearing:** past ~7:1 the launch is traction-limited (0-60 plateaus ~7.0 s) so a taller
  ratio only *costs* top speed. **~6–7:1 is the sweet spot** (quick launch + ~100–120 mph top).

> Numbers are design estimates — confirm motor curve, CdA, and the transaxle torque limit
> on the real car, then re-run.
