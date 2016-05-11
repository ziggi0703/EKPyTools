#!/usr/bin/env python
from __future__ import division, absolute_import, print_function
import pandas as pd
import numpy as np


def weighted_mean(series, weights=None):
    """
    Calculate the weighted mean of a series.

    :param series: calculate mean of this series
    :type series: pandas.Series

    :param weights: (optional) series with weights.
    :type weights: pandas.Series

    :return: mean of the series
    :rtype: float
    """
    if weights is None:
        return series.mean()

    if len(weights) != len(series):
        raise ValueError('series and weights must have same length.')

    return np.sum(weights * series) / np.sum(weights)