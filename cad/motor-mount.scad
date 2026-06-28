// 944 EV — MOTOR MOUNT BRACKET (parametric)
// Ties an EM57 mounting boss to a 944 crossmember hardpoint through a rubber/poly
// isolator, and reacts motor torque. Make 2-3 (mirror as needed). All dims mm --
// MEASURE the motor bosses + crossmember on the car. Steel weldment (or CNC plate
// then weld). Add gussets at the base/upright joint (see spec). Preview: motor-mount.svg.

/* ---- FRAME-SIDE BASE (bolts to crossmember) ---- */
base_L = 90;     // along the crossmember
base_W = 70;     // depth (toward the motor)
base_t = 8;
frame_bolt_d  = 11;
frame_bolt_dx = 60;     // spacing of the 2 frame bolts
iso_bore_d    = 50;     // isolator/bushing pocket through the base (0 = none)

/* ---- MOTOR-SIDE UPRIGHT (bolts to motor boss) ---- */
up_H = 80;
up_t = 8;
motor_bolt_d  = 11;
motor_bolt_dz = 40;     // vertical spacing of the 2 motor bolts
motor_bolt_z0 = 28;     // first motor bolt height above base

$fn = 64;

module mount() {
  // frame base
  difference() {
    cube([base_L, base_W, base_t]);
    for (x = [base_L/2 - frame_bolt_dx/2, base_L/2 + frame_bolt_dx/2])
      translate([x, base_W/2, -1]) cylinder(d = frame_bolt_d, h = base_t + 2);
    if (iso_bore_d > 0)
      translate([base_L/2, base_W/2, -1]) cylinder(d = iso_bore_d, h = base_t + 2);
  }
  // motor upright at the rear edge
  translate([0, base_W - up_t, 0])
    difference() {
      cube([base_L, up_t, up_H]);
      for (z = [motor_bolt_z0, motor_bolt_z0 + motor_bolt_dz])
        translate([base_L/2, up_t + 1, z]) rotate([90, 0, 0])
          cylinder(d = motor_bolt_d, h = up_t + 2);
    }
}

mount();
// Export STL for reference; the real mount is a measured weldment off the car.
