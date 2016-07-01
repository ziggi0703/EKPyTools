#!/usr/bin/env python
from __future__ import division
import numpy as np
import pandas as pd
import copy


class Histogram(object):
    """
    Base Histogram class

    :param title:
    :type title:

    :param bins:
    :type bins: int

    :param x_limits: limits of the histogram. (lower, upper)
    :type x_limits: tuple

    :param log: Use a logarithmic binning. Default: False.
    :type log: bool

    :param normed: Normalize the histogram. Default: False
    :type normed: bool
    """
    def __init__(self, title, bins, x_limits, log=False, normed=False):
        self._title = title
        self._n_bins = bins
        self._x_limits = x_limits
        self._log = log
        self._normed = normed

        if not log:
            self.__bins = np.linspace(x_limits[0], x_limits[1], bins + 1, endpoint=True)
        else:
            self.__bins = np.logspace(np.log10(x_limits[0]), np.log10(x_limits[1]), bins + 1, endpoint=True)
        self.__bin_content = np.zeros(self._n_bins)
        self.__sum_weights_sq = np.zeros(self._n_bins)
        self._n_entries = 0

    def __str__(self):
        return '{}: {}'.format(type(self), self._title)

    def __add__(self, other):
        """
        Add other to the current histogram. Bin contents are added and errors are quadratically
        added.

        :param other:
        :type other: Histogram

        :return: hist with the sum of self and other as bin content.
        :rtype: Histogram
        """
        try:
            self._check_hist_consistency(other)
        except Exception, e:
            raise e
        hist = Histogram('sum', bins=self._n_bins, x_limits=self._x_limits, log=self._log)
        hist.bin_content = self.bin_content + other.bin_content
        hist.bin_error = np.sqrt(self.bin_error**2 + other.bin_error**2)

        return hist

    def __neg__(self):
        temp = copy.deepcopy(self)
        temp.bin_content *= -1
        return temp

    def __sub__(self, other):
        try:
            self._check_hist_consistency(other)
        except Exception, e:
            raise e
        temp = copy.deepcopy(other)
        temp.bin_content *= -1

        res = self + temp

        if self is other:
            res.bin_error = np.zeros(self._n_bins)

        return res

    def __div__(self, other):
        return self.divide(other)

    def __truediv__(self, other):
        return self.__div__(other)

    @property
    def bins(self):
        return self.__bins

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, title):
        self._title = title

    @property
    def bin_content(self):
        """
        Get an array with the bin content.

        :return: bin content
        :rtype: numpy.ndarry
        """
        return self.__bin_content

    @bin_content.setter
    def bin_content(self, content):
        """
        Set bin content.

        :param content: New bin content
        :type content: numpy.ndarray
        """
        try:
            self._check_content_consistency(content)
        except Exception, ex:
            raise ex

        self.__bin_content = content

    @property
    def bin_error(self):
        """
        Get the error on each bin in an array. Calculated as sqrt of sum of weight**2

        :return: errors
        :rtype: numpy.ndarray
        """
        return np.sqrt(self.__sum_weights_sq)

    @bin_error.setter
    def bin_error(self, errors):
        """
        Set new bin errors

        :param errors: new errors
        :type errors: numpy.ndarray
        """
        try:
            self._check_content_consistency(errors)
        except Exception, ex:
            raise ex

        self.__sum_weights_sq = errors**2

    def divide(self, hist, inplace=False):
        """
        Divide the Histrogram by another Histogram hist.

        :param hist: divisor
        :type hist: Histogram, float

        :param inplace: If True, self will be updated.
        :type inplace: bool

        :return: Result of division
        :rtype: Histogram
        """
        try:
            self._check_hist_consistency(hist)
        except ValueError, e:
            raise e

        content = self.bin_content/hist.bin_content

        new_errors_sq = (self.bin_error**2 * hist.bin_content**2 +
                         hist.bin_error**2 * self.bin_content**2)/(hist.bin_content**4)

        if inplace:
            self.bin_content = content
            self.bin_error = new_errors_sq
            return self
        else:
            new_hist = Histogram('{}/{}'.format(self.title, hist.title),
                                 self._n_bins, self._x_limits, log=self._log)
            new_hist.bin_content = content
            new_hist.bin_error = np.sqrt(new_errors_sq)
            return new_hist

    def _check_content_consistency(self, content):
        if not isinstance(content, np.ndarray):
            raise TypeError('content/error must be of {}'.format(np.ndarray))
        if content.size != self._n_bins:
            raise ValueError('content/error must have same number of bins.'
                             ' Needed: {}, given {}'.format(content.size, self._n_bins) )

    def _check_hist_consistency(self, hist):
        if self._n_bins != hist._n_bins:
            raise ValueError('Histograms must have same number of bins.')
        if self._x_limits != hist._x_limits:
            raise ValueError('Histograms must have the same range')
        if self._log != hist._log:
            raise ValueError('Both hists must be log or not.')

    def fill(self, values, weights=None):
        """
        Fill histogram with values.

        :param values:
        :type values: float, numpy.array, pandas.Series

        :param weights: If weights are given, they are used to calculate the error in the bins and bin content is
            sum of the weights in each bin.
        :type weights: float, numpy.array
        """
        if isinstance(values, float):
            values = np.array([values])
        if isinstance(values, pd.Series):
            values = values.values
        if weights is None:
            weights = np.full(values.size, 1.)
        elif isinstance(weights, float):
            weights = np.array(weights)
        elif isinstance(weights, pd.Series):
            weights = weights.values

        if values.size != weights.size:
            raise ValueError('values and weights must have same number of entries.')

        hist, bins = np.histogram(values, bins=self._n_bins, range=self._x_limits,
                                  weights=weights, density=self._normed)

        self.__sum_weights_sq += self._calc_sum_weights_squared(values, bins, weights)

        if self._normed:
            self.__sum_weights_sq *= (1/(weights.sum()))**2

        if self.__bins is None:
            self.__bins = bins

        self.__bin_content += hist
        self._n_entries += len(values)

    def _calc_sum_weights_squared(self, series, bins, weights=None):
        """
        Calculate the sum of the squared weights for each bin of a histogram. If weights are None,
        they are set to 1 -> Sum is equal to the number of events in the bin.

        :param series: Contains the values
        :type series: numpy.array

        :param bins: The used bins in the histogram
        :type bins: numpy.array

        :param weights: event by event weights
        :type weights: numpy.array

        :return: sums per bins
        :rtype: np.ndarray
        """
        if weights is None:
            weights = np.full(len(series), 1)

        bin_sum_weight_sq = np.zeros(self._n_bins)
        bin_indices = np.digitize(series, bins, right=False)

        for index, value, weight in zip(bin_indices, series, weights):
            if 0 < index <= self._n_bins:
                bin_sum_weight_sq[index - 1] += weight**2

        return bin_sum_weight_sq
