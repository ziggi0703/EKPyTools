#!/usr/bin/env python 
__author__ = 'Michael Ziegler'


def convert_ttree_to_data_frame(tree, variables=None, **kwargs):
    """
    Convert a ROOT.TTree to a pandas.DataFrame using the root_numpy.tree2array
    function.

    :param tree: tree that is converted
    :type tree: TTree

    :param variables: Specify which variables should be loaded
    :type variables: list

    :return: Converted DataFrame
    :rtype: pandas.DataFrame
    """
    from root_numpy import tree2array
    import pandas as pd

    if variables is not None:
        array = tree2array(tree, branches=variables)
    else:
        array = tree2array(tree, **kwargs)

    data_frame = pd.DataFrame(array)

    return data_frame