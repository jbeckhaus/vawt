from dataclasses import dataclass

from build123d import *
from ocp_vscode import show_all
import math


outer_diameter = 40 * MM
rod_thread_length = 20 * MM
thread_major_diameter = 33 * MM
thread_minor_diameter = 29.211 * MM
thread_pitch = 3.5 * MM
thread_angle = 60

base_plate_thickness = 2 * MM
top_cover_thickness = 2 * MM

motor_space_diameter = 62 * MM
nema_17_width = 42 * MM
nema_17_height = 42 * MM 
nema_17_holes_spacing = 31 * MM
screw_holes_diameter = 3 * MM
screw_holes_depth = 10 * MM
shaft_hole_diameter = 30 * MM

assert outer_diameter > thread_major_diameter    

with BuildPart() as rod_top:
    
    r_helix = thread_minor_diameter / 2

    Cone(
        bottom_radius=outer_diameter/2,
        top_radius=motor_space_diameter/2,
        height=rod_thread_length,
        align=(Align.CENTER, Align.CENTER, Align.MIN),  
    )
    
    with BuildLine() as path:
        Helix(pitch=thread_pitch, height=rod_thread_length, radius=r_helix)
    
    with BuildSketch(path.line ^ 0) as thread_tooth:
        thread_depth = (thread_major_diameter - thread_minor_diameter) / 2 
        trapezoid_angle = 90 - (thread_angle/2)
        angle_space = thread_depth / math.tan(math.radians(trapezoid_angle))
        root = (thread_pitch - 2 * angle_space ) / 2
        bottom_width = thread_pitch - root
        
        Trapezoid(
            width=bottom_width, 
            height=thread_depth,  
            left_side_angle = trapezoid_angle,
            rotation=90)
        
    sweep(path=path.line, is_frenet=True, transition=Transition.ROUND, mode=Mode.SUBTRACT)

    Cylinder(
        radius = thread_minor_diameter/2 ,
        height = rod_thread_length , 
        align=(Align.CENTER, Align.CENTER, Align.MIN),
        mode=Mode.SUBTRACT
    )

    with BuildSketch(rod_top.faces().sort_by(Axis.Z)[-1]):
        offset_to_outer_thread_diameter = 5 * MM 
        Circle(motor_space_diameter/2)
        Circle((thread_major_diameter - offset_to_outer_thread_diameter)/2, mode=Mode.SUBTRACT)
    extrude(amount=base_plate_thickness)
    
    with BuildSketch(rod_top.faces().sort_by(Axis.Z)[-1]): 
        Circle(motor_space_diameter/2)
        Rectangle(nema_17_width, nema_17_width, mode=Mode.SUBTRACT) 
    extrude(amount = nema_17_height)
    
    with BuildSketch(rod_top.faces().sort_by(Axis.Z)[-1]):
        with BuildLine(mode=Mode.PRIVATE):
            selected_edge = rod_top.edges().filter_by(lambda a: a.length == nema_17_width).sort_by(Axis.Z)[-1]
            top_outer_circle = rod_top.edges().filter_by(GeomType.CIRCLE).sort_by(Axis.Z)[-1]
            selected_point = selected_edge.center()
            helper_line = IntersectingLine(start = selected_point, direction = (-1, 0, 0), other=top_outer_circle.edge())
        with Locations(helper_line.center()):
            Circle(radius=screw_holes_diameter/2)
        with Locations(helper_line.center().rotate(Axis.Z, 90)):
            Circle(radius=screw_holes_diameter/2)
        with Locations(helper_line.center().rotate(Axis.Z, 180)):
            Circle(radius=screw_holes_diameter/2) 
        with Locations(helper_line.center().rotate(Axis.Z, 270)):
            Circle(radius=screw_holes_diameter/2)
    extrude(amount=-screw_holes_depth, mode=Mode.SUBTRACT)
    

with BuildPart() as cover: 
    with BuildSketch(): 
        Circle(radius=motor_space_diameter/2)
    extrude(amount=top_cover_thickness)
    with BuildSketch(cover.faces().sort_by(Axis.Z)[-1]):
        with Locations(helper_line.center()):
            Circle(radius=screw_holes_diameter/2 + 0.2)
        with Locations(helper_line.center().rotate(Axis.Z, 90)):
            Circle(radius=screw_holes_diameter/2 + 0.2)
        with Locations(helper_line.center().rotate(Axis.Z, 180)):
            Circle(radius=screw_holes_diameter/2 + 0.2) 
        with Locations(helper_line.center().rotate(Axis.Z, 270)):
            Circle(radius=screw_holes_diameter/2 + 0.2)
        Circle(radius=shaft_hole_diameter/2)
        helper_rectangle = Rectangle(width = nema_17_holes_spacing, height=nema_17_holes_spacing, mode=Mode.PRIVATE)
        with Locations([x.start_point() for x in helper_rectangle.edges()]):
            Circle(radius=screw_holes_diameter/2 + 0.2)
    extrude(amount= -top_cover_thickness, mode=Mode.SUBTRACT)
    selection = cover.edges().filter_by(GeomType.CIRCLE).filter_by(lambda r: r.radius == screw_holes_diameter/2 + 0.2).sort_by(Axis.Z)[-8:]
    chamfer(selection, 0.5 * MM)
cover.part.position = (0,0,rod_top.faces().sort_by(Axis.Z)[-1].center().Z + 10)

show_all()
