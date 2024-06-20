# -*- coding: utf-8 -*-
"""
Created on Mon Apr 22 13:56:44 2024

@author: a423465
"""


def similar_strings(original_string, comparision_string):
    are_similar = False
    results1 = original_string.lower() in comparision_string.lower()
    results2 = comparision_string.lower() in original_string.lower()
    if results1 == True or results2 == True:
        are_similar = True
    else:
        are_similar = False
    return are_similar, comparision_string