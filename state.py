#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class State of the blend_mol project, contain all the data corresponding to a state of the molecule (atom and bond to create, to move and to destroy
"""
from blend_mol.atom import Atom
from blend_mol.bond import Bond

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

        self.__it_atom = None
        self.__it_done_bonds = []
        self.__it_done_atoms = []
        self.__it_was_done_one_time = False
        self.__index_iteration = 0

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
            if b.equals_to(name):
                return b
        print('**ERROR: no bond found in state::get_bond_by_name name is : {}, state is : '.format(name, self.__type))
        print('**INFO: bonds in this state are : {}'.format([o.name for o in self.__bonds]))

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

    def iterate_bonds(self):
        """
        Iterate on the state bonds, used to build the rigged bones structure (cis state)
        :return: next bond
        """
        if self.__it_atom and not self.__it_was_done_one_time:
            # Go get all the bonds involving current atom
            tmp_bonds = []
            for b in self.__bonds:
                if self.__it_atom.name in b.name:
                    tmp_bonds.append(b)

            # Check if anyone is not done yet
            bonds_to_do = list(set(tmp_bonds) - set(self.__it_done_bonds))
            if len(bonds_to_do) != 0:
                print([o.name for o in bonds_to_do])
                # Check first if there is an undone bond linking our current atom to an H atom
                for b in bonds_to_do:
                    if 'H' in [o for o in b.name.split('_') if o != self.__it_atom.name][0]:
                        if b.name.split('_').index(self.__it_atom.name) == 1:
                            b.revert_name_and_atoms()
                        self.__it_done_bonds.append(b)
                        return self.__it_done_bonds[-1]
                # Then check if there is an undone  bond linking our current atom to an O atom
                for b in bonds_to_do:
                    if 'O' in [o for o in b.name.split('_') if o != self.__it_atom.name][0]:
                        if b.name.split('_').index(self.__it_atom.name) == 1:
                            b.revert_name_and_atoms()
                        self.__it_done_bonds.append(b)
                        return self.__it_done_bonds[-1]
                # Finally check if there is an undone bond linking our current atom to an C atom
                for b in bonds_to_do:
                    if 'C' in [o for o in b.name.split('_') if o != self.__it_atom.name][0]:
                        if b.name.split('_').index(self.__it_atom.name) == 1:
                            b.revert_name_and_atoms()
                        self.__it_done_bonds.append(b)
                        return self.__it_done_bonds[-1]

            else:  # We've done every bond of the present atom
                last_bond_done = self.__it_done_bonds[-1]
                other_atom_name = [o for o in last_bond_done.name.split('_') if o != self.__it_atom.name][0]
                self.__it_atom = self.get_atom_by_name(other_atom_name)
                if self.__it_atom in self.__it_done_atoms:
                    # We finished our first iteration, all bonds and atoms are kept in memory to accelerate other
                    # iterations
                    self.__it_was_done_one_time = True
                    print('None of iteration finished and it was done = true (first time)\n')
                    return None
                else:
                    # Go get all the bonds involving current atom
                    tmp_bonds = []
                    for b in self.__bonds:
                        if self.__it_atom.name in b.name:
                            tmp_bonds.append(b)

                    # Check if anyone is not done yet
                    bonds_to_do = list(set(tmp_bonds) - set(self.__it_done_bonds))
                    if len(bonds_to_do) != 0:
                        # Check first if there is an undone bond linking our current atom to an H atom
                        for b in bonds_to_do:
                            if 'H' in [o for o in b.name.split('_') if o != self.__it_atom.name][0]:
                                if b.name.split('_').index(self.__it_atom.name) == 1:
                                    b.revert_name_and_atoms()
                                self.__it_done_bonds.append(b)
                                return self.__it_done_bonds[-1]
                        # Then check if there is an undone  bond linking our current atom to an O atom
                        for b in bonds_to_do:
                            if 'O' in [o for o in b.name.split('_') if o != self.__it_atom.name][0]:
                                if b.name.split('_').index(self.__it_atom.name) == 1:
                                    b.revert_name_and_atoms()
                                self.__it_done_bonds.append(b)
                                return self.__it_done_bonds[-1]
                        # Finally check if there is an undone bond linking our current atom to an C atom
                        for b in bonds_to_do:
                            if 'C' in [o for o in b.name.split('_') if o != self.__it_atom.name][0]:
                                if b.name.split('_').index(self.__it_atom.name) == 1:
                                    b.revert_name_and_atoms()
                                self.__it_done_bonds.append(b)
                                return self.__it_done_bonds[-1]
                    else:
                        print('None of iteration finished and it was done = false\n')
                        self.__it_was_done_one_time = True
                        return None
        elif not self.__it_was_done_one_time:  # First time
            for a in self.__atoms:
                if a.name == 'H50':  # TODO : find a best solution than this hardcoded one
                    for b in self.__bonds:
                        if 'H50' in b.name:
                            self.__it_atom = self.get_atom_by_name('H50')
                            if b.name.split('_').index(self.__it_atom.name) == 1:
                                b.revert_name_and_atoms()
                            self.__it_done_bonds.append(b)
                            self.__it_done_atoms = []
                            break

        else: # Not the first time, just iterate on __it_done_bonds
            if self.__index_iteration < len(self.__it_done_bonds):
                bond = self.__it_done_bonds[self.__index_iteration]
                self.__index_iteration += 1
                return bond
            else:
                # Iteration finished
                self.__index_iteration = 0
                print('None of iteration finished and it was done = true\n')
                return None

        return self.__it_done_bonds[-1]

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
