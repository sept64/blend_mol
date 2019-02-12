#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class background of the blend_mol project
allows to init background in the scene
"""

import bpy


class Background:
    def __init__(self):
        pass

    def draw(self):
        """
        The background is made of a simple huge colored plane
        """
        bpy.ops.mesh.primitive_plane_add(radius=300, view_align=False, enter_editmode=False, location=(-20, 0, 0))
