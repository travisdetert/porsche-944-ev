# 944 EV — Step-by-Step Build Guide (Stage 1 Mule)

The detailed how-to for executing the Leaf-path mule, phase by phase. Pairs with the
high-level `build-order.md` (sequence), `stage1-plan.md` (timeline), `hv-bom.md` (parts),
and **`SECURITY.md` (HV safety — non-negotiable, read first).**

**Conventions:** ⚠️ = HV/safety-critical. ✅ = verification gate (don't proceed until it
passes). 🪤 = common pitfall.

---

## Phase 2 — Teardown & adapter

### 2A. Strip the ICE driveline
**Goal:** remove the engine and fuel system, exposing the torque tube for the adapter.
**Tools:** engine hoist, transmission jack, metric sockets/wrenches, penetrating oil.

1. Disconnect the 12 V battery; relieve fuel pressure; drain coolant and fuel.
2. Remove intake, exhaust, accessories, then unbolt the engine from its mounts.
3. **Separate the engine from the torque tube** at the bellhousing; lift the engine out.
   - 🪤 944 fasteners are 39 years old — soak with penetrant, expect a few to fight you.
4. Remove the **fuel tank, lines, and the radiator/cooling** you won't reuse (keep a cabin-
   heat plan and the inverter-cooling loop in mind).
5. **Weigh the stripped car** (corner scales or a single-pad) — your balance baseline.
6. Inspect the **torque tube and transaxle** while exposed: bearings, mounts, seals. Fix
   now — it's never this accessible again.

✅ **Gate:** engine out, torque-tube input flange clean and measurable, car weighed.

### 2B. Design & outsource the adapter (the critical-path item — start at Phase 1)
**Goal:** a machined plate + coupler joining the EM57 to the torque-tube driveshaft,
concentric. **No off-the-shelf 944 part exists** (see `drivetrain-diagrams.md` §3).

1. **Measure:** EM57 mounting face/bolt pattern + output shaft; torque-tube bellhousing
   flange + driveshaft input. Record everything; photograph with a scale.
2. **Design** (or commission) the adapter: a plate matching both bolt patterns + a
   **splined/keyed coupler** mating the EM57 output to the driveshaft. The plate must
   locate the motor so the shafts are **concentric and at the right working length**.
   - 🪤 The EM57 has an **integrated reduction-gear output, not a plain shaft** — the
     coupler is the tricky part; get it right or you get driveline vibration.
3. **Quote at 2 machine shops**; pick one that commits to a date, keep the other as backup.
4. **Expect a test-fit and one revision** — build it into the schedule (Phase 2 = 5 weeks
   expected for this reason).

✅ **Gate:** adapter + coupler in hand, dry-fits to both the EM57 and the bellhousing flange.

---

## Phase 3 — Mechanical mount

**Goal:** EM57 bolted to the transaxle via the adapter, driveline true.
**Tools:** hoist, dial indicator, torque wrench, thread locker.

1. Bolt the **coupler** to the EM57 output and the **adapter plate** to the motor face.
2. Offer the assembly to the **torque-tube bellhousing**; bolt up.
3. **Check concentricity/runout** with a dial indicator on the driveshaft; rotate by hand.
   - ✅ Runout within spec, **no bind, smooth rotation by hand**. If it binds or wobbles,
     stop — re-shim/re-machine. This is why we proved fit before building the pack.
4. Fabricate/secure the **motor mounts** to the factory crossmember hardpoints (not
   sheetmetal). Torque to spec, thread-lock.
5. Plumb the **inverter/motor coolant loop** (reuse the Leaf pump + a small radiator).

✅ **Gate:** motor mounted, driveline turns freely and true by hand, coolant loop sealed.

---

## Phase 4 — Battery & pack install (Stage 1 = donor Leaf pack)

**Goal:** the donor pack mounted, safe, and ready to wire. Stage 1 uses the **whole donor
Leaf pack** (matched to the inverter) — minimal fabrication vs. the Stage-2 Tesla build.

⚠️ De-energize and verify dead before handling the pack (`SECURITY.md`).

1. **Locate the pack** per `battery-pack-and-balance.md` — for the mule, the simplest safe
   mounting that keeps it **low and secured** (the fuel-tank bay floor is ideal). You're
   not chasing perfect 50/50 yet; you're proving the drivetrain.
2. **Mount to structure, not sheetmetal** — frame into floor/tunnel hardpoints; the pack
   must not move in a crash.
3. Keep the pack's **case sealed**; route its **HV cables** with strain relief and orange loom.
4. Keep the Leaf **LBC (battery controller)** wired to the pack — ZombieVerter reads it for
   Stage-1 BMS (a real simplification; no separate BMS to build yet).

✅ **Gate:** pack mechanically secure, case intact, LBC connected, HV terminals covered.

---

## Phase 5 — Electrical integration

**Goal:** wire the HV safety loop, control, charging, and 12 V — methodically, off until
the very end. ⚠️ This whole phase is HV-critical; build it **de-energized**.

### 5A. HV power path (per `drivetrain-diagrams.md` §6 + `hv-bom.md`)
1. Build the **HV junction**: pack → **MSD** → **main fuse** → **main + precharge
   contactors** (with resistor) → inverter. Mount on a plate; label everything.
2. Crimp all **2/0 lugs** with a hydraulic crimper; ⚠️ a bad crimp is a fire — heat-shrink
   and tug-test every one.
3. Tap the **DC-DC (PDM)** off the HV bus → 12 V system.
4. Wire the **charger (PDM)** ← charge port, feeding the pack through the BMS/contactor logic.
5. ⚠️ **Isolation check (megger)**: HV must be isolated from chassis before any power-up.

### 5B. Low-voltage & control
1. Install the **ZombieVerter VCU**; wire it to the inverter, contactors, PDM, and pedal.
2. Restore **12 V accessories**, lights, and the **brake booster** (vacuum pump or iBooster
   — no engine vacuum anymore 🪤).
3. Wire **interlocks**: inertia/crash switch + BMS-healthy + "drive" in series with the
   contactor coil — **no torque unless all true**.

### 5C. Configure the ZombieVerter (bench first)
1. Flash/parameterize per the **openinverter wiki** for your EM57 inverter generation.
2. Set the **pedal map**, the **precharge timing**, contactor control, and **CAN** to the
   Leaf inverter + LBC + PDM.
3. **Bench-test the logic on low voltage** before connecting the full pack — verify
   precharge → main sequence and pedal response with no driveline load.
   - ✅ Gate: contactors sequence correctly; VCU sees pedal, inverter, BMS.

✅ **Phase gate:** isolation check passes; control logic verified on the bench; all HV
terminations covered and labeled.

---

## Phase 6 — Commissioning, first drive & shakedown

⚠️ **The most dangerous phase.** Follow the **first-power-up procedure in `SECURITY.md`**:
car on stands, extinguisher, helper at a kill switch, one-hand rule.

### 6A. First power-up (on stands)
1. De-energized pre-flight: torque check, nothing loose, isolation re-checked.
2. Insert MSD → key on → watch the **precharge → main** sequence; confirm bus voltage rises
   correctly and contactors don't chatter.
   - 🪤 Any chatter/smoke/fault → **kill power immediately**, diagnose de-energized.
3. **Spin the motor under light throttle on stands.** Verify **rotation direction** and
   that the driveline turns smoothly. Test **both directions + regen**.
   - ✅ Gate: correct rotation, smooth driveline, no faults, temps stable.

### 6B. First drive
1. Low-speed drive in a **safe, private area**. Watch pack voltage, current, temps.
2. Tune pedal feel, regen, and any current limits in the VCU.
3. Iterate — fix what surfaces (this is where mules bite; budget real debug time).

### 6C. Shakedown & sort
1. **Brakes & suspension** for the added weight — bed-in brakes; uprated springs/dampers
   if it wallows.
2. **Charge test:** full L2 charge cycle via the PDM; confirm BMS taper/balance.
3. Drive a real **grocery loop**; log **Wh/mi** (feeds `range-analysis.md`).
4. **Registration/inspection** (parallel track — partly out of your hands; drive private
   property until cleared).

✅ **Stage 1 done:** EM57 on the transaxle spins under power; runs on the donor pack
through the HV loop; charges; drives a 5–15 mi grocery loop. (See `mvp-mule.md`.)

---

## Then: Stage 2 (the pack swap)
Revisit **Phase 4 only** — build the **Tesla 14S1P / 74 kWh** pack
(`battery-pack-and-balance.md`), swap the **BMS to simpBMS**, re-check fuse sizing for
319 V, and corner-balance 7/7. Motor, inverter, VCU, adapter, and HV wiring all carry
forward. The mule becomes the 150-mile car.

---

## Document map
- **Safety:** `SECURITY.md` (read before any HV work)
- **Parts:** `hv-bom.md` · **Donor:** `phase1-donor-hunt.md`
- **Design:** `drivetrain-diagrams.md` · `battery-pack-and-balance.md` · `range-analysis.md`
- **Plan:** `build-order.md` (sequence) · `stage1-plan.md` (timeline) · `mvp-mule.md` (why staged)
- **Charter:** `../PROJECT.md`
