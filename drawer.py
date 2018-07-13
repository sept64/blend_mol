#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class Drawer of the blend_mol project
allows to draw molecules from Mol class instances
"""

import bpy
from mathutils import Vector
from numpy import arange
from blend_mol.atom import Atom


PAS = 120
BEGIN = 0
END = PAS*4

class Drawer():
    def __init__(self):
        """
        """
        pass
    
    def animate(self, mol):
        bpy.context.scene.frame_set(BEGIN)
        # Draw cis molecule
        self.draw(mol.get_state_by_name('cis'))
        for obj in bpy.data.objects: 
                    obj.keyframe_insert('location', group="LocRot")
        
        # Animate 
        frame = PAS

        for i in arange(len(mol.states)-1):
            bpy.context.scene.frame_set(frame)
            self.move(mol.states[i], mol.states[i+1])
            
            self.save_all_keys()
            frame += PAS

        bpy.context.scene.frame_end = END
        bpy.context.scene.frame_set(BEGIN)

    def draw(self, state):
        for atom in state.atoms:
            self.add_atom(atom)
            
        for bond in state.bonds:
            self.add_bond(bond)
            
    def move(self, state_1, state_2):
        bpy.ops.object.select_all(action='DESELECT')
        # Atoms
        # List new atoms
        old_atoms_str = [atom.name for atom in state_1.atoms]
        new_atoms_str = [atom.name for atom in state_2.atoms]
                
        to_move = set(new_atoms_str).intersection(old_atoms_str)
        # Move the atoms that exists
        for o in to_move:
            new_atom = state_2.get_atom_by_name(o)
            new_loc = Vector([new_atom.x, new_atom.y, new_atom.z])
            bpy.data.objects[o].location = new_loc
        
        to_create = list(set(new_atoms_str) - set(old_atoms_str))
        for atom in to_create:
            self.pick_from_aside_atom(state_2.get_atom_by_name(atom), state_2)
        
        to_destroy = list(set(old_atoms_str) - set(new_atoms_str))
        for atom in to_destroy:
            self.put_aside_atom(state_1.get_atom_by_name(atom))
            
        # Bonds
        # List new bonds
        old_bonds_str = [bond.name for bond in state_1.bonds]
        new_bonds_str = [bond.name for bond in state_2.bonds]
                
        to_move = set(new_bonds_str).intersection(old_bonds_str)
        # Move the atoms that exists
        for o in to_move:
            new_bond = state_2.get_bond_by_name(o)
            new_ob_loc = self.compute_bond_coords(new_bond)
            bpy.data.objects[o].location = new_ob_loc.location

        to_create = list(set(new_bonds_str) - set(old_bonds_str))
        for atom in to_create:
            self.pick_from_aside_atom(state_2.get_atom_by_name(atom), state_2)
        
        to_destroy = list(set(old_bonds_str) - set(new_bonds_str))
        for atom in to_destroy:
            self.put_aside_atom(state_1.get_atom_by_name(atom))
   
            
        return 0
    
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
        ob = self.compute_bond_coords(bond)

        #curve = ob.data # bpy.data.curves.new('Curve', 'CURVE')
        #ob = bpy.data.objects.new(bond.name, curve)
        #ob.location = loc
        
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
  
    def compute_bond_coords(self, bond):
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
        return ob
        
    def put_aside_atom(self, atom):
        # bpy.ops.object.select_all(action='DESELECT')
        # bpy.data.objects[atom.name].select = True
        bpy.data.objects[atom.name].location = Vector([0,0,0])
        
    def pick_from_aside_atom(self, atom, state):
        try:
            # bpy.data.objects[atom.name].select = True
            bpy.data.objects[atom.name].location = Vector([atom.x,atom.y,atom.z])
        except:
            # Frame  = 0
            bpy.context.scene.frame_set(BEGIN)
            # Add atom
            atom_tmp = Atom()
            atom_tmp.number = atom.number
            atom_tmp.name = atom.name
            atom_tmp.type = atom.type
            atom_tmp.x = 0.0
            atom_tmp.y = 0.0
            atom_tmp.z = 0.0        
            self.add_atom(atom_tmp)
            # Save keys
            self.save_all_keys()
            # Frame = X
            bpy.context.scene.frame_set(state.number*PAS)
            # Move atom
            # bpy.ops.object.select_all(action='DESELECT')
            # bpy.data.objects[atom.name].select = True
            bpy.data.objects[atom.name].location = Vector([atom.x, atom.y, atom.z])
            # Save keys again
            self.save_all_keys()
        
    def save_all_keys(self):        
        for obj in bpy.data.objects: 
                        obj.keyframe_insert('location', group="LocRot")
        