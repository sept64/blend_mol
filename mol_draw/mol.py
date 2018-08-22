#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class Mol of the blend_mol project, contain all the data corresponding to a molecule
"""
from mol_draw.state import State


class Mol:
    def __init__(self, path):
        """

        """
        self.TYPES = ['cis', 'cis_detach', 'trans_detach', 'trans']  # Const types
        self.__states = [State(path, 'cis'), State(path, 'cis_detach'), State(path, 'trans_detach'),
                         State(path, 'trans')]  # Stade can be cis, cis_detach, trans_detach or trans
        self.__path = path  # path where the info of the molecule is stored (files.mol2)

    # Getter and setter
    def get_states(self):
        return self.__states

    def get_state_by_name(self, name):
        try:
            assert (str(name).strip() in self.TYPES)
        except:
            print('**Error: bad type given in mol::get_states : {}'.format(name))
        return self.__states[self.TYPES.index(str(name).strip())]

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
