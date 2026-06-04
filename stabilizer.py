from dataclasses import dataclass

from build123d import *
from ocp_vscode import show_all
import math


wind_foil_height = 30.35 * CM
wing_angle = 55.
wing_thickness_r = 4. * MM
wing_width_r = 12. * MM
wing_length = ((wind_foil_height + wing_thickness_r * MM) / 2) / math.cos(math.radians(90. - wing_angle))

rod_height = 10 * MM
rod_width = 10 * MM
rod_tolerance = 0.08 * MM
interface_length = 40 * MM


with BuildPart() as stabilizer_wing:
    with BuildSketch() as ellipse:
        Ellipse(wing_width_r, wing_thickness_r)
    extrude(amount=wing_length)
    
with BuildPart() as middle: 
    with BuildSketch(Plane.XZ):
        Ellipse(wing_width_r,8.)
    extrude(amount=interface_length)
    
with BuildPart() as rod_connection: 
    with BuildSketch(Plane.XZ): 
        Rectangle(rod_width + rod_tolerance, rod_height + rod_tolerance, rotation = 45)
    extrude(amount=interface_length)

upper_wing = Rot(-90. + wing_angle, 0, 0) * stabilizer_wing.part
lower_wing = mirror(upper_wing, Plane.XY)
middle.part = Pos(0, interface_length * 2 / 3, 0) * middle.part
rod_connection.part = Pos(0, interface_length * 2 / 3, 0) * rod_connection.part
substract_block = Pos(0, math.sin(math.radians(90-wing_angle))*wing_length - 2., 0.) * Box(wing_width_r * 2, wing_width_r * 2, wind_foil_height, align=(Align.CENTER, Align.MIN, Align.CENTER))

stabilizer = upper_wing + lower_wing + middle.part - rod_connection.part - substract_block

export_stl(stabilizer, "stabilizer.stl")


# --------------------------------------------------
# Joint parameters
# --------------------------------------------------

pin_diameter = 5 * MM
pin_radius = pin_diameter / 2

pin_length = 15 * MM
hole_clearance = 0.2 * MM

hole_radius = (pin_diameter + hole_clearance) / 2

# keep a substantial center section
center_height = 80 * MM

split_z_top = center_height / 2
split_z_bottom = -center_height / 2

# --------------------------------------------------
# Split stabilizer into 3 pieces
# --------------------------------------------------

bbox = stabilizer.bounding_box()

upper_cut = Box(
    bbox.size.X + 100 * MM,
    bbox.size.Y + 100 * MM,
    bbox.size.Z,
    align=(Align.CENTER, Align.CENTER, Align.MIN),
)

upper_cut = Pos(
    0,
    0,
    split_z_top
) * upper_cut

lower_cut = Box(
    bbox.size.X + 100 * MM,
    bbox.size.Y + 100 * MM,
    bbox.size.Z,
    align=(Align.CENTER, Align.CENTER, Align.MAX),
)

lower_cut = Pos(
    0,
    0,
    split_z_bottom
) * lower_cut

upper_part = stabilizer & upper_cut
lower_part = stabilizer & lower_cut

center_box = Box(
    bbox.size.X + 100 * MM,
    bbox.size.Y + 100 * MM,
    center_height,
    align=(Align.CENTER, Align.CENTER, Align.CENTER),
)

center_part = stabilizer & center_box

# --------------------------------------------------
# Alignment pins
# --------------------------------------------------

pin = Cylinder(pin_radius, pin_length)

holes = []

lower_hole = Cylinder(pin_radius + rod_tolerance, pin_length + rod_tolerance, rotation=(90-wing_angle,0 ,0 ), mode=Mode.PRIVATE)
holes.append(Pos(-0.5 * wing_width_r,math.tan(math.radians(90 - wing_angle))* abs(split_z_bottom),split_z_bottom) * lower_hole)
holes.append(Pos(0.5 * wing_width_r,math.tan(math.radians(90 - wing_angle))* abs(split_z_bottom),split_z_bottom) * lower_hole)
upper_hole = Cylinder(pin_radius + rod_tolerance, pin_length + rod_tolerance, rotation=(90+wing_angle, 0, 0), mode=Mode.PRIVATE)
holes.append(Pos(-0.5 * wing_width_r,math.tan(math.radians(90 - wing_angle))* abs(split_z_top),split_z_top) * upper_hole)
holes.append(Pos(0.5 * wing_width_r,math.tan(math.radians(90 - wing_angle))* abs(split_z_top),split_z_top) * upper_hole)

lower_part = lower_part - holes
upper_part = upper_part - holes

center_part = center_part - holes

# --------------------------------------------------
# Export
# --------------------------------------------------

export_stl(upper_part, "stabilizer_upper.stl")
export_stl(center_part, "stabilizer_center.stl")
export_stl(lower_part, "stabilizer_lower.stl")
export_stl(pin, "pin.stl")



show_all()