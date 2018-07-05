#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class Reader of the blend_mol project
allows to read mol2 files and to fill and return mol classes
"""

import os
from mol import Mol

class Reader():
    def __init__(self, path):
        """
        path to folder where .mol2 files are
        :param path: path to the folder
        """
        self.dict_files = dict()
        files = os.listdir(path)
        for file in files:
            key = file.split('.')[0]
            self.dict_files[key] = path + '/' + file

        self.__is_read = False

    def get_read(self):
        return self.__is_read

    is_read = property(get_read)

    def read(self):
        """
        Read method used to read and load molecules
        Return molecules tab
        """
        keys = self.dict_files.keys()
        molecules = []

        for key in keys:
            tmp_mol = Mol(self.dict_files[key])
            tmp_mol.type = key
            mol = False
            atom = False
            bond = False

            with open(self.dict_files[key], 'r') as mol_file:
                for l in mol_file.readlines():
                    if not '#' in l and l!='\n':
                        if 'MOLECULE' in l:
                            mol = True
                            atom = False
                            bond = False
                        elif 'ATOM' in l:
                            mol = False
                            atom = True
                            bond = False
                            atom = True
                        elif 'BOND' in l:
                            mol = False
                            atom = False
                            bond = True
                        elif mol:
                            tmp_mol.data.append(l)
                        elif atom:
                            tmp_mol.atom.append(l)
                        elif bond:
                            tmp_mol.bond.append(l)

            tmp_mol.format()
            molecules.append(tmp_mol)
        return molecules