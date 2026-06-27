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
TX_TORQUE_LIMIT = 350      # Nm the stock transaxle input will take (ADR-0004) -- verify

# Motor catalog: name, torque Nm, power W, max rpm, mass kg, $ tier
MOTORS = {
    "HyPer9":     dict(T=160, P=88000,  rpm=8000,  kg=68),
    "Leaf EM57":  dict(T=320, P=110000, rpm=10500, kg=70),   # baseline
    "HiTorque AC":dict(T=350, P=130000, rpm=9000,  kg=80),
    "Dual EM57":  dict(T=640, P=220000, rpm=10500, kg=140),  # torque clamped by transaxle
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
    print(f"  {'Pack kWh':<10}{'lb':>7}{'0-60':>8}{'top':>6}{'range mix':>11}{'Wh/mi':>8}")
    line()
    for kwh in (30, 50, 74, 90):
        v = Vehicle(mo, kwh)
        rng, whmi = v.range_mi()
        print(f"  {kwh:<10}{v.lbs():>7.0f}{v.zero_to_60():>7.1f}s{v.top_speed():>6.0f}"
              f"{rng:>9.0f}mi{whmi:>8.0f}")
    line()
    print("  Range scales ~linearly with kWh; weight only nibbles 0-60 (~0.1s per 20 kWh).")


def main():
    R, P = faceoff()
    z, rr = R.zero_to_60() - P.zero_to_60(), R.range_mi()[0] / P.range_mi()[0]
    print(f"\n  0-60   RANGE {bar(10-R.zero_to_60(),10):<20} {R.zero_to_60():.1f}s")
    print(f"         POWER {bar(10-P.zero_to_60(),10):<20} {P.zero_to_60():.1f}s")
    print(f"  range  RANGE {bar(R.range_mi()[0],R.range_mi()[0]):<20} {R.range_mi()[0]:.0f} mi")
    print(f"         POWER {bar(P.range_mi()[0],R.range_mi()[0]):<20} {P.range_mi()[0]:.0f} mi")
    print(f"\n  => POWER is only ~{z:.1f}s quicker but RANGE goes ~{rr:.1f}x farther. "
          f"Reinvest in BATTERY. (ADR-0011)")

    motor_sweep()
    battery_sweep()


if __name__ == "__main__":
    main()
