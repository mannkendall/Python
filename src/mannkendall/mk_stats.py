# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors of the original matlab version of the code listed in
ORIGINAL_AUTHORS.
Copyright (c) 2020 MeteoSwiss, contributors of the Python version of the code listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains the core statistical routines for the package.
"""

# Import the required packages
from datetime import datetime
import numpy as np
from scipy.interpolate import interp1d
from scipy.stats import norm

# Import from this package
from . import mk_tools as mkt

def std_normal_var(s, var_s):
    """ Compute the normal standard variable Z.

    From Gilbert (1987).

    Args:
        s (int): S statistics of the Mann-Kendall test computed from the S_test.
        k_var (float): variance of the time series taking into account the ties in values and time.
                       It should be computed by Kendall_var().

    Returns:
        float: S statistic weighted by the variance.

    """

    # First some sanity checks.
    # Be forgiving if I got a float ...
    if isinstance(s, float) and s.is_integer():
        s = int(s)
    if not isinstance(s, (int)):
        raise Exception('Ouch ! Variable s must be of type int, not: %s' % (type(s)))
    if not isinstance(var_s, (int, float)):
        raise Exception('Ouch ! Variable var_s must be of type float, not: %s' % (type(s)))

    # Deal with the case when s is 0
    if s == 0:
        return 0.0

    # Deal with the other cases.
    return (s - np.sign(s))/var_s**0.5

def sen_slope(obs_dts, obs, k_var, alpha_cl=90.):
    """ Compute Sen's slope.

    Specifically, this computes the median of the slopes for each interval::

        (xj-xi)/(j-i), j>i

    The confidence limits are computed with an interpolation that is important if the number of data
    point is small, such as for yearly averages for a 10 year trend.

    Args:
        obs_dts (ndarray of datetime.datetime): an array of observation times. Must be 1-D.
        obs (ndarray of floats): the data array. Must be 1-D.
        k_var (float): Kendall variance, computed with Kendall_var.
        confidence (float, optional): the desired confidence limit, in %. Defaults to 90.

    Return:
        (float, float, float): Sen's slope, lower confidence limit, upper confidence limit.

    Note:
        The slopes are returned in units of 1/s.

    """

    # Start with some sanity checks
    if not isinstance(alpha_cl, (float, int)):
        raise Exception('Ouch! confidence should be of type int, not: %s' % (type(alpha_cl)))
    if alpha_cl > 100 or alpha_cl < 0:
        raise Exception('Ouch ! confidence must be 0<=alpha_cl<=100, not: %f' % (float(alpha_cl)))
    if not isinstance(k_var, (int, float)):
        raise Exception('Ouch ! The variance must be of type float, not: %s' % (type(k_var)))

    l = len(obs)

    # Let's compute the slope for all the possible pairs.
    d = np.array([item for i in range(0, l-1)
                  for item in list((obs[i+1:l] - obs[i])/mkt.dt_to_s(obs_dts[i+1:l] - obs_dts[i]))])

    # Let's only keep the values that are valid
    d = d[~np.isnan(d)]

    # Let's compute the median slope
    slope = np.nanmedian(d)

    # Apply the confidence limits
    cconf = -norm.ppf((1-alpha_cl/100)/2) * k_var**0.5

    # Note: because python starts at 0 and not 1, we need an additional "-1" to the following
    # values of m_1 and m_2 to match the matlab implementation.
    m_1 = (0.5 * (len(d) - cconf)) - 1
    m_2 = (0.5 * (len(d) + cconf)) - 1

    # Let's setup a quick interpolation scheme to get the best possible confidence limits
    f = interp1d(np.arange(0, len(d), 1), np.sort(d), kind='linear',
                 fill_value=(np.sort(d)[0], np.sort(d)[-1]),
                 assume_sorted=True, bounds_error=False)

    lcl = f(m_1)
    ucl = f(m_2)

    return (float(slope), float(lcl), float(ucl))

def s_test(obs, obs_dts):
    """ Compute the S statistics (Si) for the Mann-Kendall test.

    From Gilbert (1987).

    Args:
        obs (ndarray of floats): the observations array. Must be 1-D.
        obs_dts (ndarray of datetime.datetime): a list of observation datetimes.

    Returns:
        (float, ndarray): S, n.
                          S (float) = double sum on the sign of the difference between data pairs
                          (Si).
                          n (ndarray of int) = number of valid data in each year of the time series

    """
    # If the user gave me a list ... be nice and deal with it.
    if isinstance(obs, list) and np.all([isinstance(item, (float, int)) for item in obs]):
        obs = np.array(obs)

    # Idem for the obs_dts
    if isinstance(obs_dts, list) and np.all([isinstance(item, datetime) for item in obs_dts]):
        obs_dts = np.array(obs_dts)

    # Some sanity checks first
    for item in [obs, obs_dts]:
        if not isinstance(item, np.ndarray):
            raise Exception('Ouch ! I was expecting some numpy.ndarray, not: %s' % (type(item)))
        if np.ndim(item) != 1:
            raise Exception('Ouch ! The numpy.ndarray must have 1 dimensions, not: %i' %
                            (np.ndim(item)))
        if len(item) != len(obs):
            raise Exception('Ouch ! obs and obs_dts should have the same length !')

    # Check that I was indeed given proper datetimes !
    if np.any([not isinstance(item, datetime) for item in obs_dts]):
        raise Exception('Ouch ! I need proper datetime.datetime entities !')

    # Find the limiting years
    obs_years = np.array([item.year for item in obs_dts])
    min_year = np.min(obs_years)
    max_year = np.max(obs_years)

    # An array to keep track of the number of valid data points in each season
    n = np.zeros(max_year - min_year + 1) * np.nan
    # Create a vector to keep track of the results
    sij = np.zeros(max_year - min_year + 1) * np.nan

    for (yr_ind, year) in enumerate(range(min_year, max_year+1)):
        #How valid points do I have :
        n[yr_ind] = np.count_nonzero(~np.isnan(obs[obs_years == year]))

        # Compute s for that year, by summing the signs for the differences with all the upcoming
        # years
        sij[yr_ind] = np.nansum([np.sign(item - obs[obs_years == year])
                                 for yr2 in range(year+1, max_year+1)
                                 for item in obs[obs_years == yr2]])

    return (np.nansum(sij), n)
