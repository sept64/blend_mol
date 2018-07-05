#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class Mol of the blend_mol project, contain all the data corresponding to a molecule
"""
from atom import Atom


class Mol():
    def __init__(self, path):
        """

        """
        self.path = path # path where is stored
        self.type = None  # cis, cis_detach, trans_detach, trans
        self.data = [] # MOLECULE from file
        self.atom = [] # list of atoms
        self.bond = [] # list of links between atoms

    def format(self):
        """
        Format raw entries in attributes to have a nice and usable stuff
        """
        atom_tmp = []
        atom = Atom()
        for a in self.atom:
            tmp = a.split('    ')
            atom.number, atom.name = tmp[0].split(' ')
            if len(tmp[-1].split(' ')) == 3:
                atom.z, atom.type = tmp[-1].split(' ')[1:3]
            else:
                atom.z, atom.type = tmp[-1].split(' ')
            atom.z = float(atom.z)
            atom.x = float(tmp[1])
            atom.y = float(tmp[2])

            atom_tmp.append(atom)

        self.atom = atom_tmp
