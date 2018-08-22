#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class Rigger of the mol_rig project
allows to rig molecule
"""

import bpy
from mathutils import Vector

from mol_rig.iterator import Iterator


class Rigger:
    def __init__(self):
        pass

    def rig(self):
        # Add armature
        arm = bpy.data.armatures.new('Armature_mol')
        arm_obj = bpy.data.objects.new('Armature', arm)
        bpy.context.scene.objects.link(arm_obj)

        # Add bones to animate correctly the molecule
        # Init bones adding
        it = Iterator()
        bond_to_draw = it.next()

        self.add_bone(bond_to_draw, arm_obj, arm)
        cmpt = len(it.bonds)
        while cmpt != 0:
            old_bond = bond_to_draw
            bond_to_draw = it.next()
            if bond_to_draw:
                self.extrude_bone(old_bond, bond_to_draw)
            cmpt -= 1

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

        obj_atom_2 = scn.objects[bond.name.split('_')[1] + '_cis']
        try:
            obj_bond = scn.objects[bond.name]
        except:
            obj_bond = scn.objects['{}_{}'.format(bond.atoms[1].name, bond.atoms[0].name)]
        armature = scn.objects['Armature']
        arm_bones = armature.data.bones  # bpy.data.armatures[armature.name].bones

        obj_atom_2.select = True
        obj_bond.select = True
        armature.select = True
        scn.objects.active = armature

        arm_bones.active = arm_bones[bond.name]

        # bpy.ops.object.parent_set(type='BONE_RELATIVE')-

    def add_bone(self, bond, arm_obj, arm):
        atom_1_name = '{}_cis'.format(bond.name.split('_')[0])
        atom_2_name = '{}_cis'.format(bond.name.split('_')[1])
        atom_1 = bpy.data.objects[atom_1_name]
        atom_2 = bpy.data.objects[atom_2_name]

        bpy.context.scene.objects.active = arm_obj

        bpy.ops.object.mode_set(mode='EDIT')

        bone = arm.edit_bones.new(bond.name)
        bone.head = Vector((atom_1.location.x, atom_1.location.y, atom_1.location.z))
        bone.tail = Vector((atom_2.location.x, atom_2.location.y, atom_2.location.z))

        bpy.ops.object.mode_set(mode='OBJECT')

        # Snap origin to center of the object
        bpy.context.scene.cursor_location = Vector((atom_1.location.x, atom_1.location.y, atom_1.location.z))
        bpy.ops.object.select_all(action='DESELECT')
        arm_obj.select = True
        bpy.ops.object.origin_set(type='ORIGIN_CURSOR', center='BOUNDS')

        # Parent the bone with meshes bond and atom
        scn = bpy.context.scene

        obj_atom_2 = scn.objects[bond.name.split('_')[1] + '_cis']
        try:
            obj_bond = scn.objects[bond.name]
        except:
            obj_bond = scn.objects['{}_{}'.format(bond.atoms[1].name, bond.atoms[0].name)]
        armature = scn.objects['Armature']
        arm_bones = armature.data.bones  # bpy.data.armatures[armature.name].bones

        obj_atom_2.select = True
        obj_bond.select = True
        armature.select = True
        scn.objects.active = armature

        arm_bones.active = arm_bones[bond.name]

        bpy.ops.object.parent_set(type='BONE_RELATIVE')
