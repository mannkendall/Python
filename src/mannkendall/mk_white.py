# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors of the original matlab version of the code listed in
ORIGINAL_AUTHORS.
Copyright (c) 2020 MeteoSwiss, contributors of the Python version of the code listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains the different pre-whiteneing routines for the mannkendall package.
"""

# Import the required packages
import warnings
import copy
import numpy as np
from scipy.stats import norm

from . import mk_tools as mkt
from . import mk_stats as mks

def nanprewhite_arok(obs, alpha_ak=95):
    """ Compute the first lag autocorrelation coefficient to prewhite data as an AR(Kmax) function.

    Args:
        obs (ndarray of floats): the data array. Must be 1-D.
        alpha_ak (float): confidence level for the first lag autocorrelation in %. Defaults to 95.

    Return:
        (float, ndarray, int): ak_lag, data_prewhite, ak_ss.
                               ak_lag (float): first lag autocorrelation coefficient.
                               data_prewhite (ndarray): data after removing of the first lag
                               autorcorrelation if ak_lag is ss, original data otherwise.
                               ak_ss (int): statistical significance of the first lag
                               autocorrelation. alpha_ak is ss at the alpha_ak level, zero otherwise

    Todo:
        * fix the docstring

    """

    # Check the input. I shall be unforgiving.
    if not isinstance(obs, np.ndarray):
        raise Exception('Ouch ! data type should be numpy.ndarray, not: %s' % (type(obs)))
    if not isinstance(alpha_ak, (int, float)):
        raise Exception('Ouch ! alpha_ak should be of type float, not: %s' % (type(alpha_ak)))
    if alpha_ak > 100 or alpha_ak < 0:
        raise Exception('Ouch ! I need 0 <= alpha+ak <= 100, not: %.2f' % (alpha_ak))

    # If I just received nan's: life is easy
    if np.all(np.isnan(obs)):
        # Note: should we return False instead ?
        return (np.nan, np.zeros(len(obs))*np.nan, np.nan)

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
    # Note: mkt.levinson() include a -1 to match the matlab output ... I should probably get rid of
    # it in there, rather than here.
    ak_coefs *= -1
    uconf = norm.ppf(1-(1-alpha_ak/100)/2)/np.sqrt(n_valid)

    ak_lag = x[1]
    # ak_std = ak_std[0]

    # Take only the correlation statistically significant at 95% confidence limit for the data
    if np.abs(ak_coefs[0]) < uconf:
        data_prewhite = obs
        ak_ss = 0
        # Note: are we sure we want a formal warning here ? This is quite aggressive.
        # But I suppose it's an important thing to know ?
        warnings.warn('No statistically significant autocorrelation.')
    else:
        y = np.zeros(len(obs)) * np.nan
        y[1:] = x[1] * obs[:-1]
        data_prewhite = obs - y[:]
        ak_ss = alpha_ak

    return (ak_lag, data_prewhite, ak_ss)


def prewhite(obs, obs_dts, resolution, alpha_ak=95):
    """ Compute the necessary prewhitened datasets to assess the statistical significance, and to
    compute the Sen slope for each of the prewhitening method, including 3PW.

    Args:
        obs (ndarray of floats): the data array. Must be 1-D.
        obs_dts (ndarray of datetime.datetime): a list of observation datetimes.
        resolution (float): delta value below which two measurements are considered equivalent.
                            It is used to compute the number of ties.
        alpha_ak (float, optional): statistical significance in % for the first lag autocorrelation.
                                    Defaults to 95.

    Returns:
        (dict): data_pw, that contains 5 PW timeseries:
                * 'pw': PW with the first lag autocorrelation of the data
                * 'pw_cor': PW corrected with 1/(1-ak1)
                * 'tfpw_ws': PW with the first lag autocorrelation of the data after detrending
                             computed from PW data (see Wang & Swail)
                * 'tfpw_y': method of Yue et al 2002, not 1/1-ak1) correction, detrend on original
                            data
                * 'vctfpw': PW with the first lag autocorrelation of the data after detrending +
                            correction of the PW data for the variance (see Wang 2015)

    Todo:
        * fix this docstring

    """

    # Some sanity checks to start with
    if not isinstance(alpha_ak, (int, float)):
        raise Exception('Ouch ! alpha_ak must be of type float, not: %s' % (type(alpha_ak)))
    if alpha_ak > 100 or alpha_ak < 0:
        raise Exception('Ouch ! Confidence limits should be 0 < alpha_ak < 100, not: %.2f' %
                        (alpha_ak))

    # Create some storage dictionnaries
    data_pw = {}
    c_dict = {}

    # Deal with infinites if there are any
    obs[np.isinf(obs)] = np.nan

    # Compute the autocorrelation
    (c_dict['pw'], data_ar_removed, c_dict['ss']) = nanprewhite_arok(obs, alpha_ak=alpha_ak)

    # no statistically significant correlation ? Then get out now.
    if not((np.count_nonzero(~np.isnan(data_ar_removed)) > 0) & (c_dict['ss'] == alpha_ak) &
           (c_dict['pw'] >= 0.05)):

        data_pw['pw'] = copy.copy(obs)
        data_pw['pw_cor'] = copy.copy(obs)
        data_pw['tfpw_y'] = copy.copy(obs)
        data_pw['tfpw_ws'] = copy.copy(obs)
        data_pw['vctfpw'] = copy.copy(obs)

        return data_pw

    # Else, compute the obs PW corrected
    data_pw['pw'] = copy.copy(data_ar_removed)
    data_pw['pw_cor'] = data_ar_removed/(1-c_dict['pw'])

    # data VCTFPW corrected
    # compute the trend slope of the PW data
    t = mkt.nb_tie(data_pw['pw_cor'], resolution)
    (_, n) = mks.s_test(data_pw['pw_cor'], obs_dts)
    vari = mkt.kendall_var(obs, t, n)
    (b0_pw, _, _) = mks.sen_slope(obs_dts, data_pw['pw_cor'], vari) # slope of the original data

    t = mkt.nb_tie(obs, resolution)
    (_, n) = mks.s_test(obs, obs_dts)
    vari = mkt.kendall_var(obs, t, n)
    (b0_or, _, _) = mks.sen_slope(obs_dts, obs, vari)

    # Remove the trend
    data_detrend_pw = obs - b0_pw * mkt.dt_to_s(obs_dts-obs_dts[0])
    data_detrend_or = obs - b0_or * mkt.dt_to_s(obs_dts-obs_dts[0])

    # Compute the autocorrelation of the detrended time series
    (c_dict['vctfpw'], data_ar_removed_or, c_dict['ss_vc']) = \
                                        nanprewhite_arok(data_detrend_or, alpha_ak=alpha_ak)
    c_dict['tfpw_y'] = copy.copy(c_dict['vctfpw'])
    (ak_pw, data_ar_removed_pw, ss_pw) = nanprewhite_arok(data_detrend_pw, alpha_ak=alpha_ak)

    # Compute TFPW correction following Yue et al., 2002
    # blended data
    if np.count_nonzero(~np.isnan(data_ar_removed_or)) > 0:
        data_pw['tfpw_y'] = data_ar_removed_or + b0_or * mkt.dt_to_s(obs_dts - obs_dts[0])
    else:
        data_pw['tfpw_y'] = copy.copy(obs)

    # Compute the TFPW correction of Wang and Sail
    if (np.abs(ak_pw) >= 0.05) & (ss_pw == 95):
        # Change so that while can be used with the same variable:
        # ak is new c and c1 is the last c
        c_1 = copy.copy(c_dict['pw'])

        data_ar_removed_pw = copy.copy(obs)
        data_ar_removed_pw[1:] -= ak_pw * obs[:-1]
        data_ar_removed_pw[1:] /= (1-ak_pw)

        t = mkt.nb_tie(data_ar_removed_pw, resolution)
        (_, n) = mks.s_test(data_ar_removed_pw, obs_dts)
        vari = mkt.kendall_var(data_ar_removed_pw, t, n)
        (b1_pw, _, _) = mks.sen_slope(obs_dts, data_ar_removed_pw, vari)

        # Remove the trend
        nb_loop = 0

        # Remember that b0_pw and b1_pw are in 1/s.
        while (np.abs(ak_pw-c_1) > 1e-4) & (np.abs(b1_pw-b0_pw) > (1e-4/24/3600)):

            if (ak_pw >= 0.05) & (ss_pw == 95):

                nb_loop += 1
                data_detrend_pw = obs - b1_pw * mkt.dt_to_s(obs_dts-obs_dts[0])
                c_1 = copy.copy(ak_pw)
                b0_pw = copy.copy(b1_pw)
                (ak_pw, data_ar_removed2_pw, ss_pw) = \
                                            nanprewhite_arok(data_detrend_pw, alpha_ak=alpha_ak)

                if (ak_pw > 0) & (ss_pw == 95):

                    data_ar_removed2_pw = copy.copy(obs)
                    data_ar_removed2_pw[1:] -= ak_pw * obs[:-1]
                    data_ar_removed2_pw[1:] /= (1-ak_pw)

                    t = mkt.nb_tie(data_ar_removed2_pw, resolution)
                    (_, n) = mks.s_test(data_ar_removed2_pw, obs_dts)
                    vari = mkt.kendall_var(data_ar_removed2_pw, t, n)
                    (b1_pw, _, _) = mks.sen_slope(obs_dts, data_ar_removed2_pw, vari)
                    data_ar_removed_pw = copy.copy(data_ar_removed2_pw)

                    if nb_loop > 10:
                        break
            else:
                break
    else:
        b1_pw = copy.copy(b0_pw)
        ak_pw = copy.copy(c_dict['pw'])

    # blended data
    if np.count_nonzero(~np.isnan(data_ar_removed_pw)) > 0:
        data_pw['tfpw_ws'] = copy.copy(data_ar_removed_pw)
        c_dict['tfpw_ws'] = copy.copy(ak_pw)
    else:
        data_pw['tfpw_ws'] = copy.copy(obs)
        # Note:
        # not setting c['tfpw_ws'] here will create a case-dependant mismatch in the output

    # Correction VCTFPW
    # Correction of the variance
    var_data = np.nanvar(obs, ddof=1) # ddof=1 to be like nanvar from matlab
    var_data_tfpw = np.nanvar(data_ar_removed_or, ddof=1) # ddof=1 to be like nanvar from matlab
    data_ar_removed_var = data_ar_removed_or * var_data/var_data_tfpw

    # Modify the slope estimator
    # (correction of the slope for the autocorrelation)
    if c_dict['vctfpw'] >= 0:
        b_vc = b0_or / np.sqrt((1+c_dict['vctfpw'])/(1-c_dict['vctfpw']))
    else:
        b_vc = copy.copy(b0_or)

    # Add the trend again
    data_pw['vctfpw'] = data_ar_removed_var + b_vc * mkt.dt_to_s(obs_dts-obs_dts[0])

    return data_pw
