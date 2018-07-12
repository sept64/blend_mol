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
    
    def animate(self, mol):
        # Draw cis molecule
        self.draw(mol.get_state_by_name('cis'))
        
        # Animate 
        frame = 0
        
        for i in range(len(mol.states)):
            bpy.context.scene.frame_set(frame)
            self.move(mol.states[i], mol.states[i+1])
            
            for obj in bpy.data.objects: 
                    obj.keyframe_insert('location', group="LocRot")
            frame += 120
        
    def draw(self, state):
        for atom in state.atoms:
            self.add_atom(atom)
            
        for bond in state.bonds:
            self.add_bond(bond)
            
    def move(self, state_1, state_2):
        bpy.ops.object.select_all(action='DESELECT')
        # Atoms
        # List new atoms
        new_atoms_str = [atom.name for atom in state_1.atoms]
        old_atoms_str = [atom.name for atom in state_2.atoms]
                
        to_move = set(new_atoms_str).intersection(old_atoms_str)
        # Move the atoms that exists
        for o in to_move:
            new_atom = state_2.get_atom_by_name(o)
            new_loc = Vector([new_atom.x, new_atom.y, new_atom.z])
            bpy.data.objects[o].location = new_loc
                    
        return 0
        
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
            spline = curve.splines.new('²')
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
            curve.bevel_depth = 0.025
            curve.bevel_resolution = 10 
            curve.fill_mode = 'FULL'
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
    
    def add_atom(self, atom):
        """
        Draw an atom in blender
        """
        bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, size=0.2, view_align=False, enter_editmode=False, location=(atom.x, atom.y, atom.z))
        obj = bpy.context.selected_objects[0]
        obj.name = atom.name
            
    def add_bond(self, bond):
        """
        Draw a bond in blender
        """
        # Total paste from https://blender.stackexchange.com/questions/110177/connecting-two-points-with-a-line-curve-via-python-script
        v0, v1 = Vector([bond.atoms[0].x, bond.atoms[0].y, bond.atoms[0].z]), Vector([bond.atoms[1].x, bond.atoms[1].y, bond.atoms[1].z])  
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
        ob = bpy.data.objects.new(bond.name, curve)
        ob.matrix_world.translation = o
        
        context = bpy.context
        scene = context.scene
        
        curve = ob.data    
        curve.dimensions = '3D'
        curve.bevel_depth = 0.020
        curve.bevel_resolution = 10 
        curve.fill_mode = 'FULL'
        
        scene.objects.link(ob)
        
        # Convert everything to a mesh
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.convert(target='MESH')
        
    def remove_object(self, obj):
        pass