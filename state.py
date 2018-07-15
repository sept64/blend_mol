#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class State of the blend_mol project, contain all the data corresponding to a state of the molecule (atom and bond to create, to move and to destroy
"""
from blend_mol.atom import Atom
from blend_mol.bond import Bond

TYPES = ['cis', 'cis_detach', 'trans_detach', 'trans']


class State():
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

    def get_atom_by_name(self, name):
        for a in self.__atoms:
            if a.name == name:
                return a
        print('**ERROR: no atom found in state::get_atom_by_name name is : {}'.format(name))

    def get_bond_by_name(self, name):
        for b in self.__bonds:
            if b.name == name:
                return b
        print('**ERROR: no bond found in state::get_bond_by_name name is : {}'.format(name))

    def get_atoms(self):
        return self.__atoms

    def get_bonds(self):
        return self.__bonds

    def get_number(self):
        return self.__number

    atoms = property(get_atoms)
    bonds = property(get_bonds)
    number = property(get_number)

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
            self.__atoms.append(atom)

        # Bonds
        for b in tmp_bonds:
            bond = Bond()
            b = [eval(o) for o in b.split(' ')[1:]]
            a1 = self.__get_atom_by_number(b[0])
            a2 = self.__get_atom_by_number(b[1])
            a1.add_bonded_atom(a2)
            a2.add_bonded_atom(a1)
            bond.atoms = [a1, a2]
            bond.order = b[2]
            self.__bonds.append(bond)
            a1.bonds.append(bond)
            a2.bonds.append(bond)

    def rename(self, diffs):
        # Find first C atom == atom not linked with two C
        first_c = self.get_first_c_atom()
        # rename it
        considered_atom = first_c
        considered_atom.name = 'C01'
        count = 2
        # Browse all C atom and rename them
        end = False
        list_c = []
        while not end:
            end = True
            for atom in considered_atom.bonded_with:
                if atom.type == 'C' and atom.renamed == False:
                    if count < 10:
                        atom.name = 'C0{}'.format(count)
                    else:
                        atom.name = 'C{}'.format(count)
                    atom.renamed = True
                    end = False
                    considered_atom = atom
                    count += 1
                    list_c.append(atom)

        # Browse all O atoms linked to the C
        list_o = []
        for considered_atom in list_c:
            for atom in considered_atom.bonded_with:
                if atom.type == 'O' and atom.renamed == False:
                    if len(list_o) + 1 < 10:
                        atom.name = 'O0{}'.format(len(list_o) + 1)
                    else:
                        atom.name = 'O{}'.format(len(list_o) + 1)
                    atom.renamed = True
                    list_o.append(atom)
        # Browse all H atoms linked to the O
        list_h = []
        for considered_atom in list_o:
            for atom in considered_atom.bonded_with:
                if atom.type == 'H' and atom.renamed == False:
                    if len(list_h) + 1 < 10:
                        atom.name = 'H0{}'.format(len(list_h) + 1)
                    else:
                        atom.name = 'H{}'.format(len(list_h) + 1)
                    atom.renamed = True
                    list_h.append(atom)

        if not diffs:
            # Browse all H atoms linked to the C
            for considered_atom in list_c:
                for atom in considered_atom.bonded_with:
                    if atom.type == 'H' and atom.renamed == False:
                        if len(list_h) + 1 < 10:
                            atom.name = 'H0{}'.format(len(list_h) + 1)
                        else:
                            atom.name = 'H{}'.format(len(list_h) + 1)
                        atom.renamed = True
                        list_h.append(atom)

        else:
            # Browse all H atoms linked to the C
            count = len(list_h) + 1
            mem_tmp = []
            print('Detached : ')
            for d in diffs:
                print(d.name)
            for considered_atom in list_c:
                if not considered_atom in diffs:
                    for atom in considered_atom.bonded_with:
                        if atom.type == 'H' and atom.renamed == False:
                            if count < 10:
                                atom.name = 'H0{}'.format(count)
                            else:
                                atom.name = 'H{}'.format(count)
                            atom.renamed = True
                            count += 1
                            list_h.append(atom)
                else:
                    mem_tmp.append(count)
                    count += 1

            i = 0
            print(mem_tmp)
            for atom in self.__atoms:
                if not atom.renamed:
                    if mem_tmp[i] < 10:
                        atom.name = 'H0{}'.format(mem_tmp[i])
                    else:
                        atom.name = 'H{}'.format(mem_tmp[i])
                    i += 1
                    atom.renamed = True

        for b in self.__bonds:
            b.reset_name()

    def get_first_c_atom(self):
        for atom in self.__atoms:
            if atom.type == 'C':
                if atom.is_first():
                    return atom
