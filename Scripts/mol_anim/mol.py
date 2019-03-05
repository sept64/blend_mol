#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class Mol of the blend_mol project, contain all the data corresponding to a molecule
"""
from numpy import arange
from blend_mol.atom import Atom
from blend_mol.state import State

TYPES = ['cis', 'cis_detach', 'trans_detach', 'trans']


class Mol:
    def __init__(self, path):
        """

        """
        self.__states = [State(path, 'cis'), State(path, 'cis_detach'), State(path, 'trans_detach'),
                         State(path, 'trans')]  # Stade can be cis, cis_detach, trans_detach or trans
        self.__path = path  # path where the info of the molecule is stored (files.mol2)

    # Getter and setter
    def get_states(self):
        return self.__states

    def get_state_by_name(self, name):
        try:
            assert (str(name).strip() in TYPES)
        except:
            print('**Error: bad type given in mol::get_states : {}'.format(name))
        return self.__states[TYPES.index(str(name).strip())]

    def get_path(self):
        return self.__path

    states = property(get_states)
    path = property(get_path)

    def read(self):
        """
        Read method used to read and load molecules
        """
        for state in self.__states:
            state.read()

    def iterate_bonds(self, state):
        """
        Iterate on a given state bonds, used to build the rigged bones structure (cis state)
        :return: next bond
        """
        try:
            assert (str(state).strip() in TYPES)
        except:
            print('**Error: bad type given in mol::get_states : {}'.format(state))
        return self.__states[TYPES.index(str(state).strip())].iterate_bonds()