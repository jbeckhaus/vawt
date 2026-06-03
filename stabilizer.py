from dataclasses import dataclass

from build123d import *
from ocp_vscode import show_all
import math


wing_length = 10 * CM
wing_angle = 60.

rod_height = 10 * MM
rod_width = 10 * MM
rod_tolerance = 0.1 * MM
interface_length = 10 * MM


with BuildPart() as stabilizer_wing:
    with BuildSketch() as ellipse:
        Ellipse(10., 2.)
    extrude(amount=wing_length)
    
with BuildPart() as middle: 
    with BuildSketch(Plane.XZ):
        Ellipse(10.,8.)
    extrude(amount=interface_length)
    
with BuildPart() as rod_connection: 
    with BuildSketch(Plane.XZ): 
        Rectangle(rod_width + rod_tolerance, rod_height + rod_tolerance, rotation = 45)
    extrude(amount=-20. * MM)

upper_wing = Rot(-90. + wing_angle, 0, 0) * stabilizer_wing.part
lower_wing = mirror(upper_wing, Plane.XY)
middle.part = Pos(0, interface_length * 2 / 3, 0) * middle.part
rod_connection.part = Pos(0, -10, 0) * rod_connection.part
substract_block = Pos(0, math.sin(math.radians(90-wing_angle))*wing_length - 2., 0.) * Box(20, 20, 2*wing_length, align=(Align.CENTER, Align.MIN, Align.CENTER))

stabilizer = upper_wing + lower_wing + middle.part - rod_connection.part - substract_block

export_stl(stabilizer, "stabilizer.stl")


show_all()