# 944 EV — Low-CG Packaging (drivetrain + batteries mounted as low as possible)

The single biggest handling lever in an EV conversion is **how low the heavy mass sits.**
We pulled a tall iron engine out; now we mount the motor and the ~880 lb battery **in the
floor of the car**, between the frame rails, as low as ground clearance allows. The result
is a CG *lower than stock* — the car corners flatter and feels more planted than it ever did.

Pairs with `battery-pack-and-balance.md` (the front/rear split + weights) — this doc is the
**vertical** story: getting it low.

---

## 1. Side profile — heavy mass kept at/below axle height

```
  FRONT                                                               REAR
  =========================================================================
        ___________________________________________
       /                 cabin (seats)              \________________
    __/   [D]                              [P]        \   hatch/cargo   \__
   |  hood                                             |                    |
   | +------+                                          |        +------+    |
   | | MOTOR|  <- low in engine bay                    |        | rear |    |
   | +------+                                          |        | mods |    |
   |        ########   ##########################      |        +------+    |
   |        front box   MAIN PACK (under cabin floor)   |   <- all packs LOW |
   |====O==============================================================O=====
        front wheel        ^ mass kept at/below axle centerline      rear wheel
```

The motor sits **lower than the engine did**; the pack lives **under the cabin floor and in
the old fuel-tank bay** — never up in the engine bay where it would raise the CG.

---

## 2. Cross-section (looking forward) — the "as low as possible" view

```
             ________________________________________
            /                                        \          roof
           /     ___                      ___          \
          |     | D |                    | P |           |      occupants
          |     |___|                    |___|           |      (the only high mass —
          |   =============== floor pan ===============  |       keep it light)
          |    +------------------------------------+   |
    ======+====|         BATTERY PACK (low)         |===+======  frame rails:
          |    +------------------------------------+   |        pack sits BETWEEN
          |  rocker                            rocker   |        them, bottom near
          +-------O------------------------------O------+        the floorpan
                  tire           road            tire
          |<------ as low as ground clearance + skid plate allow ------>|
```

This is where "low CG" actually happens: the pack bottom is **just above the lowest safe
point over the road**, slung between the rockers/frame rails, **below the occupants' hip
line.** The mass is in the floor, not stacked on top of it.

---

## 3. Why low matters — CG height vs. the stock engine

```
   STOCK (ICE)                              EV (this build)

   +-----------+  <- CG HIGH                 (engine bay now light:
   |  ENGINE   | (.)  tall iron mass          motor only, mounted low)
   |  (tall)   |      sits up high
   +-----------+                             ############
   ----------- floor -----------            ----(.)------  <- battery mass
                                                  ^          IN the floor = CG LOW
   Heavy mass HIGH -> more body roll        Heavy mass LOW -> flat, planted cornering
```

Lower CG = less weight transfer, less body roll, more grip in corners. Combined with the
**49/51 front/rear** balance from `battery-pack-and-balance.md`, you get a car that's both
**evenly balanced *and* low** — the handling actually improves over stock.

---

## How low is "as low as possible"? (the limits)
You lower the pack until one of these stops you — not past it:
- **Ground clearance / breakover angle:** the pack bottom can't hang below safe road
  clearance (driveways, speed bumps). The 944 is already low — respect it.
- **Crash/strike protection:** add a **steel skid plate / structural underfloor** so a road
  strike can't breach the pack. This sets a hard floor on how low you go.
- **Structure, not sheetmetal:** the pack mounts to **frame rails / floorpan hardpoints**,
  framed in — never hung off thin sheet.
- **HV isolation + sealing:** sealed, vented enclosure; HV isolated from chassis; **MSD
  reachable** (see `SECURITY.md`).

## The payoff
- **Lower CG than stock** despite +575 lb — because the iron engine (high) is gone and the
  battery (heavy) is in the floor (low).
- **49/51 balance** preserved (front box + main box split — see balance doc).
- A converted 944 that corners flatter and feels more planted than the original.

> System/electrical diagrams: `drive-plan.md` · `drivetrain-diagrams.md`.
> Front/rear weight split + module placement: `battery-pack-and-balance.md`.
