#!/usr/bin/env python
# !/usr/bin/env python
# -*- coding: utf8 -*-

"""
Main function of the mol_draw project
"""

import bpy

from mol_draw.drawer import Drawer
from mol_draw.mol import Mol


class MolDraw(bpy.types.Operator):
    """My Object who draws a molecule"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.mol"  # Unique identifier for buttons and menu items to reference.
    bl_label = "mol_draw"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):
        path_folder = "D:\\Titane64\\Documents\\Blender\\data_mol"
        # Read cis mol file and fill mol classe
        mol = Mol(path_folder)
        mol.read()

        # Draw and animate
        drawer = Drawer(mol)
        drawer.draw()

        return {'FINISHED'}


def register():
    bpy.utils.register_class(MolDraw)
    print("Start")


def unregister():
    bpy.utils.unregister_class(MolDraw)
    print("End")
