#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class Bond of the blend_mol project, contain all the data corresponding to a link between two atoms
"""
from blend_mol.atom import Atom


class Bond:
    def __init__(self):
        """

        """
        self.__atoms = None
        self.__order = None
        self.__name = None

    def set_atoms(self, tab_a):
        self.__atoms = [tab_a[0], tab_a[1]]
        self.__name = '{}_{}'.format(tab_a[0].name, tab_a[1].name)

    def set_order(self, nb):
        self.__order = int(nb)

    def get_order(self):
        return self.__order

    def get_atoms(self):
        return self.__atoms

    def get_name(self):
        return self.__name

    def revert_name_and_atoms(self):
        self.__name = '{}_{}'.format(self.__atoms[1].name, self.__atoms[0].name)
        self.__atoms = [self.__atoms[1], self.__atoms[0]]

    order = property(get_order, set_order)
    atoms = property(get_atoms, set_atoms)
    name = property(get_name)
