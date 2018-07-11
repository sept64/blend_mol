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
        # Do atoms
        # List new atoms
        new_atoms_str = mol.atoms.keys()
        old_atoms_str = []
        for obj in bpy.data.objects:
            if not '_' in obj.name:
                old_atoms_str.append(obj.name)
                
        # Move the atoms that exists
        for obj in bpy.data.objects:
            for atom in mol.atoms:
                if obj.name == atom.name:
                    new_loc = Vector([atom.x, atom.y, atom.z])
                    obj.location = new_loc
        
        to_create = list(set(new_atoms_str) - set(old_atoms_str))
        for atom in to_create:
            bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, size=0.2, view_align=False, enter_editmode=False, location=(mol.atoms[atom].x, mol.atoms[atom].y, mol.atoms[atom].z))
            obj = bpy.context.selected_objects[0]
            obj.name = mol.atoms[atom].name
            
        to_destroy = list(set(old_bonds_str) - set(new_atoms_str))
        for atom in to_destroy:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[atom].select = True

            # remove it
            bpy.ops.object.delete() 
            
        # Do links between atoms
        # List new bonds
        new_bonds_str = []
        for bond in mol.bonds:
            new_bonds_str.append('{}_{}'.format(bond[0].name, bond[1].name))
        old_bonds_str = []
        for obj in bpy.data.objects:
            if '_' in obj.name:
                old_bonds_str.append(obj.name)
        
        # Move the bond if it is in the two lists
        commons = list(set(new_bonds_str).intersection(old_bonds_str))
        for b in commons:
            obj = bpy.data.objects[b]
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
            
            obj.location = ob.location
            
        # Create the bond if it is in the new_bonds_str but not in the old_bonds_str
        to_create = list(set(new_bonds_str) - set(old_bonds_str))
        print('TO CREATE')
        print(to_create)
        for bond in to_create:
            # Total paste from https://blender.stackexchange.com/questions/110177/connecting-two-points-with-a-line-curve-via-python-script
            v0 = Vector(bpy.data.objects[bond.split('_')[0]].location)
            v1 = Vector(bpy.data.objects[bond.split('_')[1]].location)
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
            ob = bpy.data.objects.new(bond, curve)
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
            
        to_destroy = list(set(old_bonds_str) - set(new_bonds_str))
        print('TO Destroy')
        print(to_destroy)
        for bond in to_destroy:
            bpy.ops.object.select_all(action='DESELECT')
            bpy.data.objects[bond.split('_')[0]].select = True

            # remove it
            bpy.ops.object.delete() 
                        