#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class Drawer of the blend_mol project
allows to draw molecules from Mol class instances
"""

import bpy
from mathutils import Vector, Quaternion
import math

from numpy import arange
from blend_mol.atom import Atom

PAS = 120
BEGIN = 0
END = PAS * 4


class Drawer():
    def __init__(self):
        """
        """
        self.__materials = dict()
        self.__init_metrials()

    def __init_metrials(self):
        # Purge existing materials
        for tmp_mat in bpy.data.materials:
            bpy.data.materials.remove(tmp_mat)

        self.__materials['C'] = bpy.data.materials.new(name='C_mat')  # set new material to variable
        self.__materials['H'] = bpy.data.materials.new(name='H_mat')  # set new material to variable
        self.__materials['O'] = bpy.data.materials.new(name='O_mat')  # set new material to variable

        self.__materials['C'].diffuse_color = (0, 0, 0)  # change color
        self.__materials['H'].diffuse_color = (1, 1, 1)  # change color
        self.__materials['H'].emit = 1
        self.__materials['O'].diffuse_color = (1, 0, 0)  # change color
        self.__materials['O'].emit = 1


    def animate(self, mol):
        bpy.context.scene.frame_set(BEGIN)

        # Draw cis molecule
        self.draw(mol.get_state_by_name('cis'))

        self.save_keys('')

        # Animate 
        frame = PAS

        for i in arange(len(mol.states) - 1):
            bpy.context.scene.frame_set(frame)
            self.move(mol.states[i], mol.states[i + 1])
            self.save_keys('')
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
        print('to_move : {}'.format(to_move))
        # Move the bond that exists
        for o in to_move:
            new_bond = state_2.get_bond_by_name(o)
            old_bond = state_1.get_bond_by_name(o)
            # Compute rotation and translation
            translation, euler_xyz = self.compute_translation_rotation_bonds(old_bond, new_bond)
            print(euler_xyz )
            bpy.data.objects[o].location += translation
            bpy.data.objects[o].rotation_mode = 'XYZ'
            bpy.data.objects[o].rotation_euler = euler_xyz

            # bpy.data.objects.remove(bpy.data.objects[new_ob.name])

        return 0
        to_create = list(set(new_bonds_str) - set(old_bonds_str))
        print('to_create : {}'.format(to_create))
        for bond in to_create:
            self.bond_appear(state_2.get_bond_by_name(bond), state_2)

        to_destroy = list(set(old_bonds_str) - set(new_bonds_str))
        print('to_destroy : {}'.format(to_destroy))
        for atom in to_destroy:
            self.bond_disappear(state_1.get_bond_by_name(atom), True)

    def add_atom(self, atom):
        """
        Draw an atom in blender
        """
        bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, size=0.2, view_align=False,
                                             enter_editmode=False, location=(atom.x, atom.y, atom.z))
        bpy.ops.object.shade_smooth()
        obj = bpy.context.selected_objects[0]
        obj.name = atom.name
        obj.data.materials.append(self.__materials[atom.type])  # add the material to the object

    def add_bond(self, bond):
        """
        Draw a bond in blender
        """
        # Total paste from https://blender.stackexchange.com/questions/110177/connecting-two-points-with-a-line-curve-via-python-script
        ob = self.compute_bond_coords(bond)

        # curve = ob.data # bpy.data.curves.new('Curve', 'CURVE')
        # ob = bpy.data.objects.new(bond.name, curve)
        # ob.location = loc

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

    def compute_translation_rotation_bonds(self, old_bond, new_bond):
        # Translation
        v_old_atom_0, v_old_atom_1 = Vector([old_bond.atoms[0].x, old_bond.atoms[0].y, old_bond.atoms[0].z]), Vector(
            [old_bond.atoms[1].x, old_bond.atoms[1].y, old_bond.atoms[1].z])
        center_old_bond = (v_old_atom_1 + v_old_atom_0) / 2

        v_new_atom_0, v_new_atom_1 = Vector([new_bond.atoms[0].x, new_bond.atoms[0].y, new_bond.atoms[0].z]), Vector(
            [new_bond.atoms[1].x, new_bond.atoms[1].y, new_bond.atoms[1].z])
        center_new_bond = (v_new_atom_1 + v_new_atom_0) / 2

        translation = center_new_bond - center_old_bond
        old_bond_vec = Vector([old_bond.atoms[0].x - old_bond.atoms[1].x, old_bond.atoms[0].y - old_bond.atoms[1].y, old_bond.atoms[0].z - old_bond.atoms[1].z])
        new_bond_vec = Vector([new_bond.atoms[0].x - new_bond.atoms[1].x, new_bond.atoms[0].y - new_bond.atoms[1].y,
                               new_bond.atoms[0].z - new_bond.atoms[1].z])

        rotation = old_bond_vec.rotation_difference(new_bond_vec).to_euler()
        # axe_x = Line3D((0, 0, 0), (1, 0, 0))
        # axe_y = Line3D((0, 0, 0), (0, 1, 0))
        # axe_z = Line3D((0, 0, 0), (0, 0, 1))
        #
        # # Angle Axe X
        # p3d_old_0 = Point3D(old_bond.atoms[0].x, old_bond.atoms[0].y, old_bond.atoms[0].z)
        # p3d_old_1 = Point3D(old_bond.atoms[1].x, old_bond.atoms[1].y, old_bond.atoms[1].z)
        #
        # p3d_new_0 = Point3D(new_bond.atoms[0].x, new_bond.atoms[0].y, new_bond.atoms[0].z)
        # p3d_new_1 = Point3D(new_bond.atoms[1].x, new_bond.atoms[1].y, new_bond.atoms[1].z)
        #
        # line_old = Line3D((p3d_old_0),(p3d_old_1))
        # line_new = Line3D((p3d_new_0), (p3d_new_1))
        #
        # intersection_line_old_axe_x = line_old.intersection(axe_x)
        # intersection_line_new_axe_x = line_new.intersection(axe_x)
        #
        # cos_theta_x_old = float(p3d_old_0.distance(intersection_line_old_axe_x)) / float(p3d_old_1.distance(intersection_line_old_axe_x))
        # cos_theta_x_new = float(p3d_new_0.distance(intersection_line_new_axe_x)) / float(p3d_new_1.distance(intersection_line_new_axe_x))
        #
        # theta_x_old = math.acos(cos_theta_x_old)
        # theta_x_new = math.acos(cos_theta_x_new)
        #
        # theta_x = theta_x_new - theta_x_old
        # , math.degrees(theta_x)
        return translation, rotation

    def compute_bond_coords(self, bond):
        v0, v1 = Vector([bond.atoms[0].x, bond.atoms[0].y, bond.atoms[0].z]), Vector(
            [bond.atoms[1].x, bond.atoms[1].y, bond.atoms[1].z])
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
        # bpy.data.curves.remove(curve)
        ob.matrix_world.translation = o
        return ob

    def put_aside_atom(self, atom):
        # bpy.ops.object.select_all(action='DESELECT')
        # bpy.data.objects[atom.name].select = True
        bpy.data.objects[atom.name].location = Vector([0, 0, -10])

    def pick_from_aside_atom(self, atom, state):
        try:
            bpy.data.objects[atom.name].location = Vector([atom.x, atom.y, atom.z])
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
            atom_tmp.z = -10.0
            self.add_atom(atom_tmp)
            # Save keys
            self.save_keys(atom_tmp.name)
            bpy.context.scene.frame_set((state.number-1) * PAS)
            self.save_keys(atom_tmp.name)
            # Frame = X
            bpy.context.scene.frame_set((state.number) * PAS)

            # Move atom
            # bpy.ops.object.select_all(action='DESELECT')
            # bpy.data.objects[atom.name].select = True
            bpy.data.objects[atom_tmp.name].location = Vector([atom.x, atom.y, atom.z])
            # Save keys again
            # self.save_keys(atom_tmp.name)

    def save_keys(self, name_obj):
        if name_obj == '':
            for obj in bpy.data.objects:
                obj.keyframe_insert(data_path='location')
                obj.keyframe_insert(data_path='rotation_euler')
        else:
            for obj in bpy.data.objects:
                if obj.name == name_obj:
                    obj.keyframe_insert(data_path='location')
                    obj.keyframe_insert(data_path='rotation_euler')

    def bond_appear(self, bond, state):
        # Two possibilities : 1 the bond exists but it's hidden
        # 2 the bond doesn't exists
        try:
            # Compute the new location
            ob = self.compute_bond_coords(bond)
            bpy.data.objects[bond.name].location = ob.location
            # deselect all
            bpy.ops.object.select_all(action='DESELECT')
            # selection
            bpy.data.objects[ob.name].select = True
            # remove it
            bpy.ops.object.delete()

            self.bond_disappear(bond, False)
        except:
            # Go in the previous state time line
            bpy.context.scene.frame_set((state.number - 1) * PAS)
            # Add bond
            self.add_bond(bond)
            self.bond_disappear(bond, True)
            self.save_keys(bond.name)
            bpy.context.scene.frame_set(state.number * PAS)
            self.bond_disappear(bond, False)

    def bond_disappear(self, bond, bool):
        bpy.data.objects[bond.name].hide = bool
