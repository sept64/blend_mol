#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class Iterator of the mol_rig project
allows to iterate on a (cis) molecule
"""
import bpy


class Iterator():
    def __init__(self):

        self.__it_atom = None
        self.__it_done_bonds = []
        self.__it_done_atoms = []
        self.__it_was_done_one_time = False
        self.__index_iteration = 0

        self.__bonds = []
        self.__atoms = []  # list of atoms

        self.__init_bond_list()

    def __init_bond_list(self):
        for o in bpy.data.objects:
            if 'cis' in o.name:
                if o.name.count('_') == 2:
                    self.__bonds.append(o)
                if o.name.count('_') == 1:
                    self.__atoms.append(o)
        print('Bonds are : {}'.format([o.name for o in self.__bonds]))

    def __get_atom_by_name(self, name):
        for a in self.__atoms:
            if a.name == name + '_cis':
                return a
        print('**ERROR: no atom found in iterator::__get_atom_by_name name is : {}'.format(name))

    def get_bonds(self):
        return self.__bonds

    bonds = property(get_bonds)

    def next(self):
        """
        Iterate on the bonds, used to build the rigged bones structure (cis state)
        :return: next bond
        """
        if self.__it_atom and not self.__it_was_done_one_time:
            # Go get all the bonds involving current atom
            tmp_bonds = []
            for b in self.__bonds:
                if self.__it_atom in b.name:
                    tmp_bonds.append(b)

            # Check if anyone is not done yet
            bonds_to_do = list(set(tmp_bonds) - set(self.__it_done_bonds))
            if len(bonds_to_do) != 0:
                print([o.name for o in bonds_to_do])
                # Check first if there is an undone bond linking our current atom to an H atom
                for b in bonds_to_do:
                    if 'H' in [o for o in b.name.split('_')[0:2] if o != self.__it_atom][0]:
                        if b.name.split('_').index(self.__it_atom) == 1:
                            b.name = '{}_{}_{}'.format(b.name.split('_')[1], b.name.split('_')[0], b.name.split('_')[2])
                        self.__it_done_bonds.append(b)
                        return self.__it_done_bonds[-1]
                # Then check if there is an undone  bond linking our current atom to an O atom
                for b in bonds_to_do:
                    if 'O' in [o for o in b.name.split('_')[0:2] if o != self.__it_atom][0]:
                        if b.name.split('_').index(self.__it_atom) == 1:
                            b.name = '{}_{}_{}'.format(b.name.split('_')[1], b.name.split('_')[0], b.name.split('_')[2])
                        self.__it_done_bonds.append(b)
                        return self.__it_done_bonds[-1]
                # Finally check if there is an undone bond linking our current atom to an C atom
                for b in bonds_to_do:
                    if 'C' in [o for o in b.name.split('_')[0:2] if o != self.__it_atom][0]:
                        if b.name.split('_').index(self.__it_atom) == 1:
                            b.name = '{}_{}_{}'.format(b.name.split('_')[1], b.name.split('_')[0], b.name.split('_')[2])
                        self.__it_done_bonds.append(b)
                        return self.__it_done_bonds[-1]

            else:  # We've done every bond of the present atom
                last_bond_done = self.__it_done_bonds[-1]
                other_atom_name = [o for o in last_bond_done.name.split('_') if o != self.__it_atom][0]
                self.__it_atom = self.__get_atom_by_name(other_atom_name).name.split('_')[0]
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
                        if self.__it_atom in b.name:
                            tmp_bonds.append(b)

                    # Check if anyone is not done yet
                    bonds_to_do = list(set(tmp_bonds) - set(self.__it_done_bonds))
                    if len(bonds_to_do) != 0:
                        # Check first if there is an undone bond linking our current atom to an H atom
                        for b in bonds_to_do:
                            if 'H' in [o for o in b.name.split('_')[0:2] if o != self.__it_atom][0]:
                                if b.name.split('_').index(self.__it_atom) == 1:
                                    b.name = '{}_{}_{}'.format(b.name.split('_')[1], b.name.split('_')[0],
                                                               b.name.split('_')[2])
                                self.__it_done_bonds.append(b)
                                return self.__it_done_bonds[-1]
                        # Then check if there is an undone  bond linking our current atom to an O atom
                        for b in bonds_to_do:
                            if 'O' in [o for o in b.name.split('_')[0:2] if o != self.__it_atom][0]:
                                if b.name.split('_').index(self.__it_atom) == 1:
                                    b.name = '{}_{}_{}'.format(b.name.split('_')[1], b.name.split('_')[0],
                                                               b.name.split('_')[2])
                                self.__it_done_bonds.append(b)
                                return self.__it_done_bonds[-1]
                        # Finally check if there is an undone bond linking our current atom to an C atom
                        for b in bonds_to_do:
                            if 'C' in [o for o in b.name.split('_')[0:2] if o != self.__it_atom][0]:
                                if b.name.split('_').index(self.__it_atom) == 1:
                                    b.name = '{}_{}_{}'.format(b.name.split('_')[1], b.name.split('_')[0],
                                                               b.name.split('_')[2])
                                self.__it_done_bonds.append(b)
                                return self.__it_done_bonds[-1]
                    else:
                        print('None of iteration finished and it was done = false\n')
                        self.__it_was_done_one_time = True
                        return None
        elif not self.__it_was_done_one_time:  # First time, user has to select the first atom
            self.__it_atom = bpy.context.selected_objects[0].name.split('_')[0]
            for b in self.__bonds:
                if self.__it_atom in b.name:
                    if b.name.split('_').index(self.__it_atom) == 1:
                        b.name = '{}_{}_{}'.format(b.name.split('_')[1], b.name.split('_')[0], b.name.split('_')[2])
                    self.__it_done_bonds.append(b)
                    self.__it_done_atoms = []
                    break

        else:  # Not the first time, just iterate on __it_done_bonds
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
