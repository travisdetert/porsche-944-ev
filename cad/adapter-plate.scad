// 944 EV — EM57 -> torque-tube ADAPTER PLATE  (parametric)
// All dims in mm. Replace every "// MEASURE" placeholder with the real value
// measured during teardown (step 000) and donor extraction (step 007).
// Export: File > Export > DXF (2D profile) or STL. Spec: cad/adapter-spec.md.
//
// The plate does two jobs:
//   (a) bolt the EM57 motor face to the torque-tube bellhousing flange
//   (b) locate both CONCENTRIC (centered by register diameters)
// The coupler that joins the shafts is a SEPARATE part (see adapter-spec.md).

/* ---------- MEASURE THESE (placeholders!) ---------- */
plate_OD         = 200;  // MEASURE: outer diameter (>= larger bolt circle + edge)
plate_t          = 16;   // MEASURE/CHOOSE: thickness (stiffness vs length)

motor_bc         = 150;  // MEASURE: EM57 face bolt-circle diameter
motor_bolts      = 6;    // MEASURE: EM57 face bolt count
motor_bolt_d     = 9;    // MEASURE: EM57 bolt clearance hole dia
motor_reg_d      = 110;  // MEASURE: EM57 spigot/register dia (centers the motor)
motor_reg_depth  = 4;    // MEASURE: register counterbore depth

bell_bc          = 170;  // MEASURE: bellhousing bolt-circle diameter
bell_bolts       = 8;    // MEASURE: bellhousing bolt count
bell_bolt_d      = 11;   // MEASURE: bellhousing bolt clearance hole dia
bell_reg_d       = 0;    // MEASURE: bellhousing register dia (0 = none)

bore_d           = 60;   // MEASURE: central bore (coupler/pilot clearance)
/* -------------------------------------------------- */

$fn = 160;

module bolt_ring(bc, n, d) {
    for (i = [0 : n-1])
        rotate([0, 0, i * 360 / n])
            translate([bc/2, 0, 0]) circle(d = d);
}

module adapter() {
    difference() {
        cylinder(d = plate_OD, h = plate_t);
        // central bore (through)
        translate([0, 0, -1]) cylinder(d = bore_d, h = plate_t + 2);
        // motor face bolt holes (through)
        translate([0, 0, -1]) linear_extrude(plate_t + 2)
            bolt_ring(motor_bc, motor_bolts, motor_bolt_d);
        // bellhousing bolt holes (through)
        translate([0, 0, -1]) linear_extrude(plate_t + 2)
            bolt_ring(bell_bc, bell_bolts, bell_bolt_d);
        // motor register counterbore (bottom face = motor side)
        if (motor_reg_d > 0)
            translate([0, 0, -0.01]) cylinder(d = motor_reg_d, h = motor_reg_depth);
        // bellhousing register counterbore (top face) if present
        if (bell_reg_d > 0)
            translate([0, 0, plate_t - motor_reg_depth + 0.01])
                cylinder(d = bell_reg_d, h = motor_reg_depth);
    }
}

adapter();

// TIP: comment out adapter() and use `projection(cut=false) adapter();`
// to export a clean 2D DXF of the hole/profile pattern for the shop.
