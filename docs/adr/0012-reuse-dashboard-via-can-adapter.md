# ADR-0012: Reuse the 944 dash via a CAN-to-gauge adapter

**Status:** Accepted
**Date:** 2026-06-27
**Deciders:** Travis

## Context
The stock 944 cluster's gauges were driven by ICE senders (ignition, fuel float, oil, engine
coolant) that no longer exist. We want to keep the classic dash working and informative — and
the speedo must work for inspection/registration. The ZombieVerter publishes all the relevant
data (RPM, SOC, voltages, temps) on **CAN**.

## Decision
**Keep the stock 944 instrument cluster** and drive it from the ZombieVerter CAN bus via a small
**ESP32 + CAN-transceiver "gauge adapter"** that mimics the original sender signals. Repurpose
gauges: **tach → motor RPM, fuel → SOC, oil-press → HV volts, oil-temp → battery temp**; keep
**speedo** (transaxle-native) and **coolant-temp** (reads the EV coolant loop).

## Alternatives considered
- **Rip out the cluster for a digital dash/tablet** — rejected: loses the 944 character, costs
  more, and is against the reuse ethos. (A small digital readout *alongside* stays optional.)
- **Leave the gauges dead** — rejected: no driving info, and a dead speedo fails inspection.

## Consequences
- **Positive:** classic look retained; **~$20–50** total; reuses the entire cluster; speedo +
  coolant-temp are near-native.
- **Negative / accepted cost:** per-gauge **calibration** to match sender curves (an afternoon);
  repurposed gauges want a **printed overlay** label.
- **Follow-ups:** flash the gauge-adapter firmware (openinverter examples); make the relabel
  overlay; add the adapter to the BOM (`parts-inventory.md`). See `docs/dashboard-reuse.md`.
