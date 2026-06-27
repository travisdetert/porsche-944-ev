# 1987 Porsche 944 — Electric

> **Get it running again. As cheaply as possible.**

A great old Porsche has been benched by a hard-starting engine. Rather than scrap a car
this good — or pour money into reviving a 39-year-old motor — we're giving it a new heart:
electric, built from **salvaged parts and our own hands**. Keep everything that makes it a
944 (the balance, the transaxle, the bones), change only the thing that died (the engine),
and **get it driving again** — starting with a run to the grocery store.

That's the whole project. Resurrection on a budget. Everything below is just how.

---

## The plan in one line
Swap the dead engine for a salvaged **Nissan Leaf** drivetrain, keep the Porsche's
mechanicals, and prove it drives **cheap first** — then grow the range later.

- **Stage 1 — the mule (~$3.5–5.5k):** run the Leaf motor on the **donor's own battery**
  (free with the parts). Goal: it *moves*, does a grocery loop. Proves everything risky.
- **Stage 2 — the range (later):** swap in a Tesla 74 kWh pack for ~150 miles. The mule
  *becomes* the final car — a battery swap, not a rebuild.

The cheapest way to honor the mission *is* the plan: prove it with parts you already have,
defer every dollar you can.

## Mental model: it's a big RC car
Strip away the scale and this is the *same machine* as a hobby RC car:

| RC car | This 944 |
|---|---|
| LiPo battery | ~880 lb traction pack |
| ESC (speed controller) | inverter + ZombieVerter VCU |
| brushless motor | Nissan Leaf EM57 |
| throttle on the transmitter | the accelerator pedal |
| balance charger | onboard charger + J1772 |

**Battery → speed controller → motor → wheels.** That's the whole machine. Everything *extra*
in this project exists for two reasons the RC car doesn't have: it runs **lethal voltage**
(so — contactors, precharge, fuses, a service disconnect, isolation, real PPE: non-negotiable,
see `SECURITY.md`), and it **carries you** (so the Porsche's brakes, suspension, and transaxle
stay). It's an RC car you can sit in — scaled up, and treated with respect.

## Start here
| If you want… | Read |
|---|---|
| **The spirit + the shape** | this README |
| **The execution spine (diagrams-first)** | `docs/drive-plan.md` |
| **HV safety (read before anything orange)** | `SECURITY.md` |
| **What it'll cost / where it stands** | `PROJECT.md` |
| **Step-by-step how-to** | `docs/build-guide.md` |
| **First moves (donor hunt + parts)** | `docs/phase1-donor-hunt.md` · `docs/hv-bom.md` |
| **The engineering** | `docs/drivetrain-diagrams.md` · `docs/battery-pack-and-balance.md` · `docs/range-analysis.md` |
| **Timeline** | `docs/stage1-plan.md` (realistic ~5 months, part-time) |

## Where it stands
**Status:** Building — fully planned, not yet started. Leaf path committed; Stage-1 mule is
the next move. Realistic budget to *driving*: **~$3.5–5.5k**.

---

*Why a 944? Front engine, rear transaxle, near-50/50 balance — it's practically begging to
be converted. Pull the engine, drop in a motor, reuse the rest. The car was built for this.*
