#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class Drawer of the blend_mol project
allows to draw molecules from Mol class instances
"""

import bpy
from mathutils import Vector


class Drawer():
    def __init__(self):
        """
        """
        pass
    
    def draw(self, mol):
        for atom in mol.atoms:
            bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, size=0.2, view_align=False, enter_editmode=False, location=(atom.x, atom.y, atom.z))
            obj = bpy.context.selected_objects[0]
            obj.name = atom.name
            
        for bond in mol.bonds:
            print(bond)
            # Total paste from https://blender.stackexchange.com/questions/110177/connecting-two-points-with-a-line-curve-via-python-script
            v0, v1 = Vector([bond[0].x, bond[0].y, bond[0].z]), Vector([bond[1].x, bond[1].y, bond[1].z])  
            o = (v1 + v0) / 2  

            curve = bpy.data.curves.new('Curve', 'CURVE')
            spline = curve.splines.new('BEZIER')
            bp0 = spline.bezier_points[0]
            bp0.co = v0 - o
            bp0.handle_left_type = bp0.handle_right_type = 'AUTO'

            spline.bezier_points.add(count=1)
            bp1 = spline.bezier_points[1]
            bp1.co = v1 - o
            bp1.handle_left_type = bp1.handle_right_type = 'AUTO'
            ob = bpy.data.objects.new('{}_{}'.format(bond[0].name, bond[1].name), curve)
            ob.matrix_world.translation = o
            
            context = bpy.context
            scene = context.scene
            #ob = context.object
            #mw = ob.matrix_world
            #me = ob.data
            
            curve = ob.data    
            curve.dimensions = '3D'
            curve.bevel_depth = 0.010
            curve.bevel_resolution = 3 
            
            scene.objects.link(ob)

            # Convert everything to a mesh
            bpy.ops.object.select_all(action='SELECT')
            bpy.ops.object.convert(target='MESH')
     
    def move(self, mol):
        bpy.ops.object.select_all(action='DESELECT')
        # Select an atom
        for obj in bpy.data.objects:
            for atom in mol.atoms:
                if obj.name == atom.name:
                    new_loc = Vector([atom.x, atom.y, atom.z])
                    obj.location = new_loc

        
        