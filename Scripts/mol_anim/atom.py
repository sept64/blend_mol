#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class Atom of the blend_mol project, contain all the data corresponding to an atom
"""
ATOM_TYPE = ['C', 'H', 'O']


class Atom:
    def __init__(self):
        """

        """
        self.__number = None
        self.__name = None
        self.__type = None  # C, H, O

        self.x = None  # MOLECULE pos x
        self.y = None  # MOLECULE pos y
        self.z = None  # MOLECULE pos z

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

    def get_type(self):
        return self.__type

    number = property(get_number, set_number)
    name = property(get_name, set_name)
    type = property(get_type, set_type)
