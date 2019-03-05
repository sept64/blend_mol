#!/usr/bin/env python
# !/usr/bin/env python
# -*- coding: utf8 -*-

"""
Main function of the mol_rig project
"""

import bpy
from mol_rig.rigger import Rigger


class MolRig(bpy.types.Operator):
    """My Object who rig a molecule"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.mol_rig"  # Unique identifier for buttons and menu items to reference.
    bl_label = "mol_rig"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):
        # Rig
        rig = Rigger()
        rig.rig()

        return {'FINISHED'}


def register():
    bpy.utils.register_class(MolRig)
    print("Start")


def unregister():
    bpy.utils.unregister_class(MolRig)
    print("End")
