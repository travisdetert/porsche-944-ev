# HV Safety Protocol — read before touching anything orange

This build runs a **~320–400 V DC traction pack**. That is **lethal**. DC across the
chest can stop your heart, and it causes muscles to *clamp* — you may not be able to let
go. Worse, the **inverter capacitors stay charged to pack voltage for minutes after you
disconnect the battery**. Respect this document like the wiring depends on your life,
because it does.

> This is the physical-safety analog of the standing code-security expectation: do a
> **wiring + isolation review before first power-up**, and again after any change to the
> HV system — same discipline as a security pass before a push.

## The non-negotiable rules
1. **Never work on live HV alone.** Have a buddy who knows how to cut power and do CPR.
2. **One-hand rule.** When near energized HV, keep one hand in your pocket. Never bridge
   hand-to-hand (the path runs across your heart).
3. **Assume every conductor is live until you have measured it dead** with your own meter.
4. **No jewelry, watches, or rings.** They turn a brush-contact into a burn or a weld.
5. **Insulated tools only** near HV. **Class 0 (1000 V) gloves**, inspected for pinholes,
   with leather overgloves. Safety glasses.
6. **DC-rated everything.** A meter, fuse, or switch rated only for AC will not safely
   interrupt a DC arc.

## De-energize procedure (do this before any HV work)
1. Vehicle off, key out, in Park/neutral, wheels chocked.
2. **Pull the Manual Service Disconnect (MSD)** and put it **in your pocket** (your lockout).
3. **Wait 5+ minutes** for the inverter capacitors to bleed down.
4. **Live-dead-live test your meter:** verify it on a known live source, then measure the
   inverter DC bus and pack terminals, then re-verify on the known source. The bus must
   read **< 60 V** before you touch anything.
5. Only now is it safe to work.

## Re-energize procedure (precharge — every power-up)
1. HV connections torqued, covered, and visually clear; no tools left behind.
2. Insert MSD.
3. Key on → BMS/VCU healthy → **precharge contactor closes** (resistor soft-charges the
   inverter caps) → **main contactor closes** → precharge opens → ready.
4. Never close the main contactor onto an uncharged bus — the inrush welds contacts and
   can rupture caps. The precharge step exists for this reason.

## First power-up — extra precautions
- Car on stands, wheels free, nobody under it.
- **DC-rated fire extinguisher** within reach; clear exit path.
- Eye protection; gloves; one hand rule.
- A helper at a **physical kill** (MSD or a 12 V cutoff to the contactor coil) ready to
  open the contactor instantly.
- Bring the bus up via precharge and watch for: contactor chatter, smoke, fault codes,
  unexpected motion. Anything wrong → kill power, walk away, diagnose de-energized.

## Always-on engineering requirements (built into the BOM)
- **HV isolated from chassis.** Add an isolation/insulation check (megger before first
  power-up; an IMD/insulation monitor is ideal for ongoing).
- **BMS can force the contactors open** on over/under-voltage or over-temp.
- **Inertia/crash switch** in the contactor-coil circuit.
- **HV fuse** sized to the pack, DC-rated, in the main path.
- **Orange loom/labels** on every HV conductor; covers on all live terminals.

## When to stop and get a professional
- You cannot confidently complete the de-energize + live-dead-live test from memory.
- Any sign of pack damage, swelling, electrolyte smell, or coolant in the pack.
- Isolation check shows HV leaking to chassis and you cannot find it.
- First power-up throws faults you do not understand — diagnose de-energized, ask the
  openinverter community, do not "just try it again" live.

**Golden rule:** if you are tired, rushed, or alone — stop. The pack will still be there
tomorrow. So should you be.
