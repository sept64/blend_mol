#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class State of the blend_mol project, contain all the data corresponding to a state of the molecule (atom and bond to create, to move and to destroy
"""
from mol_draw.atom import Atom
from mol_draw.bond import Bond

TYPES = ['cis', 'cis_detach', 'trans_detach', 'trans']


class State:
    def __init__(self, path, type):
        """

        """
        try:
            assert (str(type) in TYPES)
        except:
            print('**Error: bad type given in state::__init__ : {}'.format(type))

        self.__path = '{}\\{}.mol2'.format(path, type)  # path where the info of the molecule is stored (files.mol2)
        self.__type = str(type)
        self.__data = []  # @MOLECULE from file
        self.__atoms = []  # list of atoms
        self.__bonds = []  # list of links between atoms
        self.__number = TYPES.index(type)

    def __get_atom_by_number(self, number):
        for a in self.__atoms:
            if a.number == int(number):
                return a

    def get_atoms(self):
        return self.__atoms

    def get_bonds(self):
        return self.__bonds

    def get_number(self):
        return self.__number

    def get_type(self):
        return self.__type

    atoms = property(get_atoms)
    bonds = property(get_bonds)
    number = property(get_number)
    type = property(get_type)

    def read(self):
        """
        Read the corresponding mol2 file and fill State attributes
        """
        bool_data = False
        bool_atoms = False
        bool_bonds = False

        tmp_data = []
        tmp_atoms = []
        tmp_bonds = []

        with open(self.__path, 'r') as mol_file:
            for l in mol_file.readlines():
                if not '#' in l and l != '\n':
                    if 'MOLECULE' in l:
                        bool_data = True
                        bool_atoms = False
                        bool_bonds = False
                    elif 'ATOM' in l:
                        bool_data = False
                        bool_atoms = True
                        bool_bonds = False
                    elif 'BOND' in l:
                        bool_data = False
                        bool_atoms = False
                        bool_bonds = True
                    elif bool_data:
                        tmp_data.append(l)
                    elif bool_atoms:
                        tmp_atoms.append(l)
                    elif bool_bonds:
                        tmp_bonds.append(l)

        # Format raw strings and fill attributes
        # Data
        self.__data = tmp_data

        # Atoms
        for a in tmp_atoms:
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
            if int(atom.number) <= 9:
                atom.name = '{}0{}'.format(atom.type, atom.number)
            self.__atoms.append(atom)

        # Bonds
        for b in tmp_bonds:
            bond = Bond()
            b = [eval(o) for o in b.split(' ')[1:]]
            a1 = self.__get_atom_by_number(b[0])
            a2 = self.__get_atom_by_number(b[1])
            bond.atoms = [a1, a2]
            bond.order = b[2]
            self.__bonds.append(bond)