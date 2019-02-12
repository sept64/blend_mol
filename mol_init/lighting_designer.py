#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class LigtingDesigner of the blend_mol project
allows to place lights in the scene
"""

import bpy


class LightingDesigner:
    def place_lights(self):
        """
        Places 4 lights :
            * -10, 0, 12
            * 10, 0, 12
            * 0,-10, 12
            * 0, 10, 12
        """
        coords = [[-10, 0, 12], [10, 0, 12], [0,-10, 12], [0, 10, 12]]
        for i in coords:
            bpy.ops.object.lamp_add(type='POINT', radius=1, view_align=False, location=(i[0], i[1], i[2]))
