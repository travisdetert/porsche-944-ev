#!/usr/bin/env python3
"""
944 EV — performance simulation with motor + battery swaps.

Core question (ADR-0011): stripping frees money + weight. Spend it on BATTERY or
MOTOR? This computes 0-60, top speed, and range from first principles (tractive
force vs aero + rolling drag), with TWO real caps that matter on this car:
  - RWD traction limit (mu * rear weight)
  - stock-transaxle input-torque limit (~350 Nm) -- ADR-0004

Sweeps let you swap motors and batteries to see how the models move.
Pure stdlib. Run: python3 sim/ev_944_sim.py
Design estimates -- confirm motor curve, CdA, and the transaxle torque limit on the car.
"""
import math

G, RHO, MPH = 9.81, 1.2, 2.2369

BASE_GLIDER_KG = 1050      # stripped 944: body + electronics, NO motor, NO battery
PACK_KG_PER_KWH = 5.5      # cells + enclosure
USD_PER_KWH = 130          # Tesla salvage modules, cheapest vendor (~$690 / 5.3 kWh)
TX_TORQUE_LIMIT = 350      # Nm the stock transaxle input will take (ADR-0004) -- verify

# Motor catalog: torque Nm, power W, max rpm, mass kg, approx salvage/kit $
# Specs from vendor/conversion sources (HyPer9 NetGain sheet; EM57 Nissan/openinverter). Verify on the unit.
MOTORS = {
    "HyPer9":      dict(T=235, P=95000,  rpm=8000,  kg=59,  usd=5400),  # NetGain kit (bolt-in)
    "Leaf EM57":   dict(T=320, P=110000, rpm=10500, kg=60,  usd=1000),  # baseline (ZE1 donor)
    "Leaf EM57 e+":dict(T=340, P=160000, rpm=10500, kg=62,  usd=1500),  # 62 kWh e+ donor, same motor
    "Dual EM57":   dict(T=640, P=220000, rpm=10500, kg=120, usd=2200),  # torque clamped by transaxle
}


class Vehicle:
    def __init__(self, motor, batt_kwh, CdA=0.62, Crr=0.011, wheel_r=0.30,
                 gear_R=7.2, eff=0.88, usable=0.90, rear_frac=0.52, mu=0.95,
                 tx_limit=TX_TORQUE_LIMIT, extra_kg=0):
        self.mo = motor
        self.kwh = batt_kwh
        self.m = BASE_GLIDER_KG + motor["kg"] + batt_kwh * PACK_KG_PER_KWH + extra_kg
        self.CdA, self.Crr, self.r = CdA, Crr, wheel_r
        self.R, self.eff, self.usable = gear_R, eff, usable
        self.rear, self.mu, self.tx = rear_frac, mu, tx_limit

    def wheel_force(self, v):
        w_omega = v / self.r
        m_omega = w_omega * self.R
        if m_omega * 60 / (2 * math.pi) > self.mo["rpm"]:
            return 0.0
        omega_base = self.mo["P"] / self.mo["T"]
        T = self.mo["T"] if m_omega <= omega_base else self.mo["P"] / m_omega
        T = min(T, self.tx)                       # transaxle torque cap
        return T * self.R * self.eff / self.r

    def road_load(self, v):
        return 0.5 * RHO * self.CdA * v * v + self.Crr * self.m * G

    def zero_to_60(self):
        dt, v, t = 0.005, 0.0, 0.0
        traction = self.mu * self.m * G * self.rear
        while v < 26.82 and t < 60:
            a = (min(self.wheel_force(v), traction) - self.road_load(v)) / self.m
            if a <= 0:
                return None
            v += a * dt; t += dt
        return t

    def top_speed(self):
        vmax, v = 0.0, 0.1
        while v < 160:
            if v / self.r * self.R * 60 / (2 * math.pi) > self.mo["rpm"]:
                break
            if self.wheel_force(v) > self.road_load(v):
                vmax = v
            else:
                break
            v += 0.1
        return vmax * MPH

    def range_mi(self, mph=65, mix=1.18):
        v = mph / MPH
        wh_per_mi = (self.road_load(v) * v / self.eff + 300) / mph * mix
        return self.kwh * self.usable * 1000 / wh_per_mi, wh_per_mi

    def pack_cost(self):
        return self.kwh * USD_PER_KWH

    def cost_per_mile_range(self):
        return self.pack_cost() / self.range_mi()[0]

    def lbs(self):
        return self.m * 2.2046

    def pwr_to_wt(self):
        return (self.mo["P"] / 1000) / (self.m / 1000)


def bar(value, vmax, width=20):
    return "#" * max(0, min(width, int(round(width * value / vmax)))) if vmax else ""


def line(c="-", n=86):
    print("  " + c * n)


def faceoff():
    RANGE = Vehicle(MOTORS["Leaf EM57"], 74, rear_frac=0.52)
    POWER = Vehicle(MOTORS["Dual EM57"], 40, rear_frac=0.50)
    print("=" * 90)
    print("  REINVESTMENT FACE-OFF -- spend the savings on BATTERY vs MOTOR")
    print("=" * 90)
    hdr = f"  {'':<15}{'STOCK gas':>16}{'RANGE (battery)':>20}{'POWER (motor)':>20}"
    print(hdr)
    print(f"  {'':<15}{'147hp I4':>16}{'EM57 + 74kWh':>20}{'DualEM57 + 40kWh':>20}")
    line()
    print(f"  {'Weight (lb)':<15}{2900:>16}{RANGE.lbs():>20.0f}{POWER.lbs():>20.0f}")
    print(f"  {'Motor':<15}{'147 hp':>16}{'110 kW':>20}{'220 kW':>20}")
    print(f"  {'Battery':<15}{'(tank)':>16}{'74 kWh':>20}{'40 kWh':>20}")
    line()
    print(f"  {'0-60 mph (s)':<15}{8.4:>16}{RANGE.zero_to_60():>20.1f}{POWER.zero_to_60():>20.1f}")
    print(f"  {'Top speed mph':<15}{130:>16}{RANGE.top_speed():>20.0f}{POWER.top_speed():>20.0f}")
    print(f"  {'Range mix (mi)':<15}{350:>16}{RANGE.range_mi()[0]:>20.0f}{POWER.range_mi()[0]:>20.0f}")
    print("=" * 90)
    return RANGE, POWER


def motor_sweep(batt=50):
    print(f"\n  MOTOR SWAP  (fixed {batt} kWh pack; transaxle torque cap = {TX_TORQUE_LIMIT} Nm)")
    line()
    print(f"  {'Motor':<14}{'kW':>6}{'Nm':>6}{'lb':>7}{'0-60':>7}{'top':>6}   launch torque used")
    line()
    for name, mo in MOTORS.items():
        v = Vehicle(mo, batt)
        z = v.zero_to_60()
        used = min(mo["T"], TX_TORQUE_LIMIT)
        capped = "  <-- CAPPED by transaxle" if mo["T"] > TX_TORQUE_LIMIT else ""
        print(f"  {name:<14}{mo['P']//1000:>6}{mo['T']:>6}{v.lbs():>7.0f}"
              f"{z:>6.1f}s{v.top_speed():>6.0f}   {used:>3.0f} Nm{capped}")
    line()
    print("  Past ~350 Nm the launch is identical -- the transaxle (not the motor) is the wall.")


def battery_sweep(motor="Leaf EM57"):
    mo = MOTORS[motor]
    print(f"\n  BATTERY SWAP  (fixed motor: {motor}, {mo['P']//1000} kW)")
    line()
    print(f"  {'Pack kWh':<9}{'lb':>6}{'0-60':>7}{'range':>9}{'pack $':>9}{'$/mi-range':>12}")
    line()
    for kwh in (30, 50, 74, 90):
        v = Vehicle(mo, kwh)
        rng, _ = v.range_mi()
        print(f"  {kwh:<9}{v.lbs():>6.0f}{v.zero_to_60():>6.1f}s{rng:>7.0f}mi"
              f"{'$'+format(v.pack_cost(), ',.0f'):>9}"
              f"{'$'+format(v.cost_per_mile_range(), '.0f'):>12}")
    line()
    print("  Range scales ~linearly with kWh, so $/mile-of-range is ~flat (~$40). Weight barely")
    print("  touches 0-60 -- battery is near-pure upside: ~$40 per added mile, kept forever.")


def gear_sweep(motor="Leaf EM57", batt=50):
    mo = MOTORS[motor]
    print(f"\n  GEAR-RATIO SWAP  (single fixed gear; {motor}, {batt} kWh)")
    line()
    print(f"  {'overall ratio':<15}{'0-60':>7}{'top mph':>9}   trade")
    line()
    for R in (4.0, 5.0, 6.0, 7.2, 8.5, 10.0):
        v = Vehicle(mo, batt, gear_R=R)
        trade = ("top-speed biased" if R <= 5
                 else "quick launch, low top" if R >= 9 else "balanced")
        print(f"  {R:<15.1f}{v.zero_to_60():>6.1f}s{v.top_speed():>8.0f}   {trade}")
    line()
    print("  Higher ratio = quicker 0-60 but lower (rpm-limited) top speed, and vice-versa.")
    print("  ~7-8 is the streetable sweet spot for the EM57 in the 944.")


def scatter():
    """ASCII 0-60 vs range scatter across motor x battery configs."""
    W, H = 64, 18
    XMAX, YMIN, YMAX = 320.0, 5.0, 13.0      # range axis, 0-60 axis (s)
    grid = [[" "] * W for _ in range(H)]
    configs = [
        ("a", "Leaf EM57", 30), ("b", "Leaf EM57", 50),
        ("c", "Leaf EM57", 74), ("d", "Leaf EM57", 90),
        ("e", "HyPer9", 50), ("f", "Leaf EM57 e+", 74),
        ("g", "Dual EM57", 40), ("h", "Dual EM57", 74),
    ]
    legend = []
    for tag, mname, kwh in configs:
        v = Vehicle(MOTORS[mname], kwh)
        z, rng = v.zero_to_60(), v.range_mi()[0]
        legend.append((tag, mname, kwh, z, rng))
        cx = max(0, min(W - 1, int(rng / XMAX * (W - 1))))
        cy = max(0, min(H - 1, int((z - YMIN) / (YMAX - YMIN) * (H - 1))))
        grid[cy][cx] = tag
    # stock gas reference
    cx = min(W - 1, int(350 / XMAX * (W - 1)))
    grid[min(H - 1, int((8.4 - YMIN) / (YMAX - YMIN) * (H - 1)))][cx] = "S"

    print("\n  0-60 vs RANGE  (UP = quicker, RIGHT = farther; top-right = best of both)")
    for r in range(H):
        ylab = YMIN + r * (YMAX - YMIN) / (H - 1)
        print(f"  {ylab:4.1f}s |" + "".join(grid[r]))
    print("        +" + "-" * W)
    xax = [" "] * W
    for s, col in [("0", 0), ("80", 16), ("160", 32), ("240", 48), ("320", W - 3)]:
        for i, ch in enumerate(s):
            if 0 <= col + i < W:
                xax[col + i] = ch
    print("         " + "".join(xax) + "   range (mi)")
    line()
    for tag, mname, kwh, z, rng in legend:
        print(f"   {tag}  {mname:<12}{kwh:>3} kWh   {z:>4.1f}s {rng:>4.0f} mi")
    print(f"   S  {'STOCK gas':<12}{'ref':>3}       8.4s  350 mi")
    line()
    print("  The EM57 line (a-d) sweeps battery: same quickness, more range rightward.")
    print("  Dual EM57 (g,h) buys ~1.5s up but no range; HyPer9 (e) is just slow. Battery wins.")


def main():
    R, P = faceoff()
    z, rr = R.zero_to_60() - P.zero_to_60(), R.range_mi()[0] / P.range_mi()[0]
    print(f"\n  0-60   RANGE {bar(10-R.zero_to_60(),10):<20} {R.zero_to_60():.1f}s")
    print(f"         POWER {bar(10-P.zero_to_60(),10):<20} {P.zero_to_60():.1f}s")
    print(f"  range  RANGE {bar(R.range_mi()[0],R.range_mi()[0]):<20} {R.range_mi()[0]:.0f} mi")
    print(f"         POWER {bar(P.range_mi()[0],R.range_mi()[0]):<20} {P.range_mi()[0]:.0f} mi")
    print(f"\n  => POWER is only ~{z:.1f}s quicker but RANGE goes ~{rr:.1f}x farther. "
          f"Reinvest in BATTERY. (ADR-0011)")
    print(f"     At ${USD_PER_KWH}/kWh: RANGE pack ${R.pack_cost():,.0f} -> {R.range_mi()[0]:.0f}mi "
          f"(~${R.cost_per_mile_range():.0f}/mi); POWER pack ${P.pack_cost():,.0f} -> {P.range_mi()[0]:.0f}mi.")

    motor_sweep()
    battery_sweep()
    gear_sweep()
    scatter()


if __name__ == "__main__":
    main()
