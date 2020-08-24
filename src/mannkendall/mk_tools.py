# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains useful tool for the package.
"""

# Import the required packages
import numpy as np

def nb_tie(data, resolution):
    """ Compute the number of data point considered to be equivalent (and to be treated as "ties").

    Args:
        data (ndarray of floats): the data array. Must be 1-D.
        resolution (float): delta value below which two measurements are considered equivalent.

    Return:
        float: amount of ties in the data.

    Todo:
        * fix docstring to better describe the function.
    """

    # If the user gave me a list ... be nice and deal with it.
    if isinstance(data, list) and np.all([isinstance(item, (float, int)) for item in data]):
        data = np.array(data)

    # Otherwise, be unforgiving.
    if not isinstance(data, np.ndarray):
        raise Exception('Ouch! data should be of type ndarray, not: %s' % (type(data)))
    if not isinstance(resolution, (int, float)):
        raise Exception('Ouch! data should be of type float, not: %s' % (type(data)))

    # if everything is a nan, return 0.
    if np.all(np.isnan(data)):
        return np.zeros(1)
    # If there are less than 4 valid data point, return nan.
    if np.count_nonzero(~np.isnan(data)) <= 4:
        return np.nan
    # If all the data is the same, just count it.
    if np.nanmin(data) == np.nanmax(data):
        return np.count_nonzero(~np.isnan(data))

    # If there's nothing weird with the data, let's compute the bin edges.
    bins = np.arange(np.nanmin(data), np.nanmax(data)+resolution, resolution)

    # A sanity check
    if len(bins) < 2:
        raise Exception('Ouch! This error is impossible.')

    # Then compute the number of element sin each bin.
    return np.histogram(data, bins=bins)[0]


def kendall_var(data, t, n):
    """ Compute the variance with ties in the data and ties in time.

    Args:
        data (ndarray of floats): the data array. Must be 1-D.
        t (ndarray of int): number of elements in each tie. Must be 1-D.
        n (ndarray of int): number of non-missing data. Must be 1-D.

    Return:
        float: the variance.

    Note:
        Source: Eq. 4.20, GAW report 133 (A. Sirois), p.30 of annex D.

    """

    # Some sanity checks first
    for item in [data, t, n]:
        if not isinstance(item, np.ndarray):
            raise Exception('Ouch ! Variables must be of type ndarray, not: %s' % (type(item)))
        if np.dim(item) != 1:
            raise Exception('Ouch! Variables must be 1-D array.')

    # What is the length of the data ignoring the nans ?
    l_real = np.count_non_zero(~np.isnan(data))

    var_s = (l_real*(l_real-1)*(2*l_real+5) - np.nansum(t*(t-1)*(2*t+5)) -
             np.nansum(n*(n-1)*(2*n+5))) / 18
    var_s += np.nansum(t*(t-1)*(t-2)) * np.nansum(n*(n-1)*(n-2)) / (9*l_real*(l_real-1)*(l_real-2))
    var_s += np.nansum(t*(t-1)) * np.nansum(n*(n-1)) / (2*l_real*(l_real-1))

    return var_s