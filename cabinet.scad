standing_height = 100;
screen_diagonal_inches = 27;
wood_thickness = 1.2;

/* monitors */
/*
bezel = 0.5;
padding = 2 * bezel;
screen_aspect = 16/9;
in_to_cm = 2.54;
screen_diagonal = screen_diagonal_inches * in_to_cm;
screen_height = bezel + screen_diagonal / sqrt(1 + (screen_aspect)^2);
screen_width = bezel + screen_aspect * screen_height;
height_bottom = padding + standing_height;
translate([0, 0, height_bottom])
cube([screen_width, 1, screen_height]);
translate([0, 0, height_bottom + padding + screen_height])
cube([screen_width, 1, screen_height]);
*/

// tabletop
tabletop_depth = 40;
tabletop_width = 80;
tabletop_thickness = wood_thickness;
// bottom
cube([tabletop_width, tabletop_depth, tabletop_thickness]);
// tom
translate([0, 0, standing_height - tabletop_thickness])
cube([tabletop_width, tabletop_depth, tabletop_thickness]);
// front
translate([0, 0, tabletop_thickness])
cube([tabletop_width, tabletop_thickness, standing_height - 2 * tabletop_thickness]);
// back
translate([0, tabletop_depth - tabletop_thickness, tabletop_thickness])
cube([tabletop_width, tabletop_thickness, standing_height - 2 * tabletop_thickness]);
// left
translate([0, tabletop_thickness, tabletop_thickness])
cube([tabletop_thickness, tabletop_depth - 2 * tabletop_thickness, standing_height - 2 * tabletop_thickness]);
// right
translate([tabletop_width - tabletop_thickness, tabletop_thickness, tabletop_thickness])
cube([tabletop_thickness, tabletop_depth - 2 * tabletop_thickness, standing_height - 2 * tabletop_thickness]);
