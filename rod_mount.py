from dataclasses import dataclass

from build123d import *
from ocp_vscode import show_all
import importlib

screw_lib = importlib.import_module('123DScrew.123DScrew')


outer_diameter = 40 * MM
rod_thread_length = 10 * MM
thread_major_diameter = 33 * MM
thread_pitch = 3.5 * MM


assert outer_diameter > thread_major_diameter

with BuildPart() as rod_top:
    insert = screw_lib.threaded_insert(major_d=thread_major_diameter, pitch=thread_pitch, length=rod_thread_length, thickness=outer_diameter-thread_major_diameter,
                         tolerance_scale=screw_lib.TOL(0.5, thread_major_diameter))
    
    
# flat bed slight indent with screw holes for final motor cover thingy.   



show_all()
