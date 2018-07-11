#!/usr/bin/env python
#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Main function of the blend_mol project
"""

import bpy
from blend_mol.reader import Reader
from blend_mol.drawer import Drawer

class BlendMol(bpy.types.Operator):
    """My Object who creates a molecule"""      # Use this as a tooltip for menu items and buttons.
    bl_idname = "object.mol"        # Unique identifier for buttons and menu items to reference.
    bl_label = "Mol"         # Display name in the interface.
    bl_options = {'REGISTER', 'UNDO'}  # Enable undo for the operator.
    def execute(self, context):
        path_folder = "D:\\Titane64\\Documents\\Blender\\data_mol"
        # Read files and fill classes
        reader = Reader(path_folder)
        molecules = reader.read()
        
        # Generation .blend file
        drawer = Drawer()
        frame = 0
        for mol in molecules:
            bpy.context.scene.frame_set(frame)
            if mol.type == 'cis':
                drawer.draw(mol)
            else:
                print(mol.type)
                drawer.move(mol)
                
            for obj in bpy.data.objects: 
                    obj.keyframe_insert('location', group="LocRot")
            frame += 20
            
        #bpy.context.scene.frame_set(0)
        return {'FINISHED'}
    
# Fonction qui se lance seuelemnt une fois l'add-on 
# activé
def register():
    bpy.utils.register_class(BlendMol)
    print("Start")
    
    
# est une fonction pour décharger tout 
# ce qui a été installé par register, celle-ci 
# est appelée quand l’add-on est désactivé.
def unregister():
    bpy.utils.unregister_class(BlendMol)
    print("End")