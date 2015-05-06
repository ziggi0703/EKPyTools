#!/usr/bin/env python
from unittest import TestCase
from ekpytools import conversion
import pandas as pd
import ROOT

__author__ = 'Michael Ziegler'


class TestConversion(TestCase):
    def test_load_tree_as_data_frame(self):
        def create_ttree():
            """
            Create a simple root tree for testing
            :return: created tree
            :rtype: ROOT.TTree
            """
            from root_numpy import array2tree
            import numpy as np

            array = np.zeros(10, dtype={'names': ['var1', 'var2', 'var3', 'var4'],
                                        'formats': [np.float, np.float, np.float, np.float]})

            return array2tree(array, 'test_tree')

        test_tree = create_ttree()

        self.assertRaises(TypeError, conversion.convert_ttree_to_data_frame, 'No TTree')
        self.assertIsNotNone(conversion.convert_ttree_to_data_frame(test_tree))

        data_frame = conversion.convert_ttree_to_data_frame(test_tree)
        test_shape = (10, 4)
        test_column_names = ['var1', 'var2', 'var3', 'var4']

        self.assertTupleEqual(test_shape, data_frame.shape)
        self.assertListEqual(test_column_names, data_frame.columns.get_values().tolist())

        self.assertEqual(0., data_frame['var1'][0])

        variable_selection = ['var1', 'var4']

        data_frame_2 = conversion.convert_ttree_to_data_frame(test_tree, variable_selection)
        test_shape_2 = (10, 2)

        self.assertTupleEqual(test_shape_2, data_frame_2.shape)
        self.assertListEqual(variable_selection, data_frame_2.columns.get_values().tolist())

    def test_convert_data_frame_to_ttree(self):
        def get_leaf_names(tree):
            leaf_list = tree.GetListOfLeaves()
            entries = leaf_list.GetEntries()

            return [leaf_list.At(index).GetName() for index in xrange(entries)]

        data_frame = pd.DataFrame({'a': [1, 1.2, 143, 12, -12.1, 121],
                                   'b': [2, 1.3, 144, 13, -12.2, 122],
                                   'c': [3, 1.4, 145, 14, -12.3, 123],
                                   'd': [4, 1.5, 146, 15, -12.4, 124]})

        result_tree = conversion.convert_data_frame_to_ttree(data_frame, 'test_tree')

        self.assertIsInstance(result_tree, ROOT.TTree)
        self.assertEqual(result_tree.GetEntries(), 6)
        self.assertListEqual(get_leaf_names(result_tree), ['a', 'b', 'c', 'd'])

        result_tree_2 = conversion.convert_data_frame_to_ttree(data_frame, 'test_tree_2', columns=['a', 'b'])
        self.assertListEqual(get_leaf_names(result_tree_2), ['a', 'b'])

        self.assertRaises(KeyError, conversion.convert_data_frame_to_ttree, data_frame,
                          'test_tree_3', columns=['d', 'f'])