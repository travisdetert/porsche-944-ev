# 944 EV — Performance Simulation

A first-principles model (tractive force vs. aero + rolling drag) for comparing build
configs. Run it: `python3 sim/ev_944_sim.py` (pure stdlib, no deps).

## What it models
- **0-60 mph** via time-step integration, limited by **RWD traction** (μ × rear weight)
  *and* the **stock-transaxle input-torque cap** (~350 Nm, ADR-0004).
- **Top speed** (rpm- or power-limited).
- **Range** from steady road-load consumption (highway + mixed).

## Swap motors & batteries
- Edit the **`MOTORS`** dict to add/change a motor (torque, power, rpm, mass).
- Change `TX_TORQUE_LIMIT` once you confirm the real transaxle limit.
- `motor_sweep(batt=…)` and `battery_sweep(motor=…)` show how each axis moves the model.

## Headline findings (default run)
- **Reinvest in BATTERY, not motor** (ADR-0011): a 220 kW "power" build is only ~1.7 s
  quicker to 60 than the 110 kW EM57, but gives up ~half the range.
- **The transaxle is the wall:** past ~350 Nm, launch torque is identical — a bigger motor
  can't put more down. The **Leaf EM57 (320 Nm) already nearly maxes the transaxle.**
- **Range scales ~linearly with kWh**, and added battery weight barely touches 0-60
  (~0.1 s per 20 kWh). So kWh is almost pure upside.

> Numbers are design estimates — confirm motor curve, CdA, and the transaxle torque limit
> on the real car, then re-run.
