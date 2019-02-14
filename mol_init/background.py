#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class background of the blend_mol project
allows to init background in the scene
"""

import bpy


class Background:
    def __init__(self):
        self.__material = bpy.data.materials.new(name='background_mat')  # set new material to variable
        self.__material.diffuse_color = (0.020, 0.368, 0.954)
        self.__material.diffuse_intensity = 0.5
        self.__material.emit = 0.2
        self.__material.specular_color = (0.611, 0.914, 1)
        self.__material.specular_intensity = 0.650
        self.__material.specular_hardness = 28


def draw(self):
        """
        The background is made of a simple huge colored plane
        """
        bpy.ops.mesh.primitive_plane_add(radius=300, view_align=False, enter_editmode=False, location=(-20, 0, 0))
        bpy.data.objects['Plane'].name = 'Background'
        bpy.data.objects['Background'].rotation_euler[1] = 1    # In radians
