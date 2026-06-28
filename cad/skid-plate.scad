// 944 EV — SKID PLATE (parametric, flat with turned-up lip)
// Protects the low main battery box from road strikes (the box sits low, ADR-0005/0011).
// Sacrificial + replaceable. All dims mm -- size to the MAIN box footprint + margin.
// Steel preferred under the pack (strike resistance). Preview: cad/skid-plate.svg. Gate G4.

plate_L  = 640;   // box footprint length + margin (MEASURE main box / bay)
plate_W  = 560;   // box footprint width  + margin
plate_t  = 4;     // 3-5 mm steel
corner_r = 30;
bolt_d   = 9;
inset    = 18;    // bolt inset from edge
n_long   = 3;     // bolts along each long edge
n_wide   = 2;     // bolts along each short edge
lip_h    = 15;    // turned-up edge lip (deflects strikes)
lip_t    = 3;

$fn = 56;

module rr(w, h, r) { hull() for (x = [r, w-r], y = [r, h-r]) translate([x, y]) circle(r); }

difference() {
  union() {
    linear_extrude(plate_t) rr(plate_L, plate_W, corner_r);
    // perimeter lip wall
    linear_extrude(plate_t + lip_h)
      difference() { rr(plate_L, plate_W, corner_r); offset(-lip_t) rr(plate_L, plate_W, corner_r); }
  }
  // long-edge bolts
  for (i = [0 : n_long-1], y = [inset, plate_W - inset])
    translate([inset + i*(plate_L - 2*inset)/(n_long-1), y, -1])
      cylinder(d = bolt_d, h = plate_t + 2);
  // short-edge bolts
  for (j = [0 : n_wide-1], x = [inset, plate_L - inset])
    translate([x, inset + j*(plate_W - 2*inset)/(n_wide-1), -1])
      cylinder(d = bolt_d, h = plate_t + 2);
}
// Export DXF (flat) for laser/waterjet + brake the lip; print skid-plate.svg 1:1 to template.
