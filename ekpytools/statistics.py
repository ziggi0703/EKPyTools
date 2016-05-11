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


def weighted_std(series, weights=None):
    """
    Calculate the weighted standard deviation of a series

    :param series: calculate std of this series
    :type series: pandas.Series

    :param weights: (optional) use these weights
    :type weights: pandas.Series

    :return: weighted std
    :rtype: float
    """
    if weights is None:
        return series.std()

    if len(weights) != len(series):
        raise ValueError('series and weights must have same length.')

    s0 = np.sum(weights)

    if s0 == 0:
        return 0

    s1 = np.sum(weights * series)
    s2 = np.sum(weights * series * series)

    return np.sqrt((s2 / s0 - s1**2/s0**2))