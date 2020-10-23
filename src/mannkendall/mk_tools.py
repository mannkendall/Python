# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors of the original matlab version of the code listed in
ORIGINAL_AUTHORS.
Copyright (c) 2020 MeteoSwiss, contributors of the Python version of the code listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains useful tools for the package.
"""

# Import the required packages
import numpy as np
from scipy import stats as spstats

from statsmodels.tsa import stattools

def de_sort(vals, inds):
    """ De-sort an array of values vals that were sorted according to the indices inds.

    Args:
        vals (ndarray): a 1-D array to de-sort.
        inds (ndarray of int): the sorting indices.

    Returns:
        ndarray: the de-sorted array.

    """

    # Create the de-sorted structure
    out = np.zeros_like(vals)

    # Loop through every item.
    for (sorted_ind, unsorted_ind) in enumerate(inds):
        out[unsorted_ind] = vals[sorted_ind]

    return out


def dt_to_s(time_deltas):
    """ A convenience function that converts an array of datetime.timedeltas into an array of
    floats corresponding to the total_seconds() of each elements.

    Args:
        time_deltas (ndarray of datetime.timedelta): array of timedeltas.

    Returns:
        ndaray of flot: the same array with all elements converted to total_seconds().

    Note:
        Adapted from `SO <https://stackoverflow.com/questions/19039080/elegant-way-of-convert-a-numpy-array-containing-datetime-timedelta-into-seconds>`__.
        Reply by prgao.
    """

    f = np.vectorize(lambda x: x.total_seconds())

    return f(time_deltas)

def nb_tie(data, resolution):
    """ Compute the number of data point considered to be equivalent (and to be treated as "ties").

    Args:
        data (ndarray of floats): the data array. Must be 1-D.
        resolution (float): delta value below which two measurements are considered equivalent.

    Return:
        ndarray of int: amount of ties in the data.

    Todo:
        * adjust docstring to better describe the function.
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
        return np.array([np.nan])
    # If there are less than 4 valid data point, return nan.
    if np.count_nonzero(~np.isnan(data)) <= 4:
        return np.array([np.nan])
    # If all the data is the same, just count it.
    if np.nanmin(data) == np.nanmax(data):
        return np.array([np.count_nonzero(~np.isnan(data))])

    # If there's nothing weird with the data, let's compute the bin edges.
    # Avoid the use of np.arange because of floating point errors, in favor of linspace
    #bins = np.arange(np.nanmin(data), np.nanmax(data)+resolution, resolution)
    nbins = int((np.nanmax(data)-np.nanmin(data))//resolution + 1)
    bins = np.linspace(np.nanmin(data), np.nanmin(data) + nbins * resolution, num=nbins + 1)
                       #dtype='float128') # Partial fix of #17, but does not work on all machines !

    # A sanity check
    if len(bins) < 2:
        raise Exception('Ouch! This error is impossible.')

    # Then compute the number of elements in each bin.
    return np.histogram(data, bins=bins)[0]


def kendall_var(data, t, n):
    """ Compute the variance with ties in the data and ties in time.

    Args:
        data (ndarray of floats): the data array. Must be 1-D.
        t (ndarray of int): number of elements in each tie. Must be 1-D.
        n (ndarray of int): number of non-missing data for each year. Must be 1-D.

    Return:
        float: the variance.

    Note:
        Source: Eq. 4.20, GAW report 133 (A. Sirois), p.30 of annex D.

    """

    # Some sanity checks first
    for item in [data, t, n]:
        if not isinstance(item, np.ndarray):
            raise Exception('Ouch ! Variables must be of type ndarray, not: %s' % (type(item)))
        if np.ndim(item) != 1:
            raise Exception('Ouch! Variables must be 1-D array.')

    # Length of the data ignoring the nans.
    l_real = np.count_nonzero(~np.isnan(data))

    var_s = (l_real*(l_real-1)*(2*l_real+5) - np.nansum(t*(t-1)*(2*t+5)) -
             np.nansum(n*(n-1)*(2*n+5))) / 18
    var_s += np.nansum(t*(t-1)*(t-2)) * np.nansum(n*(n-1)*(n-2)) / (9*l_real*(l_real-1)*(l_real-2))
    var_s += np.nansum(t*(t-1)) * np.nansum(n*(n-1)) / (2*l_real*(l_real-1))

    return var_s

def nanautocorr(obs, nlags, r=0):
    """ Compute the Pearson R autocoreelation coefficient for an array that contains nans.

    Also compute the confidence bounds b following Bartlett's formula.

    Args:
        obs (ndarray of float): the data array. Must be 1-D.
        nlags (int): number of lags to compute.
        r (int, optional): number of lags until the model is supposed to have a significant
                           autocorrelation coefficient. Must be < nlags. Defaults to 0.

    Returns:
        (ndarray, float): the autocorrelation coefficients, and the confidence bounds b.

    Note:
        Adapted from Fabio (2020), Autocorrelation and Partial Autocorrelation with NaNs,
        `<https://www.mathworks.com/matlabcentral/fileexchange/43840-autocorrelation-and-partial-autocorrelation-with-nans>`__,
        MATLAB Central File Exchange. Retrieved August 26, 2020.

    """

    # Some sanity checks

    # First, remove the mean of the data
    obs_corr = obs - np.nanmean(obs)
    out = []

    # Then, loop through the lags, and compute the perason r coefficient.
    for ind in range(1, nlags+1):
        obs_1 = obs_corr[ind:]
        obs_2 = obs_corr[:-ind]
        msk = ~np.isnan(obs_1) * ~np.isnan(obs_2)

        out += [spstats.pearsonr(obs_1[msk], obs_2[msk])[0]]

    # For consistency with matlab, let's also include the full auto-correlation
    msk = ~np.isnan(obs_corr)
    out = np.array([spstats.pearsonr(obs_corr[msk], obs_corr[msk])[0]] + out)

    # confidence bounds
    b = 1.96 * len(obs)**(-0.5) * np.nansum(out[:r+1]**2)**0.5

    return (out, b)

def levinson(r, n):
    """ Adapts the levinson() routine from matlab.

    Basically re-arranges the outputs from statsmodels.tsa.stattools.levinson_durbin() to match
    the matlab outputs. Includes a sign change and swapping a "1".

    For more info, see `<https://ch.mathworks.com/help/signal/ref/levinson.html?s_tid=srchtitle>`__.

    Todo:
        * fix this docstring

    """

    out = stattools.levinson_durbin(r, nlags=n, isacov=True)

    return (np.array([1] + list(-out[1])), out[0], -out[2][1:])
