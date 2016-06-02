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


def ecdf_of_column(frame, column, weight_column=None):
    """
    Calculate the empirical CDF of the values of column.

    :param frame: data
    :type frame: pandas.DataFrame

    :param column: Column name in frame
    :type column: str

    :param weight_column: (optional) use values of the column as weights
    :type weight_column: str

    :return: Empirical CDF
    :rtype:
    """
    if weight_column is None:
        counts = frame[column].value_counts(normalize=True)
    else:
        counts = frame.groupby(column)[weight_column].sum()/frame[weight_column].sum()
    rv = counts.sort_index().cumsum()

    rv.name = 'CDF_{}'.format(column)
    rv.index.name = None

    return rv


def ecdf_of_series(self, weights=None):
    """
    Calculate the empirical CDF of the values.

    :param self:
    :type self: pandas.Series

    :param weights: (optional) events weights
    :type weights: pandas.Series

    :return: CDF
    :rtype: pandas.Series
    """
    if weights is None:
        counts = self.value_counts(normalize=True)
    else:
        if len(weights) != len(self):
            raise ValueError('series and weights must have same length.')

        frame = pd.DataFrame(dict(values=self, weights=weights))

        counts = frame.groupby('values')['weights'].sum()/frame['weights'].sum()

    rv = counts.sort_index().cumsum()
    rv.name = 'CDF_{}'.format(self.name) if self.name is not None else None
    rv.index.name = None

    return rv


