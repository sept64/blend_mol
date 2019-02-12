#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Main function of the mol_init project
"""

import bpy
from mol_init.lighting_designer import LightingDesigner
from mol_init.background import Background


class MolInit(bpy.types.Operator):
    """My Object who init the scene for further mol stuff"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.mol"  # Unique identifier for buttons and menu items to reference.
    bl_label = "mol_init"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):
        # Place lights
        l = LightingDesigner()
        l.place_lights()

        # Draw background
        b = Background()
        b.draw()

        return {'FINISHED'}


def register():
    bpy.utils.register_class(MolInit)
    print("Start")


def unregister():
    bpy.utils.unregister_class(MolInit)
    del bpy.types.Scene.conf_path
    print("End")
