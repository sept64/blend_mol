#!/usr/bin/env python
# !/usr/bin/env python
# -*- coding: utf8 -*-

"""
Main function of the mol_draw project
"""

import os

import bpy
from mol_draw.drawer import Drawer
from mol_draw.mol import Mol


class MolDraw(bpy.types.Operator):
    """My Object who draws a molecule"""  # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.mol"  # Unique identifier for buttons and menu items to reference.
    bl_label = "mol_draw"  # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.

    def execute(self, context):
        path_folder = ""
        if os.name == 'nt':  # Microsoft
            path_folder = "D:\\Titane64\\Documents\\Blender\\data_mol\\"
        if os.name == 'posix':  # Linux
            path_folder = "/home/tsotirop/Perso/blend_mol/molecules/"
        else:
            exit("ERROR: system is neither linux nor windows. Exiting.")
        print('In path: {}'.format(path_folder))
        # Read mol files and draw them
        files = []
        for _, _, f in os.walk(path_folder):
            print('\tFiles are: {}'.format(f))
            files = f
            break

        layer = 0
        for file in files:
            path_to_mol = path_folder + file
            print('Drawing molecule: {}'.format(path_to_mol))
            mol = Mol(path_to_mol)
            mol.read()
            print(mol)
            # Draw
            drawer = Drawer(mol)
            drawer.draw(layer, file)
            layer += 1

        return {'FINISHED'}


def register():
    bpy.utils.register_class(MolDraw)
    bpy.types.Scene.conf_path = bpy.props.StringProperty \
            (
            name="Root Path",
            default="",
            description="Define the root path of the project",
            subtype='DIR_PATH'
        )
    print("Start")


def unregister():
    bpy.utils.unregister_class(MolDraw)
    del bpy.types.Scene.conf_path
    print("End")
