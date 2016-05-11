#!/usr/bin/env python 
__author__ = 'Michael Ziegler'

__all__ = ['datahandling', 'conversion', 'plotting']

from .statistics import weighted_mean, weighted_std
from pandas import Series

Series.weighted_mean = weighted_mean
Series.weighted_std = weighted_std