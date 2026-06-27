# Next Steps — your action runbook

**Where you are:** planning is complete (full repo). Teardown is the active move. Nothing
bought yet. **How to use this:** work top to bottom. Each step has an **action**, the **gate**
that means it's done, and the **doc / task #** to reference. Don't skip the gates.

> This is the one-page overview. The detailed, self-contained step files live in **`../steps/`**
> (`000-pull-the-engine.md` … `015-register.md`) — each with its own actions, gate, blockers, and refs.

---

## ⛏️ NOW — this week (~$0 out of pocket)

- [ ] **1. Pull the engine** — task #8
  - Disconnect the 12 V battery; relieve fuel pressure; drain fluids.
  - Strip and set aside **to sell**: engine, intake, exhaust, ECU, fuel system, alt/starter/AC.
  - Separate the engine from the torque tube; hoist it out. Pull the fuel tank.
  - **Measure** the front bay + fuel-tank bay + torque-tube flange; photograph with a ruler.
  - **Weigh** the stripped car.
  - ✅ *engine out · bays measured · gas parts listed for sale* — `build-guide.md` §2A, `parts-inventory.md`

- [ ] **2. PF1 — confirm ZombieVerter supports your target Leaf year** (openinverter wiki),
  *before* buying a donor — task #1 — `phase1-donor-hunt.md`

- [ ] **3. PF3 — email 2 machine shops** the adapter concept + your flange photos for quotes;
  line up a backup — task #3 — `build-guide.md` §2B

- [ ] **4. PF4 — get HV safety gear** (Class-0 gloves, CAT III DC meter, megger, DC extinguisher)
  and rehearse the de-energize procedure — task #4 — **`SECURITY.md`**

- [ ] **5. List the gas parts for sale** — this is your funding — `parts-inventory.md`

---

## 🛒 BUY — only once Pre-Flight (1–4) is green

- [ ] **6. Hunt the donor Leaf** (2013–2017 EM57); run **LeafSpy**, record SOH > 70 % — task #5
- [ ] **7. PF2 — pull the EM57 inverter cap spec** → size the DC fuse + precharge — task #2 — `hv-bom.md`
- [ ] **8. Extract & label everything** from the donor (**de-energize first!**) — task #6
- [ ] **9. Batch-order** ZombieVerter + HV bits + small parts (reuse donor HV where you can) — task #7 — `parts-shopping-list.md`

---

## 🔧 BUILD

- [ ] **10. Machine + dry-fit the adapter** — gate G2 — task #9
- [ ] **11. Mount the EM57; verify driveline true by hand** — gate G3 — task #10
- [ ] **12. Mount the donor pack; pass the megger isolation check** — gate G4 — task #11
- [ ] **13. Wire the HV loop + bench-verify ZombieVerter control** — gate G5 — task #12 — `build-guide.md` §5

---

## ⚡ DRIVE

- [ ] **14. First power-up on stands** — rotation / temps / no faults — gate G6 — task #13 — `SECURITY.md` (first power-up)
- [ ] **15. First drive + grocery loop** — gate G7 = **DONE** — task #14 — `mvp-mule.md`
- [ ] **16. Register / inspect** (runs in parallel) — task #15

---

## Golden rules
- **Don't buy anything** until the engine's out, **PF1 is green**, and the bays are measured.
- **Reuse the donor's HV system** (cheapest path) and **sell the gas parts** (funds the donor).
- **Never cheap out** on HV gloves, the fuse rating, or adapter alignment.
- **Read `SECURITY.md` before anything orange. Never work live HV alone.**

## Come back to me when…
- **Engine's out + bays measured** → I fold the real numbers in and sharpen the SVGs.
- **Your search budget resets** → I close PF1/PF2 and turn the shopping list into a live cart.
- **You pick a start month** → I re-anchor the whole timeline to real dates.

> Detail behind every step: `drive-plan.md` (gates) · `build-guide.md` (how) ·
> `stage1-plan.md` (timeline) · `procurement-plan.md` (money). Tracked: tasks #1–#15.
