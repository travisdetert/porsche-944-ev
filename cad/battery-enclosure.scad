// 944 EV — BATTERY ENCLOSURE  (parametric, folded/welded sheet box)
// Two needed: FRONT box (6 modules) + MAIN box (8 modules). Set the layout +
// bay limits below. All dims mm. NO 3D printer here -> fit-check with a CARDBOARD
// mock at the EXTERNAL dims this echoes. Spec: cad/battery-enclosure-spec.md.

/* ---- WHICH BOX (set the module grid) ---- */
modules_x = 4;    // modules along the car's length
modules_y = 2;    // modules across the car's width
layers    = 1;    // vertical layers (watch ground clearance!)

/* ---- MODULE size (Tesla 5.3 kWh default; MEASURE Leaf for Stage 1) ---- */
mod_L = 685;  // module length   (Tesla ~685 -- the tight dimension in the 944!)
mod_W = 300;  // module width
mod_H = 85;   // module height

/* ---- ENCLOSURE ---- */
clear    = 8;     // clearance around modules
wall_t   = 3;     // aluminum sheet thickness (light, ADR-0011)
floor_t  = 3;
flange_w = 25;    // mounting-flange width (bolts to frame rails)
flange_t = 3;
vent_d   = 25;    // vent port diameter
vents    = 2;     // vents per long side

/* ---- BAY LIMIT (MEASURE on the car) — sanity check only ---- */
bay_L = 0;  // MEASURE bay length (0 = skip the check)
bay_W = 0;  // MEASURE bay width
bay_H = 0;  // MEASURE bay depth (mind ground clearance + skid plate)

// ---- derived ----
in_L  = modules_x*mod_L + (modules_x+1)*clear;
in_W  = modules_y*mod_W + (modules_y+1)*clear;
in_H  = layers*mod_H + clear + 20;          // +20 for busbars/wiring
ext_L = in_L + 2*wall_t;
ext_W = in_W + 2*wall_t;
ext_H = in_H + floor_t;

echo(str("INTERNAL  L=", in_L,  "  W=", in_W,  "  H=", in_H,  " mm"));
echo(str("EXTERNAL  L=", ext_L, "  W=", ext_W, "  H=", ext_H, " mm  (+", flange_w, " flanges)"));
if (bay_L > 0)
  echo(str("BAY FIT?  L ", ext_L, "/", bay_L, "  W ", ext_W, "/", bay_W,
           "  H ", ext_H, "/", bay_H, "   (external must be <= bay)"));

$fn = 48;

module enclosure() {
  difference() {
    union() {
      difference() {                                  // open-top tray
        cube([ext_L, ext_W, ext_H]);
        translate([wall_t, wall_t, floor_t]) cube([in_L, in_W, in_H + 1]);
      }
      translate([-flange_w, 0, ext_H - flange_t]) cube([flange_w, ext_W, flange_t]);
      translate([ext_L, 0, ext_H - flange_t])     cube([flange_w, ext_W, flange_t]);
    }
    for (s = [0, 1], i = [1 : vents])               // low vent ports
      translate([i*ext_L/(vents+1), s*ext_W, floor_t + vent_d])
        rotate([90, 0, 0]) cylinder(d = vent_d, h = wall_t + 2, center = true);
  }
  %for (xi = [0:modules_x-1], yi = [0:modules_y-1], zi = [0:layers-1])  // module ghosts
    translate([wall_t + clear + xi*(mod_L+clear),
               wall_t + clear + yi*(mod_W+clear),
               floor_t + zi*mod_H])
      cube([mod_L, mod_W, mod_H]);
}

enclosure();
