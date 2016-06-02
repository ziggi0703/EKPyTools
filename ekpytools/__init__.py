#!/usr/bin/env python 
__author__ = 'Michael Ziegler'

__all__ = ['datahandling', 'conversion', 'plotting']

from .statistics import weighted_mean, weighted_std, empirical_cdf
from pandas import Series, DataFrame

Series.weighted_mean = weighted_mean
Series.weighted_std = weighted_std

DataFrame.empirical_cdf = empirical_cdf
