#!/usr/bin/env python 
__author__ = 'Michael Ziegler'


import matplotlib.pyplot as plt


def create_hist_from_data_frame(data, column, bins=100, title=None, xlabel=None, ylabel=None, range=None):
    """
    Create a histogram for a column out of a DataFrame and add
    title and lable  to the plot.

    :param data: Contains the data
    :type data: pandas.DataFrame

    :param column: Name of the column that should be plotted as histogram
    :type column: str

    :param bins: Number of bins used in the histogram
    :type bins: int

    :param title: Title of the plot. If None, no title is set
    :type title: str

    :param xlabel: Label of the x-axis
    :type xlabel: str

    :param ylabel: Label of the y-axis
    :type ylabel: str

    :return: figure
    """
    array = data[column].get_values()

    fig = plt.figure()
    if title is not None:
        plt.title(title)
    if xlabel is not None:
        plt.xlabel(xlabel)
    if ylabel is not None:
        plt.ylabel(ylabel)

    hist = plt.hist(array, bins=bins, range=range)

    return fig