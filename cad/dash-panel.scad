// 944 EV — custom DASH PANEL (parametric, flat — laser/CNC acrylic or aluminum)
// Holds the repurposed gauges (see cad/dash-spec.md + docs/dashboard-reuse.md).
// Layout MATCHES cad/dash-panel.svg (gen_previews.py). All dims mm.
// Coords are origin-TOP-LEFT to match the SVG; y is flipped for OpenSCAD below.

panel_w   = 380;
panel_h   = 170;
panel_t   = 4;     // acrylic / aluminum thickness
corner_r  = 10;
mount_d   = 5;     // corner mounting holes
mount_in  = 12;    // mount inset from edges

// Each gauge cutout: [x, y, hole_dia]  (hole_dia = gauge body diameter)
gauges = [
  [ 95,  92, 86],   // speedo  (MPH)        -- transaxle-native
  [285,  92, 86],   // tach    (motor RPM)
  [190,  50, 40],   // CHARGE %             -- was fuel
  [190, 104, 40],   // HV x100 V            -- was oil press
  [150, 148, 34],   // BATT C               -- was oil temp
  [230, 148, 34],   // COOLANT              -- native (EV coolant loop)
];

$fn = 96;

module rrect(w, h, r) {
  hull() for (x = [r, w-r], y = [r, h-r]) translate([x, y]) circle(r);
}

difference() {
  linear_extrude(panel_t) rrect(panel_w, panel_h, corner_r);
  for (g = gauges)
    translate([g[0], panel_h - g[1], -1]) cylinder(d = g[2], h = panel_t + 2);
  for (x = [mount_in, panel_w - mount_in], y = [mount_in, panel_h - mount_in])
    translate([x, y, -1]) cylinder(d = mount_d, h = panel_t + 2);
}

// Export DXF (2D) for laser/waterjet, or STL for CNC. Print dash-panel.svg 1:1
// as a drilling/face template and to check gauge clearance.
