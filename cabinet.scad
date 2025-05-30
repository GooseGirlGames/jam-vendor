standing_height = 100;
screen_diagonal_inches = 27;
wood_thickness = 1.2;
kantholz = 6;
kantholz_poke = 10;

/* bottom box */
// tabletop
tabletop_depth = 40;
tabletop_width = 85;
side_height = standing_height - 2 * wood_thickness;
// bottom
cube([tabletop_width, tabletop_depth, wood_thickness]);
// top
translate([0, 0, standing_height - wood_thickness])
cube([tabletop_width, tabletop_depth, wood_thickness]);
// front
translate([0, 0, wood_thickness])
cube([tabletop_width, wood_thickness, standing_height - 2 * wood_thickness]);
// back
translate([0, tabletop_depth - wood_thickness, wood_thickness])
cube([tabletop_width, wood_thickness, side_height]);
// left
translate([0, wood_thickness, wood_thickness])
cube([wood_thickness, tabletop_depth - 2 * wood_thickness, standing_height - 2 * wood_thickness]);
// right
translate([tabletop_width - wood_thickness, wood_thickness, wood_thickness])
cube([wood_thickness, tabletop_depth - 2 * wood_thickness, standing_height - 2 * wood_thickness]);

// Kantholz my beloved
kantholz_dx = tabletop_width - kantholz - 2 * wood_thickness;
kantholz_dy = - 2 * wood_thickness - kantholz;
kantholz_height = standing_height + kantholz_poke - wood_thickness;
translate([wood_thickness, wood_thickness, wood_thickness])
cube([kantholz, kantholz, kantholz_height - kantholz_poke - wood_thickness]);
translate([wood_thickness, wood_thickness + tabletop_depth + kantholz_dy, wood_thickness])
cube([kantholz, kantholz, kantholz_height]);
translate([wood_thickness + kantholz_dx, wood_thickness, wood_thickness])
cube([kantholz, kantholz, kantholz_height]);
translate([wood_thickness + kantholz_dx, wood_thickness + tabletop_depth + kantholz_dy, wood_thickness])
cube([kantholz, kantholz, kantholz_height]);

// monitors
bezel = 0.5;
padding = 2 * bezel;
screen_aspect = 16/9;
in_to_cm = 2.54;
screen_diagonal = screen_diagonal_inches * in_to_cm;
screen_height = bezel + screen_diagonal / sqrt(1 + (screen_aspect)^2);
screen_width = bezel + screen_aspect * screen_height;
height_bottom = padding + standing_height;
screen_dy = 3 * wood_thickness + kantholz;
screen_dx = 2 * wood_thickness;
translate([screen_dx, tabletop_depth - screen_dy, height_bottom])
cube([screen_width, 1, screen_height]);
translate([screen_dx, tabletop_depth - screen_dy, height_bottom + padding + screen_height])
cube([screen_width, 1, screen_height]);
top_screen_top = height_bottom + padding + 2 * screen_height;

top_wall_height = top_screen_top - standing_height + padding;

// monitor walls
translate([0, tabletop_depth - wood_thickness, standing_height])
cube([tabletop_width, wood_thickness, top_wall_height]);
translate([wood_thickness, tabletop_depth - wood_thickness - kantholz - wood_thickness, standing_height])
cube([tabletop_width - 2 * wood_thickness, wood_thickness, top_wall_height]);

// left side wall
translate([0, 0, standing_height])
cube([wood_thickness, tabletop_depth, top_wall_height]);

// right side wall (inner)
translate([screen_width + 4 * padding, wood_thickness, standing_height])
cube([wood_thickness, tabletop_depth - 3 * wood_thickness - kantholz, top_wall_height]);

// right side wall (outer)
translate([tabletop_width - wood_thickness, wood_thickness, standing_height])
cube([wood_thickness, tabletop_depth - 2 * wood_thickness, top_wall_height]);

// front wall
front_wall_x = screen_width + 4 * padding;
translate([front_wall_x, 0, standing_height])
cube([tabletop_width - front_wall_x, wood_thickness, top_wall_height]);
