from dataclasses import dataclass

from build123d import *
from ocp_vscode import show_all
from math import *


disk_diameter = 165 * MM
disk_height = 2 * CM
vertical_rods_diameter = 142 * MM
m3_screw_hole_diameter = 3.1 * MM

with BuildPart() as disk:
    Cylinder(
        radius = disk_diameter / 2, 
        height = disk_height
    )
    
         # Rod connection holes 
    for angle in [0, 120, 240]:
        x = (disk_diameter / 4) * cos(radians(angle))
        y = (disk_diameter / 4) * sin(radians(angle))

        with Locations((x, y, disk_height/2)):
            Cylinder(
                radius=m3_screw_hole_diameter / 2,
                height=10,
                mode=Mode.SUBTRACT
            )
            
    for angle in [0, 120, 240]:
        x = (vertical_rods_diameter / 2) * cos(radians(angle+60))
        y = (vertical_rods_diameter / 2) * sin(radians(angle+60))

        with Locations((x, y, disk_height / 2)):
            box = Box(
                20,
                30,
                25,
                rotation=Rotation(0,0,angle+60),
                align=(Align.CENTER, Align.CENTER, Align.MIN)
            )
            edges = box.edges().filter_by(Axis.Z)
            a = 12
            b = 7
            chamfer(edges[0], a, b)
            chamfer(edges[1], a, b)
            chamfer(edges[2], b, a)
            p4 = chamfer(edges[3], a, b)
            
            fillet(p4.edges().filter_by(Axis.Z)[0:8], 4)
            
        with Locations((x, y, disk_height / 2)):
            Box(
                10.1, 
                10.1, 
                50,
                rotation=Rotation(0,0,angle+60),
                mode=Mode.SUBTRACT,
                align=(Align.CENTER, Align.CENTER, Align.MIN)
            )
        
        #fillet(disk.edges().filter_by_position(Axis.Z, disk_height/2, disk_height/2), 1)
    
    
    
rod_substractions = []
    
for angle in [0, 120, 240]:
    rod_substractions.append(Box(disk_diameter/2, 10.1, 10.1, align=(Align.MIN, Align.CENTER, Align.CENTER), rotation=(45,0,0)).rotate(Axis.Z, angle,transform=True))
    
for index, polar_location in enumerate(PolarLocations(radius=10, start_angle=0, count=3).local_locations):
    rod_substractions[index].position += polar_location.position 
    
disk.part -= rod_substractions


show_all()
