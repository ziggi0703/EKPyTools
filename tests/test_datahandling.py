from unittest import TestCase
import os
from ekpytools import datahandling
import ConfigParser
import inspect
from ROOT import TFile, TTree, TChain
import numpy as np
from root_numpy import array2root

__author__ = 'Michael Ziegler'


class TestDataHandling(TestCase):
    def _create_root_file(self, file_name='data.root', tree_name='data'):
        location = os.path.join(os.getcwd(), os.path.dirname(inspect.getfile(inspect.currentframe())))
        file_name = os.path.join(location, file_name)
        entries = 100

        if os.path.isfile(file_name):
            return file_name, tree_name, entries

        array = np.zeros(entries, dtype={'names': ['var1', 'var2', 'var3', 'var4', 'var5'],
                                         'formats': ['f4', 'f4', 'f4', 'f4', 'f4']})

        array2root(array, file_name, treename=tree_name)
        return file_name, tree_name, entries

    def _create_config_file(self, file_name='data.config'):
        location = os.path.join(os.getcwd(), os.path.dirname(inspect.getfile(inspect.currentframe())))
        file_name = os.path.join(location, file_name)

        with open(file_name, 'w') as config_file:
            content = """[variables]
var1: 0.1
var2: 0.1
var3: 0.4

[boolSection]
test0: True
test1: False
test2: Yes
test3: No
test4: 1
test5: 0
"""
            config_file.write(content)
        return file_name

    def test_load_trees_from_file(self):
        root_file, tree, entries = self._create_root_file()
        self.assertRaises(IOError, datahandling.load_trees_from_file, "abcdef")

        test_trees, input_file = datahandling.load_trees_from_file(root_file)

        self.assertIsInstance(input_file, TFile)
        self.assertEqual(1, len(test_trees))

        self.assertTrue('data' in test_trees)
        self.assertEqual(entries, test_trees['data'].GetEntries())

    def test_load_tree_from_file(self):
        self.assertRaises(IOError, datahandling.load_tree_from_file,
                          "abcdef", "ghi")

        root_file, tree_name, entries = self._create_root_file()
        wrong_tree_name = "wrongName"
        test_tree, input_file = datahandling.load_tree_from_file(root_file, wrong_tree_name)

        self.assertIsNone(test_tree)

        test_tree, input_file = datahandling.load_tree_from_file(root_file, tree_name)

        self.assertIsInstance(test_tree, TTree)
        self.assertEqual(entries, test_tree.GetEntries())

    def test_load_chain_from_files(self):
        self.assertRaises(IOError, datahandling.load_chain_from_files,
                          "abcd", "ghi")

        self.assertRaises(TypeError, datahandling.load_chain_from_files,
                          999, "ghi")

        root_file, proper_tree_name, entries = self._create_root_file()
        chain = datahandling.load_chain_from_files([root_file],
                                                   proper_tree_name)[0]

        self.assertIsInstance(chain, TChain)
        self.assertEqual(entries, chain.GetEntries())

    def test_load_config_section(self):
        config_file_name = self._create_config_file()
        section = "variables"

        self.assertRaises(IOError, datahandling.load_config_section, "DOES_NOT_EXIST", section)
        self.assertRaises(ConfigParser.NoSectionError, datahandling.load_config_section,
                          config_file_name, "NOT_IN_CONFIG")

        variables_section = datahandling.load_config_section(config_file_name, section)
        self.assertEqual(variables_section['var1'], 0.1)
        self.assertEqual(variables_section['var2'], 0.1)
        self.assertEqual(variables_section['var3'], 0.1)


        bool_section0 = datahandling.load_config_section(config_file_name, 'boolSection',
                                                         ['test0', 'test1', 'test2',
                                                          'test3', 'test4', 'test5'])

        bool_section1 = datahandling.load_all_config_sections(config_file_name,
                                                              ['test0', 'test1',
                                                               'test2', 'test3',
                                                               'test4', 'test5'])['boolSection']

        self.assertEqual(bool_section0, bool_section1)

        self.assertEqual(bool_section0['test0'], True)
        self.assertEqual(bool_section0['test1'], False)
        self.assertEqual(bool_section0['test2'], True)
        self.assertEqual(bool_section1['test3'], False)
        self.assertEqual(bool_section1['test4'], True)
        self.assertEqual(bool_section1['test5'], False)