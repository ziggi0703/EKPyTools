#!/usr/bin/env python 
__author__ = 'Michael Ziegler'


from root_numpy import tree2array, array2tree
import pandas as pd
import sys


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
    if variables is not None:
        array = tree2array(tree, branches=variables)
    else:
        array = tree2array(tree, **kwargs)

    data_frame = pd.DataFrame(array)

    return data_frame


def convert_data_frame_to_ttree(data_frame, tree_name, columns=None):
    """
    Convert a pandas.DataFrame to a ROOT.TTree

    :param data_frame: data that is written to a TTree
    :type data_frame: pandas.DataFrame

    :param tree_name: name of the TTree
    :type tree_name: str

    :param columns: columns that are written to the TTree. If None (default), all columns in data_frame
        are written to the TTree
    :type columns: list, None

    :return: converted TTree
    :rtype: ROOT.TTree
    """
    if columns is not None:
        df_data = data_frame[columns]
    else:
        df_data = data_frame
    array = df_data.to_records(index=False)

    return array2tree(array, name=tree_name)
