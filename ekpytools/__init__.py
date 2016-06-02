#!/usr/bin/env python 
__author__ = 'Michael Ziegler'

__all__ = ['datahandling', 'conversion', 'plotting']

from .statistics import weighted_mean, weighted_std, ecdf_of_column, ecdf_of_series
from pandas import Series, DataFrame

Series.weighted_mean = weighted_mean
Series.weighted_std = weighted_std
Series.empirical_cdf = ecdf_of_series

DataFrame.empirical_cdf = ecdf_of_column

