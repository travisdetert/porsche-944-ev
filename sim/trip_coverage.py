#!/usr/bin/env python3
"""
Trip coverage — does the hardware cover the trips we actually want to take?

Pulls REAL road distances (OSRM) from Menomonee Falls to a set of Wisconsin
destinations, then runs each through the EV physics model (ev_944_sim.Vehicle) at
highway speed to answer, per battery pack:
  - can we reach it on one charge (with a 10% arrival reserve)?
  - round-trip on one charge, or charge at the destination?
  - given v1 is AC Level-2 ONLY (6.6 kW, ADR-0006), how long is that destination charge?

Honest by design: highway steady-state (worse than the mixed number), 10% reserve,
no DCFC. Run: python3 sim/trip_coverage.py
"""
import json
import math
import urllib.request

from ev_944_sim import MOTORS, Vehicle

ORIGIN = (43.1789, -88.1170)        # Menomonee Falls
MOTOR = "Leaf EM57"                  # the planned build
PACKS = [50, 74, 90]                # kWh options to compare
L2_KW = 6.6                         # AC Level-2 only (ADR-0006)
RESERVE = 0.10                      # arrive with >=10% in the tank
HWY_MPH, HWY_MIX = 70, 1.12        # steady highway (less efficient than 'mixed')

# (name, (lat, lon), straight-line fallback miles if OSRM is unreachable)
TRIPS = [
    ("Lake Geneva getaway",        (42.5917, -88.4334), 48),
    ("Wisconsin Dells",            (43.6275, -89.7710), 95),
    ("Green Bay (Lambeau)",        (44.5013, -88.0622), 105),
    ("Door County (Sturgeon Bay)", (44.8341, -87.3770), 140),
    ("Minocqua (Northwoods)",      (45.8708, -89.7152), 210),
    ("Bayfield / Apostle Islands", (46.8111, -90.8192), 330),
]


def haversine_mi(a, b):
    R = 3958.8
    la1, lo1, la2, lo2 = map(math.radians, [a[0], a[1], b[0], b[1]])
    h = math.sin((la2 - la1) / 2) ** 2 + math.cos(la1) * math.cos(la2) * math.sin((lo2 - lo1) / 2) ** 2
    return 2 * R * math.asin(math.sqrt(h))


def road_mi(a, b, fallback):
    url = ("https://router.project-osrm.org/route/v1/driving/"
           f"{a[1]},{a[0]};{b[1]},{b[0]}?overview=false")
    try:
        d = json.load(urllib.request.urlopen(url, timeout=25))
        return d["routes"][0]["distance"] / 1609.34, "OSRM"
    except Exception:
        return haversine_mi(a, b) * 1.25, "est"   # ~25% over crow-flies


def main():
    print("=" * 96)
    print(f"  TRIP COVERAGE — {MOTOR}, highway {HWY_MPH} mph, {int(RESERVE*100)}% arrival reserve, "
          f"AC L2 {L2_KW} kW only (ADR-0006)")
    print("=" * 96)

    ranges = {}
    for kwh in PACKS:
        v = Vehicle(MOTORS[MOTOR], kwh)
        rng, wh = v.range_mi(mph=HWY_MPH, mix=HWY_MIX)
        ranges[kwh] = (rng, wh)
        print(f"   {kwh:>2} kWh pack: highway range {rng:5.0f} mi @ {wh:3.0f} Wh/mi  "
              f"(usable to {int(RESERVE*100)}% reserve: {rng*(1-RESERVE):.0f} mi)")
    print("-" * 96)
    hdr = f"  {'Destination':<26}{'1-way':>7}{'round':>7}   " + "".join(f"{str(k)+'kWh':>14}" for k in PACKS)
    print(hdr)
    print("  " + "-" * 92)

    summary = {k: [] for k in PACKS}
    for name, dest, fb in TRIPS:
        ow, src = road_mi(ORIGIN, dest, fb)
        rt = ow * 2
        cells = ""
        for kwh in PACKS:
            rng, wh = ranges[kwh]
            usable = rng * (1 - RESERVE)
            if rt <= usable:
                tag = "✓ round-trip"
                summary[kwh].append("round")
            elif ow <= usable:
                charge_h = (ow * wh / 1000) / L2_KW           # refill the leg at the destination
                tag = f"✓ +{charge_h:.0f}h L2"
                summary[kwh].append("oneway")
            else:
                stops = math.ceil(ow / usable) - 1
                tag = f"✗ {stops} stop" + ("s" if stops != 1 else "")
                summary[kwh].append("short")
            cells += f"{tag:>14}"
        print(f"  {name:<26}{ow:>6.0f}{rt:>7.0f}   {cells}   [{src}]")

    print("  " + "-" * 92)
    print("  Legend: ✓ round-trip = there & back on ONE charge · ✓ +Nh L2 = reach it, then an")
    print("          overnight L2 charge at the destination · ✗ N stops = needs en-route charging")
    print("          (on L2 that's hours — the case for a DCFC/CCS retrofit, or a bigger pack).")
    print("=" * 96)
    for kwh in PACKS:
        s = summary[kwh]
        rt = s.count("round"); ow = s.count("oneway"); sh = s.count("short")
        print(f"   {kwh} kWh: {rt} round-trip · {ow} reachable w/ dest charge · {sh} need en-route charging")
    print("=" * 96)


if __name__ == "__main__":
    main()
