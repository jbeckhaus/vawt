from dataclasses import dataclass

from build123d import *
from ocp_vscode import show_all
import importlib
import math

screw_lib = importlib.import_module('123DScrew.123DScrew')


outer_diameter = 40 * MM
rod_thread_length = 20 * MM
thread_major_diameter = 33 * MM
thread_minor_diameter = 29.211 * MM
thread_pitch = 3.5 * MM
thread_angle = 60

base_plate_thickness = 2 * MM

motor_space_diameter = 62 * MM
nema_17_lengh = 42 * MM
nema_17_width = 42 * MM
nema_17_height = 42 * MM 

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
        Rectangle(nema_17_lengh, nema_17_width, mode=Mode.SUBTRACT) 
    extrude(amount = nema_17_height)
    
    

show_all()
