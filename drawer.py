#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class Drawer of the blend_mol project
allows to draw molecules from Mol class instances
"""

import bpy
import math
from blend_mol.atom import Atom
from mathutils import Vector, Quaternion, Matrix
from numpy import arange

PAS = 120
BEGIN = 0
END = PAS * 4


class Drawer:
    def __init__(self, mol):
        """
        """
        self.__mol = mol

        self.__materials = dict()
        self.__init_metrials()
        self.__init_animation()

    def __init_metrials(self):
        # Purge existing materials
        for tmp_mat in bpy.data.materials:
            bpy.data.materials.remove(tmp_mat)

        self.__materials['C'] = bpy.data.materials.new(name='C_mat')  # set new material to variable
        self.__materials['H'] = bpy.data.materials.new(name='H_mat')  # set new material to variable
        self.__materials['O'] = bpy.data.materials.new(name='O_mat')  # set new material to variable

        self.__materials['C'].diffuse_color = (0, 0, 0)
        self.__materials['H'].diffuse_color = (1, 1, 1)
        self.__materials['O'].diffuse_color = (1, 0, 0)

        self.__materials['H'].emit = 1
        self.__materials['O'].emit = 1

        self.__materials['C'].specular_intensity = 0
        self.__materials['H'].specular_intensity = 0
        self.__materials['O'].specular_intensity = 0

    def __init_animation(self):
        bpy.context.scene.frame_end = END

    def animate(self):
        bpy.context.scene.frame_set(BEGIN)

        # Draw cis molecules
        self.draw(self.__mol.get_state_by_name('cis'))

        self.save_keys('')

        # Animate 
        frame = PAS
        i = 0
        # for i in arange(len(self.__mol.states) - 1):
        while i < len(self.__mol.states) - 1:
            bpy.context.scene.frame_set(frame)
            self.move(i, i + 1)
            bpy.context.scene.frame_set(frame)
            self.save_keys('')
            i += 1
            frame += PAS
        bpy.context.scene.frame_set(BEGIN)

    def move(self, index_start, index_end):
        state_1 = self.__mol.states[index_start]
        state_2 = self.__mol.states[index_end]
        print('Computing move between state {} and state {}'.format(state_1.type, state_2.type))

        bpy.ops.object.select_all(action='DESELECT')
        bpy.ops.object.mode_set(mode='POSE')

        # Select the good bone and start the iteration loop to move all of it
        bond = self.__mol.iterate_bonds('cis')
        arm = bpy.data.armatures['Armature_mol']
        while bond:
            bone = arm.bones[bond.name]
            bone.select = True

            old_bonds_str = [bond.name for bond in state_1.bonds]
            new_bonds_str = [bond.name for bond in state_2.bonds]

            to_move = set(new_bonds_str).intersection(old_bonds_str)

            # Move the bond that exists
            for o in to_move:
                new_bond = state_2.get_bond_by_name(o)
                old_bond = state_1.get_bond_by_name(o)
                # Compute rotation and translation
                translation, euler_xyz = self.compute_translation_rotation_bonds(old_bond, new_bond)
                # Convert euler angles into matrix rotation
                matrix_rotation_new = euler_xyz.to_matrix().to_4x4()

                orig_loc, orig_rot, orig_scale = bone.matrix_local.decompose()
                orig_loc_mat = Matrix.Translation(orig_loc)
                orig_rot_mat = orig_rot.to_matrix().to_4x4()
                orig_scale_mat = Matrix.Scale(orig_scale[0], 4, (1, 0, 0)) * Matrix.Scale(orig_scale[1], 4, (0, 1, 0))

                bone.matrix_world = orig_loc_mat * matrix_rotation_new * orig_rot_mat * orig_scale_mat

                bone.location += translation

                self.save_keys(o)

            bond = self.__mol.iterate_bonds('cis')
        bpy.ops.object.mode_set(mode='OBJECT')

    def draw(self, state):
        for atom in state.atoms:
            self.add_atom(atom)

        for bond in state.bonds:
            self.add_bond(bond)

        # Add armature
        context = bpy.context
        scene = context.scene

        arm = bpy.data.armatures.new('Armature_mol')
        arm_obj = bpy.data.objects.new('Armature', arm)
        scene.objects.link(arm_obj)

        # Add bones to animate correctly the molecule
        # Init bones adding
        bond_to_draw = self.__mol.iterate_bonds('cis')
        self.add_bone(bond_to_draw, arm_obj, arm)
        cmpt = len(self.__mol.get_state_by_name('cis').bonds)
        while cmpt != 0:
            old_bond = bond_to_draw
            bond_to_draw = self.__mol.iterate_bonds('cis')
            if bond_to_draw:
                self.extrude_bone(old_bond, bond_to_draw)
            cmpt -= 1
        """
        done_bonds = [first_bond]
        self.add_bone(first_bond, arm_obj, arm)
        self.do_bone_starting_with(first_bond, first_bond.atoms[1], done_bonds)
        self.do_bone_starting_with(first_bond, first_bond.atoms[0], done_bonds)

        if len(self.__mol.get_state_by_name('cis').bonds) > len(done_bonds):
            print('We\'ve done {} bones yet, but {} are still to do !'.format(len(done_bonds), len(
                self.__mol.get_state_by_name('cis').bonds) - len(done_bonds)))
            bonds_to_do = list(set(self.__mol.get_state_by_name('cis').bonds) - set(done_bonds))
            print('Bones left : {}'.format([o.name for o in bonds_to_do]))

            first_bond = bonds_to_do[0]
            done_bonds.append(first_bond)
            self.add_bone(first_bond, arm_obj, arm)

            self.do_bone_starting_with(first_bond, first_bond.atoms[1], done_bonds)
            self.do_bone_starting_with(first_bond, first_bond.atoms[0], done_bonds)

        """

    def do_bone_starting_with(self, old_bond, head, already_done):
        # Propagate throw all the "heads" of the bones
        print('Do bone starting with : {} {} {}'.format(old_bond.name, head.name, [o.name for o in already_done]))
        for b in self.__mol.get_state_by_name('cis').bonds:
            if not b in already_done and b.atoms[0].name == head.name:
                self.extrude_bone(old_bond, b)
                already_done.append(b)
                self.do_bone_starting_with(b, b.atoms[1], already_done)

    def extrude_bone(self, old_bond, bond):
        print('Extrude with : {} {}'.format(old_bond.name, bond.name))
        arm = bpy.data.armatures['Armature_mol']
        # arm = ob.data

        bpy.ops.object.mode_set(mode='EDIT')

        if old_bond.atoms[0].name == bond.atoms[0].name:
            # bone = arm.edit_bones.new(bond.name)
            # bone.parent = arm.edit_bones[old_bond.name]
            bpy.ops.armature.select_all(action='DESELECT')
            # Active/select whatever the good bone to extrude
            arm.edit_bones[old_bond.name].select_head = True
            bpy.ops.armature.extrude()
            bone = arm.edit_bones[old_bond.name + '.001']
            bone.name = bond.name

        else:
            # Deselect everything first
            bpy.ops.armature.select_all(action='DESELECT')
            # Active/select whatever the good bone to extrude
            arm.edit_bones[old_bond.name].select_tail = True
            bpy.ops.armature.extrude()
            bone = arm.edit_bones[old_bond.name + '.001']
            bone.name = bond.name

        bpy.ops.armature.select_all(action='DESELECT')
        # Set the tail of the new bone
        arm.edit_bones[bond.name].select_tail = True
        bpy.context.scene.cursor_location = Vector((bond.atoms[1].x, bond.atoms[1].y, bond.atoms[1].z))
        bpy.ops.view3d.snap_selected_to_cursor()
        # bone.tail.xyz = bpy.context.scene.cursor_location
        bpy.ops.armature.select_all(action='DESELECT')

        bpy.ops.object.mode_set(mode='OBJECT')
        bpy.ops.object.select_all(action='DESELECT')

        # Parent the bone with meshes bond and atom
        scn = bpy.context.scene

        # obj_atom_1 = scn.objects[bond.atoms[0].name]
        obj_atom_2 = scn.objects[bond.atoms[1].name]
        try:
            obj_bond = scn.objects[bond.name]
        except:
            obj_bond = scn.objects['{}_{}'.format(bond.atoms[1].name, bond.atoms[0].name)]
        armature = scn.objects['Armature']
        arm_bones = armature.data.bones  # bpy.data.armatures[armature.name].bones

        # obj_atom_1.select = True
        obj_atom_2.select = True
        obj_bond.select = True
        armature.select = True
        scn.objects.active = armature

        arm_bones.active = arm_bones[bond.name]

        bpy.ops.object.parent_set(type='BONE_RELATIVE')

    def __move_atom_and_bond_objects_old(self, index_start, index_end):

        state_1 = self.__mol.states[index_start]
        state_2 = self.__mol.states[index_end]
        print('Computing move between state {} and state {}'.format(state_1.type, state_2.type))

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
            self.save_keys(o)

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

        # Move the bond that exists
        for o in to_move:
            new_bond = state_2.get_bond_by_name(o)
            old_bond = state_1.get_bond_by_name(o)
            # Compute rotation and translation
            translation, euler_xyz = self.compute_translation_rotation_bonds(old_bond, new_bond)
            # Convert euler angles into matrix rotation
            matrix_rotation_new = euler_xyz.to_matrix().to_4x4()

            """
            i=0
            while i < len(euler_xyz):
                if abs(euler_xyz[i]) ==  abs(bpy.data.objects[o].rotation_euler[i]):
                    # math.copysign(euler_xyz[i], bpy.data.objects[o].rotation_euler[i])
                    # euler_xyz[i] = 0.0
                i += 1
            """
            orig_loc, orig_rot, orig_scale = bpy.data.objects[o].matrix_world.decompose()
            orig_loc_mat = Matrix.Translation(orig_loc)
            orig_rot_mat = orig_rot.to_matrix().to_4x4()
            orig_scale_mat = Matrix.Scale(orig_scale[0], 4, (1, 0, 0)) * Matrix.Scale(orig_scale[1], 4, (0, 1, 0))

            bpy.data.objects[o].matrix_world = orig_loc_mat * matrix_rotation_new * orig_rot_mat * orig_scale_mat

            bpy.data.objects[o].location += translation

            self.save_keys(o)

        to_create = list(set(new_bonds_str) - set(old_bonds_str))
        # print('to_create : {}'.format(to_create))
        for bond in to_create:
            self.bond_appear(state_2.get_bond_by_name(bond), state_2)

        to_destroy = list(set(old_bonds_str) - set(new_bonds_str))
        # print('to_destroy : {}'.format(to_destroy))
        for bond in to_destroy:
            self.bond_disappear(state_1.get_bond_by_name(bond), state_2)

    def add_atom(self, atom):
        """
        Draw an atom in blender
        """
        if atom.type == 'C' or atom.type == 'O':
            bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, size=0.4, view_align=False,
                                                 enter_editmode=False, location=(atom.x, atom.y, atom.z))
        else:
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
        self.__materials[bond.name] = bpy.data.materials.new(name=bond.name)
        self.__materials[bond.name].use_transparency = True
        ob.data.materials.append(self.__materials[bond.name])

        context = bpy.context
        scene = context.scene

        curve = ob.data
        curve.dimensions = '3D'
        curve.bevel_depth = 0.1
        curve.bevel_resolution = 32
        curve.fill_mode = 'FULL'

        ob.name = bond.name

        scene.objects.link(ob)

        # Convert everything to a mesh
        bpy.ops.object.select_all(action='SELECT')
        bpy.ops.object.convert(target='MESH')

    def add_bone(self, bond, arm_obj, arm):
        atom_1 = bond.atoms[0]
        atom_2 = bond.atoms[1]

        bpy.context.scene.objects.active = arm_obj

        bpy.ops.object.mode_set(mode='EDIT')

        bone = arm.edit_bones.new(bond.name)
        bone.head = Vector((atom_1.x, atom_1.y, atom_1.z))
        bone.tail = Vector((atom_2.x, atom_2.y, atom_2.z))

        bpy.ops.object.mode_set(mode='OBJECT')

        # Snap origin to center of the object
        bpy.context.scene.cursor_location = Vector((atom_1.x, atom_1.y, atom_1.z))
        bpy.ops.object.select_all(action='DESELECT')
        arm_obj.select = True
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='BOUNDS')

        # Parent the bone with meshes bond and atom
        scn = bpy.context.scene

        # obj_atom_1 = scn.objects[bond.atoms[0].name]
        obj_atom_2 = scn.objects[bond.atoms[1].name]
        try:
            obj_bond = scn.objects[bond.name]
        except:
            obj_bond = scn.objects['{}_{}'.format(bond.atoms[1].name, bond.atoms[0].name)]
        armature = scn.objects['Armature']
        arm_bones = armature.data.bones  # bpy.data.armatures[armature.name].bones

        # obj_atom_1.select = True
        obj_atom_2.select = True
        obj_bond.select = True
        armature.select = True
        scn.objects.active = armature

        arm_bones.active = arm_bones[bond.name]

        bpy.ops.object.parent_set(type='BONE_RELATIVE')

    def compute_translation_rotation_bonds(self, old_bond, new_bond):
        # Translation
        v_old_atom_0, v_old_atom_1 = Vector([old_bond.atoms[0].x, old_bond.atoms[0].y, old_bond.atoms[0].z]), Vector(
            [old_bond.atoms[1].x, old_bond.atoms[1].y, old_bond.atoms[1].z])
        center_old_bond = (v_old_atom_1 + v_old_atom_0) / 2

        v_new_atom_0, v_new_atom_1 = Vector([new_bond.atoms[0].x, new_bond.atoms[0].y, new_bond.atoms[0].z]), Vector(
            [new_bond.atoms[1].x, new_bond.atoms[1].y, new_bond.atoms[1].z])
        center_new_bond = (v_new_atom_1 + v_new_atom_0) / 2

        translation = center_new_bond - center_old_bond

        # Rotation
        old_bond_vec = Vector([old_bond.atoms[1].x - old_bond.atoms[0].x, old_bond.atoms[1].y - old_bond.atoms[0].y,
                               old_bond.atoms[1].z - old_bond.atoms[0].z])
        new_bond_vec = Vector([new_bond.atoms[1].x - new_bond.atoms[0].x, new_bond.atoms[1].y - new_bond.atoms[0].y,
                               new_bond.atoms[1].z - new_bond.atoms[0].z])

        # print('OldBond 0 = [{}, {}, {}], 1 = [{}, {}, {}]'.format(old_bond.atoms[0].x, old_bond.atoms[0].y,
        #                                                           old_bond.atoms[0].z,
        #                                                           old_bond.atoms[1].x, old_bond.atoms[1].y,
        #                                                           old_bond.atoms[1].z))
        # print('NewBond 0 = [{}, {}, {}], 1 = [{}, {}, {}]'.format(new_bond.atoms[0].x, new_bond.atoms[0].y,
        #                                                           new_bond.atoms[0].z,
        #                                                           new_bond.atoms[1].x, new_bond.atoms[1].y,
        #                                                           new_bond.atoms[1].z))

        rotation = old_bond_vec.rotation_difference(new_bond_vec).to_euler()
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
        bpy.data.objects[atom.name].location = Vector([0, 0, -10])
        self.save_keys(atom.name)

    def pick_from_aside_atom(self, atom, state):
        try:
            bpy.data.objects[atom.name].location = Vector([atom.x, atom.y, atom.z])
            self.save_keys(atom.name)
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
            bpy.context.scene.frame_set((state.number - 1) * PAS)
            self.save_keys(atom_tmp.name)
            # Frame = X
            bpy.context.scene.frame_set(state.number * PAS)

            # Move atom
            bpy.data.objects[atom_tmp.name].location = Vector([atom.x, atom.y, atom.z])
            self.save_keys(atom_tmp.name)

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
            # Fade in
            bpy.context.scene.frame_set((state.number - 1) * PAS)
            bpy.data.materials[bond.name].alpha = 0
            bpy.data.materials[bond.name].keyframe_insert(data_path='alpha')
            bpy.context.scene.frame_set(state.number * PAS)
            bpy.data.materials[bond.name].alpha = 1
            bpy.data.materials[bond.name].keyframe_insert(data_path='alpha')
            # Move them !
            # Get old bound atoms positions etc.
            old_bond = None
            found = False
            i = 0
            while not found:
                state = self.__mol.states[i]
                for b in state.bonds:
                    if b.name == bond.name:
                        old_bond = b
                        found = True
                        break
                i += 1

            # Compute rotation and translation
            translation, euler_xyz = self.compute_translation_rotation_bonds(old_bond, bond)
            # Convert euler angles into matrix rotation
            matrix_rotation_new = euler_xyz.to_matrix().to_4x4()
            try:
                orig_loc, orig_rot, orig_scale = bpy.data.objects[bond.name].matrix_world.decompose()
            except:
                orig_loc, orig_rot, orig_scale = bpy.data.objects[
                    '{}_{}'.format(bond.atoms[1].name, bond.atoms[0].name)].matrix_world.decompose()
            orig_loc_mat = Matrix.Translation(orig_loc)
            orig_rot_mat = orig_rot.to_matrix().to_4x4()
            orig_scale_mat = Matrix.Scale(orig_scale[0], 4, (1, 0, 0)) * Matrix.Scale(orig_scale[1], 4, (0, 1, 0))

            bpy.data.objects[
                bond.name].matrix_world = orig_loc_mat * matrix_rotation_new * orig_rot_mat * orig_scale_mat
            try:
                bpy.data.objects[bond.name].location += translation
            except:
                bpy.data.objects['{}_{}'.format(bond.atoms[1].name, bond.atoms[0].name)].location += translation

            self.save_keys(bond.name)
            # print('Fade in of {}'.format(bond.name))

        except:
            # print('Adding {}'.format(bond.name))
            # Add bond
            self.add_bond(bond)
            # Hide it from the start
            bpy.context.scene.frame_set(0)
            bpy.data.materials[bond.name].alpha = 0
            bpy.data.materials[bond.name].keyframe_insert(data_path='alpha')

            bpy.context.scene.frame_set((state.number - 1) * PAS)
            bpy.data.materials[bond.name].keyframe_insert(data_path='alpha')

            bpy.context.scene.frame_set(state.number * PAS)
            bpy.data.materials[bond.name].alpha = 1
            bpy.data.materials[bond.name].keyframe_insert(data_path='alpha')

    def bond_disappear(self, bond, state):
        # Fade out
        # print('Fade out of {}'.format(bond.name))
        bpy.context.scene.frame_set((state.number - 1) * PAS)
        bpy.data.materials[bond.name].alpha = 1
        bpy.data.materials[bond.name].keyframe_insert(data_path='alpha')
        bpy.context.scene.frame_set(state.number * PAS)
        bpy.data.materials[bond.name].alpha = 0
        bpy.data.materials[bond.name].keyframe_insert(data_path='alpha')
