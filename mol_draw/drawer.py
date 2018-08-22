#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class Drawer of the blend_mol project
allows to draw molecules from Mol class instances
"""

import bpy
from mathutils import Vector


class Drawer:
    def __init__(self, mol):
        """
        """
        self.__mol = mol

        self.__materials = dict()
        self.__init_materials()

    def __init_materials(self):
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

    def draw(self):
        """
        Draws all the molecule's states in different layers
        :return:
        """

        layer_cmp = 0
        for state_name in self.__mol.TYPES:
            layers = [False, False, False, False, False, False, False, False, False, False, False, False, False,
                      False, False, False, False, False, False, False]
            layers[layer_cmp] = True
            state = self.__mol.get_state_by_name(state_name)

            for atom in state.atoms:
                self.add_atom(atom, state_name, layers)

            for bond in state.bonds:
                self.add_bond(bond, state_name, layers)
            layer_cmp += 1

    def add_atom(self, atom, state_name, layers):
        """
        Draw an atom in blender
        """
        if atom.type == 'C' or atom.type == 'O':
            bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, size=0.4, view_align=False,
                                                 enter_editmode=False, location=(atom.x, atom.y, atom.z), layers=layers)
        else:
            bpy.ops.mesh.primitive_uv_sphere_add(segments=64, ring_count=32, size=0.2, view_align=False,
                                                 enter_editmode=False, location=(atom.x, atom.y, atom.z), layers=layers)
        bpy.ops.object.shade_smooth()
        obj = bpy.data.objects['Sphere']
        obj.name = '{}_{}'.format(atom.name, state_name)
        obj.data.materials.append(self.__materials[atom.type])  # add the material to the object

    def add_bond(self, bond, state_name, layers):
        """
        Draw a bond in blender
        """
        # Total paste from https://blender.stackexchange.com/questions/110177/connecting-two-points-with-a-line-curve-via-python-script
        ob = self.__compute_bond_coords(bond)
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

        ob.name = '{}_{}'.format(bond.name, state_name)

        scene.objects.link(ob)

        bpy.data.objects[ob.name].layers = layers

    def __compute_bond_coords(self, bond):
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
        ob.matrix_world.translation = o
        return ob
