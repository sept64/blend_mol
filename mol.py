#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class Mol of the blend_mol project, contain all the data corresponding to a molecule
"""
from blend_mol.atom import Atom


class Mol():
    def __init__(self, path):
        """

        """
        self.path = path # path where is stored
        self.type = None  # cis, cis_detach, trans_detach, trans
        self.data = [] # MOLECULE from file
        self.atoms = [] # list of atoms
        self.bonds = [] # list of links between atoms

    def format(self):
        """
        Format raw entries in attributes to have a nice and usable stuff
        """
        atoms_tmp = []
        for a in self.atoms:
            atom = Atom()
            tmp = a.split('    ')
            atom.number, atom.name = tmp[0].split(' ')
            if len(tmp[-1].split(' ')) == 3:
                atom.z, atom.type = tmp[-1].split(' ')[1:3]
            else:
                atom.z, atom.type = tmp[-1].split(' ')
            atom.z = float(atom.z)
            atom.x = float(tmp[1])
            atom.y = float(tmp[2])

            atoms_tmp.append(atom)
        self.atoms = atoms_tmp

        bonds_tmp = []
        for b in self.bonds:
            b = [eval(o) for o in b.split(' ')[1:]]
            atom1 = self.atoms[b[0]-1]
            atom2 = self.atoms[b[1]-1]
            nb_liaisons = b[2]
            
            bonds_tmp.append([atom1, atom2, nb_liaisons])
            
        self.bonds = bonds_tmp
        