# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains the core statistical routines for the package.
"""

# Import the required packages
import numpy as np
from scipy.interpolate import interp1d

def std_normal_var(s, var_data):
    """ Compute the normalized standard variable Z.

    From Gilbert (1987).

    Args:
        data (float): 1-D numpy array with the data.
        var_data (float): 1-D numpy array with the variance.

    Returns:
        ndarray: the normalised variance.

    Todo:
        * check the docstrings
        * include better reference

    """

    # First some anity checks.
    for item in [s, var_data]:
        if not isinstance(item, (float, int)):
            raise Exception('Ouch ! Variables must be of type float, not: %s' % (type(item)))

    # Deal with the case when s is 0
    if s == 0:
        return 0.0

    # Deal with the other cases.
    return (s + np.sign(s))/var_data**0.5

def sen_slope(time, data, variance, confidence=90.):
    """ Compute Sen's slope.

    Specifically, this computes the median of the slopes for each interval::

        (xj-xi)/(j-i), j>i

    The confidence limits are computed with an interpolation that is important if the number of data
    point is small, such as for yearly averages for a 10 year trend.

    Args:
        time (list of datetime.datetime): a list of observation times.
        data (ndarray of floats): the data array. Must be 1-D.
        variance (float): Kendall variance, computed with Kendall_var.
        confidence (float, optional): the desired confidence limit, in %. Must be 90 or 95.
                                      Defaults to 90.

    Return:
        (float, float, float): Sen's slope, lower confidence limit, upper confidence limit.

    Todo:
        * check/fix this README

    """

    # Start with some sanity checks
    if not isinstance(confidence, (float, int)):
        raise Exception('Ouch! confidence should be of type int, not: %s' % (type(confidence)))
    if confidence not in [90, 95]:
        raise Exception('Ouch ! confidence must be 90 or 95, not: %f' % (float(confidence)))
    if not isinstance(variance, (int, float)):
        raise Exception('Ouch ! The variance must be of type float, not: %s' % (type(variance)))

    for item in [time, data]:
        if np.any(np.isnan(item)):
            raise Exception('Ouch ! Something bad is going to happen because of unexpected nans!')

    l = len(data)

    # Let's compute the slope for all the possible pairs.
    d = np.array([item for i in range(0, l-1)
                  for item in list((data[i+1:l] - data[i])/(time[i+1:l] - time[i]))])

    # Let's compute the median slope
    slope = np.nanmedian(d)

    # Apply the confidence limits
    # Todo: can I simplify this ?
    if confidence == 90:
        cconf = 1.645 * variance**0.5
    elif confidence == 95:
        cconf = 1.96 * variance**0.5
    else:
        raise Exception("Ouch ! This error is impossible.")

    m_1 = 0.5 * (len(d) - cconf)
    m_2 = 0.5 * (len(d) + cconf)

    # Let's setup a quick interpolation scheme to get the best possible confidence limits
    f = interp1d(np.arange(0, len(d), 1), np.sort(d), kind='linear', fill_value=(d[0], d[-1]),
                 assume_sorted=True, bounds_error=False)
    lcl = f(m_1)
    ucl = f(m_2)

    return (slope, lcl, ucl)
