from ConfigParser import ConfigParser
from __builtin__ import isinstance

__author__ = 'Michael Ziegler'

from ROOT import TFile, TTree, TLeaf, TChain
import os.path
import glob


def write_to_csv(values, csv_file, separator=","):
    """
    Write values to a csv file

    :param values: List of values which are written to the csv file
    :type values: list

    :param csv_file: opened file to which the values are written
    :type csv_file: file

    :param separator: Columns in the file are separated with this char
    :type separator: str
    """
    if isinstance(values, str):
        values = [values]

    values = [str(value) for value in values]

    csv_file.write(separator.join(values) + "\n")


def load_trees_from_file(file_name):
    """
    Load all TTree from a ROOT file

    @param file_name Name of ROOT file
    @return dict with name of tree as key and the tree as value, ROOT file
    """

    if not os.path.isfile(file_name):
        raise IOError("File %s does not exist." % file_name)
    root_file = TFile(file_name)

    if root_file.IsZombie():
        raise IOError("Can't open root file %s." % file_name)

    keys = root_file.GetListOfKeys()

    trees = {}

    for key in keys:
        tree = root_file.Get(key.GetName())

        if isinstance(tree, TTree):
            trees[key.GetName()] = tree

    return trees, root_file


def load_tree_from_file(file_name, tree_name):
    """
    Load TTree with name tree_name from ROOT file with name file_name

    @return TTree, TFile
    """
    if not os.path.isfile(file_name):
        raise IOError("File %s does not exist." % file_name)
    file = TFile(file_name)

    if file.IsZombie():
        raise IOError("Can't open root file %s." % file_name)

    key_names = [key.GetName() for key in file.GetListOfKeys()]

    tree = None
    if tree_name in key_names:
        tree = file.Get(tree_name)
        if not isinstance(tree, TTree):
            tree = None

    return tree, file


def load_chain_from_files(file_names, tree_name):
    """
    Load TTree with tree_name from multiple files in a TChain.

    @param file_names List with ROOT file names or basestring "*" is allowed
    @param tree_name TTree with this name is loaded from files
    @return TChain
    """
    file_name_list = None

    if isinstance(file_names, basestring):
        if '*' in file_names:
            file_name_list = glob.glob(file_names)
        else:
            file_name_list = [file_names]
    elif isinstance(file_names, list):
        file_name_list = file_names
    else:
        raise TypeError("%s is not a str or list of str" % file_names)

    data_chain = TChain(tree_name)
    added_files = 0
    for file in file_name_list:
        if not os.path.isfile(file):
            raise IOError("File %s does not exist." % file)

        added_files += data_chain.AddFile(file)

    return data_chain, added_files


def load_config_section(config_file, section, bool_options=None):
    """
    Load a configuration for a section from a config file
    using ConfigParser
    """

    config_parser = ConfigParser()
    read_files = config_parser.read(config_file)

    if not read_files:
        raise IOError("Config file %s does not exist" % config_file)

    return load_options_from_parser(config_parser, section,
                                    bool_options=bool_options)


def load_options_from_parser(config_parser, section, bool_options=None):
    """
    Load options for a specific section from a config parser
    """
    options = config_parser.options(section)

    option_dict = {}

    if bool_options is not None and isinstance(bool_options, basestring):
        bool_options = [bool_options]

    for option in options:
        if bool_options is not None and option in bool_options:
            option_dict[option] = config_parser.getboolean(section, option)
        else:
            option_dict[option] = config_parser.get(section, option)

    return option_dict


def load_all_config_sections(config_file, bool_options=None):
    """
    Load every section in a configuration file

    :param config_file: Path to config file
    :type config_file:

    :param bool_options: list with boolean options
    :type bool_options:

    :return: Dictionary with all options per section
    :rtype: dict
    """
    config_parser = ConfigParser()

    read_files = config_parser.read(config_file)

    all_sections = config_parser.sections()

    sections_options = {}

    for section in sorted(all_sections):
        sections_options[section] = load_options_from_parser(config_parser, section,
                                                             bool_options=bool_options)

    return sections_options