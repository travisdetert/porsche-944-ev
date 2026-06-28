# Custom Dash Panel + Gauge Faces — design spec

A clean custom layout for the **repurposed EV gauges** (ADR-0012). Model: `dash-panel.scad`
(flat panel cutouts) · preview: `dash-panel.svg` · gauge mapping: `../docs/dashboard-reuse.md`.

## Two routes (pick one)
- **A — Overlay the stock cluster (cheapest):** keep the 944 cluster housing; print **adhesive
  gauge-face overlays** with the new EV scales/labels. No new panel. Best for keeping the look.
- **B — New flat panel (this CAD):** laser/CNC a matte panel (`dash-panel.scad`) with the gauges
  in a custom go-kart layout. Cleaner/sparser; more work. Use the same printed faces.

## Layout (matches the preview)
| Gauge | Label | Source / scale |
|---|---|---|
| Large L | **MPH** | speedo — transaxle-native |
| Large R | **RPM ×1000** | motor RPM (CAN adapter) |
| Small | **CHARGE %** | ← fuel gauge → SOC 0–100 |
| Small | **HV ×100 V** | ← oil-press → pack volts |
| Small | **BATT °C** | ← oil-temp → battery temp |
| Small | **COOLANT** | native — EV coolant loop |
| Warning lamps | **FAULT · BMS · 12V · BRAKE** | VCU/BMS/DC-DC/brake |

## Material & build
- **Panel:** 3–4 mm matte **acrylic** (laser) or **aluminum** (CNC/waterjet). Bolts to the
  stock cluster points or a small bracket.
- **Faces:** print the per-gauge scales on **adhesive vinyl/paper**; apply to gauge fronts.
- Backlighting: reuse the cluster's existing illumination.

## Fit-check (no 3D printer)
- **Print `dash-panel.svg` at 1:1** on paper → use as a **drilling/face template** and to check
  each gauge body + needle clearance before cutting acrylic.

## Deliverable
- **DXF** from `dash-panel.scad` (`projection()` / 2D export) → laser/waterjet the panel.
- The **SVG faces** printed for the overlays.

## Keep it honest (legal)
- The **speedometer must read correctly** (inspection) — it's transaxle-native, verify calibration.
- Repurposed gauges get clear labels so the car is readable by anyone.

> Edit the layout in **both** `dash-panel.scad` (gauge vector) and `gen_previews.py` (`DASH`),
> then re-run `python3 cad/gen_previews.py` to refresh the preview.
