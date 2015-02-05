#!/usr/bin/env python
from unittest import TestCase
from ekpytools import conversion
import numpy as np

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

