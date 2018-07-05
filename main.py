#!/usr/bin/env python
# -*- coding: utf8 -*-

"""
Main function of the blend_mol project
"""
from reader import Reader

def main(path_folder):
    """
    Main function
    """
    # Read files and fill classes
    reader = Reader(path_folder)
    molecules = reader.read()
    print(molecules)
    # Generation .blend file


if __name__ == '__main__':
    name = '/home/tsotirop/Documents/test_mol'
    main(name)