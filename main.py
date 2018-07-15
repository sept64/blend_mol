#!/usr/bin/env python
# !/usr/bin/env python
# -*- coding: utf8 -*-

"""
Main function of the blend_mol project
"""

import bpy
from blend_mol.mol import Mol
from blend_mol.drawer import Drawer


class BlendMol(bpy.types.Operator):
    """My Object who creates a molecule"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.mol"  # Unique identifier for buttons and menu items to reference.
    bl_label = "Mol"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):
        path_folder = "D:\\Titane64\\Documents\\Blender\\data_mol"
        # Read cis mol file and fill mol classe
        mol = Mol(path_folder)
        mol.read()

        # Draw and animate
        drawer = Drawer()
        drawer.animate(mol)

        return {'FINISHED'}


def register():
    bpy.utils.register_class(BlendMol)
    print("Start")


def unregister():
    bpy.utils.unregister_class(BlendMol)
    print("End")
