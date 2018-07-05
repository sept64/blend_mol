#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Class Atom of the blend_mol project, contain all the data corresponding to an atom
"""


class Atom():
    def __init__(self):
        """

        """
        self.number = None
        self.name = None
        self.type = None    # C, H, O
        self.x = None   # MOLECULE pos x
        self.y = None   # MOLECULE pos y
        self.z = None   # MOLECULE pos z