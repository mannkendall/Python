# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains the different pre-whiteneing routines for the mannkendall package.
"""

# Import the required packages
import warnings
import numpy as np

from . import mk_tools as mkt

def nanprewhite_arok(obs):
    """ Compute the first lag autocorrelation coefficient to prewhite data as an AR(Kmax) function.

    Args:
        obs (ndarray of floats): the data array. Must be 1-D.

    Return:
        (float, float, int, ndarray, int): ak_lag, ak_std, k, data_prewhite, ak_ss

    Todo:
        * fix the docstring
        * clean-up the fonction

    """

    # Check the input. I shall be unforgiving.
    if not isinstance(obs, np.ndarray):
        raise Exception('Ouch ! data type should be numpy.ndarray, not: %s' % (type(obs)))

    # If I just received nan's: life is easy
    if np.all(np.isnan(obs)):
        return (np.nan, np.nan, np.nan, np.nan, np.nan, np.nan)

    # Deal with infinites if there are any
    obs[np.isinf(obs)] = np.nan

    # Number of valid points
    n_valid = np.count_nonzero(~np.isnan(obs))

    # Number of lags with a significant autocorrelation coefficient
    p_ind = 5

    # Number of lags to be computed
    nlag = 10

    # Restrict the number of computed lags and the number of the significant AC coefficients if the
    # time series is short.
    if nlag > len(obs)/2:
        nlag = len(obs)//2 # Keep nlag an integer.
    if p_ind >= nlag:
        p_ind = nlag - 1

    # Compute the autocorrelation
    (x, _) = mkt.nanautocorr(obs, nlag, p_ind)

    # Compute the confidence limits for the autocorrelation
    (_, _, ak_coefs) = mkt.levinson(x / n_valid, p_ind)
    ak_coefs *= -1
    # TODO: the following sqrt complains when the inside gets negative.
    # Should that really happen ?
    ak_std = np.sqrt((1-ak_coefs**2)/n_valid)
    uconf = 1.96/np.sqrt(n_valid)

    k_max = np.min([5, nlag])

    # Test the residue of the AR(Kmax)
    #res = np.zeros((len(obs), k_max)) * np.nan # Not used
    y = np.zeros((len(obs), k_max)) * np.nan

    aic2 = np.zeros(k_max) * np.nan
    bic2 = np.zeros(k_max) * np.nan
    se = np.zeros(k_max) * np.nan

    for ind in range(k_max):
        if ind == 0:
            y[1:, 0] = x[1] * obs[:-1]
            # following Wilks p.362
            se[0] = (1-x[1]**2) * np.nanvar(obs)
        else:
            y[ind+1:, ind] = y[ind+1:, ind-1] + x[ind+1] * obs[:-ind-1]
            # followin WIlks p.362
            se[ind] = (1-x[ind+1]**2) * se[ind-1] * ind

        aic2[ind] = n_valid * np.log(n_valid * se[ind]**2/(n_valid-ind)) + 2*(ind)
        bic2[ind] = n_valid * np.log(n_valid * se[ind]**2/(n_valid-ind)) + (ind+2)*np.log(n_valid)
        #res[ind:, ind] = obs[ind:] - y[ind:, ind] # Not used

    # TODO: aic2 and bic2 are still wrong
    # Need to debug this !!!


    # Autocorrelation degree
    k = np.max([np.argmin(aic2), np.argmin(bic2)])

    ak_lag = x[1]
    ak_std = ak_std[0]

    # Take only the correlation statistically significant at 95% confidence limit for the data
    if np.abs(ak_coefs[0]) < uconf:
        data_prewhite = obs
        ak_ss = 0
        # TODO: are we sure we want a formal warning here ? This is quite aggressive.
        # But I suppose it's an important thing to know ?
        warnings.warn('No statistically significant autocorrelation.')
    else:
        data_prewhite = obs - y[:, 0]
        ak_ss = 95

    return (ak_lag, ak_std, k, data_prewhite, ak_ss)
