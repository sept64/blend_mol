#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class Atom of the blend_mol project, contain all the data corresponding to an atom
"""
ATOM_TYPE = ['C', 'H', 'O']


class Atom():
    def __init__(self):
        """

        """
        self.__number = None
        self.__name = None
        self.__type = None  # C, H, O
        self.__order = 0  # C = 4, H = 1, O = 2

        self.x = None  # MOLECULE pos x
        self.y = None  # MOLECULE pos y
        self.z = None  # MOLECULE pos z
        self.__bonded_with = []  # list of linked  atom
        self.renamed = False
        self.bonds = []

    def set_number(self, nb):
        self.__number = int(nb)

    def get_number(self):
        return self.__number

    def set_name(self, name):
        self.__name = str(name)

    def get_name(self):
        return self.__name

    def set_type(self, type):
        try:
            assert (str(type).strip() in ATOM_TYPE)
        except:
            print('**Error: bad type given in atom::set_name : {}'.format(type))
        self.__type = str(type).strip()
        # if self.__type == 'C':
        #     self.__order = 4
        # elif self.__type == 'H':
        #     self.__order = 1
        # elif self.__type == 'O':
        #     self.__order = 2

    def get_type(self):
        return self.__type

    def add_bonded_atom(self, a):
        self.__bonded_with.append(a)
        self.__order = len(self.__bonded_with)

    def is_first(self):
        nb_c = 0
        for a in self.__bonded_with:
            if a.type == 'C':
                nb_c += 1
        if nb_c > 1:
            return False
        else:
            return True

    def get_bonded_with(self):
        return self.__bonded_with

    def is_full(self):
        cmpt = 0
        for b in self.bonds:
            cmpt += b.order
        if self.__order == cmpt:
            return True
        else:
            return False

    number = property(get_number, set_number)
    name = property(get_name, set_name)
    type = property(get_type, set_type)
    bonded_with = property(get_bonded_with)
