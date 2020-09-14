# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains the core routines for the mannkendall package.
"""

# Import python packages
from pathlib import Path
import numpy as np
import scipy.stats as spstats

# Import from this package
from . import mk_hardcoded as mkh
from . import mk_tools as mkt
from . import mk_stats as mks
from . import mk_white as mkw


def compute_mk_stat(obs_dts, obs, resolution):
    """ Compute all the components for the MK statistics.

    Args:
        obs_dts (ndarray of datetime.datetime): a list of observation datetimes.
        obs (ndarray of floats): the data array. Must be 1-D.
        resolution (float): delta value below which two measurements are considered equivalent.

    Returns:
        (dict, int, float, float): result, s, vari, z

    """

    result = {}

    t = mkt.nb_tie(obs, resolution)
    (s, n) = mks.s_test(obs, obs_dts)
    vari = mkt.kendall_var(obs, t, n)
    z = mks.std_normal_var(s, vari)

    if len(obs) > 10:
        result['p'] = 2 * (1 - spstats.norm.cdf(np.abs(z), loc=0, scale=1))
    else:
        # TODO: do we really need this external file ?
        prob_mk_n = np.genfromtext(Path(__file__).parent / 'Prob_MK_n.csv')
        result['p'] = prob_mk_n[np.abs(s), len(obs)]

    # Determine the statistic significance
    if result['p'] <= 0.05:
        result['ss'] = 95
    elif 0.1 >= result['p'] > 0.05:
        result['ss'] = 90
    else:
        result['ss'] = 0

    (slope, slope_min, slope_max) = mks.sen_slope(obs_dts, obs, vari)
    result['ak'] = np.nan
    result['slope'] = slope * 3600 * 24 * 365.25  # Transform the slop in 1/yr. TODO: use precise year length ?
    result['ucl'] = slope_max * 3600 * 24 *365.25 # idem
    result['lcl'] = slope_min * 3600 * 24 * 365.25 # idem
    result['median'] = np.nanmedian(obs)
    result['slope_p'] = result['slope'] * 100/np.abs(result['median'])
    result['ucl_p'] = slope_max *3600 *24 *365.25 * 100/np.abs(result['median'])
    result['lcl_p'] = slope_min *3600 *24 *365.25 * 100/np.abs(result['median'])
    result['xhomo'] = np.nan

    return (result, s, vari, z)

# TODO: the following function is superseeded by mk_multi_tas()
#def mk_year(obs_dts, obs, resolution, pw_method = '3pw'):
    """Applies the Mann-Kendall test and the Sen slope on the given time granularity.

    Three pre-whitening methods are applied:
        *  PW (storch), and TFPW_Y (trend free PW, Yue et al, 2002) to compute the statistical
        significance, and
        * VCTFPW (W. Wang, Y. Chen, S. Becker & B. Liu, 2015) to compute the Sen's slope.

    Only the statistically significant autocorrelation are taken into account for the prewhitening.

    The statistically significance of the trends is taken at 95% confidence limit.

    The upper and lower confidence limits are given by the 90% of all the intervals differences
    distribution.

    The significance level is given by the Mann-Kendall test and has therefore no direct relation
    to the confidence limits.

    The resolution is taken into account to determine the number of ties in the data. It should
    typically be similar (or slightly larger) than the temporal resolution of the instrument. One
    should note, however, that this parameter isn't usually determinant for the results.

    Args:
        obs_dts (ndarray of datetime.datetime): a list of observation datetimes.
        obs (ndarray of floats): the data array. Must be 1-D.
        pw_method( str): must be one of ['3pw', 'pw', 'tfpw_y', 'tfpw_ws', 'vctfpw'].
                         Defaults to '3PW'.
        resolution (float): delta value below which two measurements are considered equivalent.

    Returns:
        dict: a dictionnary with the following entries:
                  * 'period':year or 12 months + year or 4 meteorological seasons + year
                  * 'ss': statistical significance, where:
                      - float>95: at least float>95 for both PW and TFPW_Y tests
                      - float>90: 90<float<95 for both PW and TFPW_Y tests
                      - -1: test is statistically significant for TFPW_Y, but not for PW (false positive)
                      - -2 or -3: test is statistically significant for PW, but not for TFPW_Y (false negative)
                      - 0: neither PW nor TFPW_Y are statistically significant
                  * 'slope': Sen's slope in units/yr
                  * 'ucl': upper confidence level in units/yr
                  * 'lcl': lower confidence level in untis/yr
                  * 'median': median of the data
                  * 'slope_p': Sen's slope in %/yr
                  * 'ucl_p': upper confidence limit in %/yr
                  * 'lcl_p': lower confidence limit in %/yr
                  * 'ak': first lag autocorrelation after detrending
                  * 'xhomo': homogeneity of the trend per seasons/month:
                      - 1: homogeneous at 90% confidence level
                      - 0: not homogenous the yearly slope should not be calculated
                      - np.nan: not assigned for yearly trend.

    Note:
        References:
            * W. Wang, Y. Chen, S. Becker & B. Liu, 2015, Variance Correction PreWhitening Method
              for trend Detection in Autocorrelated Data, J. Hydrol. Eng., 20 (12).
              `<https://doi.org/10.1061/(ASCE)HE.1943-5584.0001234>`__
            * WMO-GAW publication 133, annex E, p.26
            * explanantions of MULTMK/PARTMK from C.
    Todo:
        * fix this docstring.

    """
'''
    # Find the limiting years
    obs_years = np.array([item.year for item in obs_dts])
    min_year = np.min(obs_years)
    max_year = np.max(obs_years)

    # Compute the 3 prewhitened time series.
    (data_pw, ak_y) = mkw.prewhite(obs, obs_dts, resolution)

    result = {}

    # Compute the Mann-Kendall parameters for PW method
    if pw_method in ['pw', 'tfpw_y', 'tfpw_ws', 'vctfpw']:
        (result, _, _, _) = compute_mk_stat(obs_dts, data_pw[pw_method], resolution)
        result['ak'] = ak_y[pw_method]

    elif pw_method == '3pw':

        (result_pw, _, _, _) = compute_mk_stat(obs_dts, data_pw['pw'], resolution)
        (result_tfpw_y, _, _, _) = compute_mk_stat(obs_dts, data_pw['tfpw_y'], resolution)
        (result_vctfpw, _, _, _) = compute_mk_stat(obs_dts, data_pw['vctfpw'], resolution)
        result['ak'] = ak_y['vctfpw']

        # Determine the statistical significance
        if (result_pw['p'] <= 0.05) & (result_tfpw_y['p'] <= 0.05):
            # If both methods are above 95%, give the worst of both.
            result['ss'] = 100. * (1 - np.max([result_pw['p'], result_tfpw_y['p']]))
        elif (0.1 >= result_pw['p'] > 0.05) & (0.1 >= result_tfpw_y['p'] <= 0.05):
            # Idem, but if both methods are between 90% and 95%
            result['ss'] = 100. * (1 - np.max([result_pw['p'], result_tfpw_y['p']]))
        elif (result_pw['p'] > 0.05) & (result_tfpw_y['p'] <= 0.05):
            # False positive
            result['ss'] = -1
        elif (result_pw['p'] <= 0.05) & (result_tfpw_y['p'] > 0.05):
            # False negative
            result['ss'] = -2
        elif (result_pw['p'] <= 0.1) & (result_tfpw_y['p'] > 0.1):
            #TODO: we will actually never enter this place: we would get caught by the previous one!
            # False positive
            result['ss'] = -3
        else:
            result['ss'] = 0

        # Let's assign the rem,aining variables
        for item in ['slope', 'ucl', 'lcl', 'median', 'slope_p', 'ucl_p', 'lcl_p', 'xhomo']:
            result[item] = result_vctfpw[item]
    else:
        raise Exception('Ouch ! Unknowkn pw_method: %s' % (pw_method))

    return result
'''

def mk_multi_tas(multi_obs_dts, multi_obs, resolution, pw_method='3pw'):
    """ Applies the Mann-Kendall test and the Sen slope on the given time granularity for a data set
    split into different temporal aggregations.

    Args:
        multi_obs_dts (list of 1-D ndarray of datetime.datime):
        multi_obs (list of 1-D ndarray)
        resolution (float)
        pw_method

    Returns:
        dict

    Todo:
        * Drastically improve this docstring, to be as good as the former mk_year().

    """

    # Some sanity checks first
    if pw_method not in mkh.VALID_PW_METHODS:
        raise Exception('Ouch ! pw_method unknown.')

    # TODO: merge this into a sub-function ?
    if not isinstance(multi_obs_dts, list):
        # If I received a 1-D array, be nice and deal with it.
        if isinstance(multi_obs_dts, np.ndarray):
            multi_obs_dts = [multi_obs_dts]
        else:
            raise Exception('Ouch ! Unsupported type: %s' % (type(multi_obs_dts)))

    if not isinstance(multi_obs, list):
        # If I received a 1-D array, be nice and deal with it.
        if isinstance(multi_obs, np.ndarray):
            multi_obs = [multi_obs]
        else:
            raise Exception('Ouch ! Unsupported type: %s' % (type(multi_obs)))

    if len(multi_obs_dts) != len(multi_obs):
        raise Exception('Ouch ! multi_obs_dts and multi_obs should have the same length !')

    if np.any([np.ndim(item) != 1 for item in multi_obs_dts]):
        raise Exception('Ouch ! I was expecting 1-D arrays inside multi_obs_dts.')
    if np.any([np.ndim(item) != 1 for item in multi_obs]):
        raise Exception('Ouch ! I was expecting 1-D arrays inside multi_obs.')

    if np.any([len(item) != len(multi_obs[ind]) for (ind, item) in enumerate(multi_obs_dts)]):
        raise Exception('Ouch ! Inconsistent length between obs and obs_dts arrays.')

    # How many different time aggregates do we have ?
    n_tas = len(multi_obs_dts)
    # What is the length of each time aggregate ?
    len_tas = [len(item) for item in multi_obs]

    # First, apply the necessary prewhitening to *all* the data combined.
    # To do that, I need to put the data in order !
    sort_ind = np.concatenate(multi_obs_dts).argsort()
    (multi_obs_pw, ak_y) = mkw.prewhite(np.concatenate(multi_obs)[sort_ind],
                                        np.concatenate(multi_obs_dts)[sort_ind],
                                        resolution)

    # Re-split the data according to the original input ... including
    for key in multi_obs_pw:
        # De-sort the output array
        desorted = mkt.de_sort(multi_obs_pw[key], sort_ind)
        # De-concatenate it.
        multi_obs_pw[key] = list(np.split(desorted, np.array([np.sum(len_tas[:ind+1])
                                                              for ind in range(n_tas-1)])))

    # Create some useful variables
    s_tot = {'-': 0.0, 'pw': 0.0, 'tfpw_y': 0.0}
    var_tot = {'-': 0.0, 'pw': 0.0, 'tfpw_y': 0.0}

    # Storage space for the final results
    result = {}
    z = np.zeros(n_tas) * np.nan

    # Start looping through the different periods
    for ta_ind in range(n_tas):

        result[ta_ind] = {}

        # First, let's make sure there are enough data in the period.
        if len(multi_obs[ta_ind]) <= 1:
            result[ta_ind] = {'p': np.nan, 'ss': np.nan, 'slope': np.nan, 'ucl': np.nan,
                              'lcl': np.nan, 'median': np.nan, 'slope_p': np.nan, 'ucl_p': np.nan,
                              'lcl_p': np.nan}
            continue

        # Now, run whichever method was requested
        # Compute the Mann-Kendall parameters for PW method
        if pw_method in ['pw', 'tfpw_y', 'tfpw_ws', 'vctfpw']:
            (result[ta_ind], s, vari, z[ta_ind]) = compute_mk_stat(multi_obs_dts[ta_ind],
                                                                   multi_obs_pw[pw_method][ta_ind],
                                                                   resolution)
            s_tot['-'] += s
            var_tot['-'] += vari
            ak = ak_y[pw_method]

        elif pw_method == '3pw':

            (result_pw, s_pw, vari_pw, _) = compute_mk_stat(multi_obs_dts[ta_ind],
                                                            multi_obs_pw['pw'][ta_ind], resolution)
            s_tot['pw'] += s_pw
            var_tot['pw'] += vari_pw

            (result_tfpw_y, s_tfpw_y, vari_tfpw_y, _) = \
                compute_mk_stat(multi_obs_dts[ta_ind], multi_obs_pw['tfpw_y'][ta_ind], resolution)
            s_tot['tfpw_y'] += s_tfpw_y
            var_tot['tfpw_y'] += vari_tfpw_y

            (result_vctfpw, _, _, z[ta_ind]) = compute_mk_stat(multi_obs_dts[ta_ind],
                                                               multi_obs_pw['vctfpw'][ta_ind],
                                                               resolution)

            # Determine the statistical significance
            if (result_pw['p'] <= 0.05) & (result_tfpw_y['p'] <= 0.05):
                # If both methods are above 95%, give the worst of both.
                result[ta_ind]['ss'] = 100. * (1 - np.max([result_pw['p'], result_tfpw_y['p']]))
            elif (0.1 >= result_pw['p'] > 0.05) & (0.1 >= result_tfpw_y['p'] <= 0.05):
                # Idem, but if both methods are between 90% and 95%
                result[ta_ind]['ss'] = 100. * (1 - np.max([result_pw['p'], result_tfpw_y['p']]))
            elif (result_pw['p'] > 0.05) & (result_tfpw_y['p'] <= 0.05):
                # False positive
                result[ta_ind]['ss'] = -1
            elif (result_pw['p'] <= 0.05) & (result_tfpw_y['p'] > 0.05):
                # False negative
                result[ta_ind]['ss'] = -2
            elif (result_pw['p'] <= 0.1) & (result_tfpw_y['p'] > 0.1):
                #TODO: we will actually never enter this place: we would get caught by the previous one!
                # False positive
                result[ta_ind]['ss'] = -3
            else:
                result[ta_ind]['ss'] = 0

            # Let's assign the remaining variables
            for item in ['slope', 'ucl', 'lcl', 'median', 'slope_p', 'ucl_p', 'lcl_p']:
                result[ta_ind][item] = result_vctfpw[item]

            ak = ak_y['vctfpw']

        else:
            raise Exception('Ouch ! Unknowkn pw_method: %s' % (pw_method))


    # Now let's look at the sum of all the time aggregations.
    # TODO: simplify (by function grouping) the following two if clauses
    result[n_tas] = {}
    result[n_tas]['ak'] = ak

    if pw_method != '3pw':

        z_tot = mks.std_normal_var(s_tot['-'], var_tot['-'])

        if np.sum([len(item) for item in multi_obs]) > 10: # TODO: count all values, including nans?
            result[n_tas]['p'] = 2 * (1 - spstats.norm.cdf(np.abs(z_tot), loc=0, scale=1))
        else:
            # TODO: do we really need this external file ?
            prob_mk_n = np.genfromtext(Path(__file__).parent / 'Prob_MK_n.csv')
            result[n_tas]['p'] = prob_mk_n[np.abs(s_tot['-']),
                                           np.sum([len(item) for item in multi_obs])] # TODO: check this !

        # Compute the statistical significance
        if result[n_tas]['p'] <= 0.1:
            result[n_tas]['ss'] = 100 * (1.-result[n_tas]['p'])
        else:
            result[n_tas]['ss'] = 0

        # Compute the median
        result[n_tas]['median'] = np.nanmedian(np.concatenate(multi_obs))

        # Compute the chi-square to test the homogeneity between months
        xhomo = np.nansum(z**2) - n_tas *np.nanmean(z)**2 # TODO: check ok with matlab code.

        if xhomo <= 4.575:
            result[n_tas]['xhomo'] = 1
        else:
            result[n_tas]['xhomo'] = 0

    if pw_method == '3pw':

        z_tot_pw = mks.std_normal_var(s_tot['pw'], var_tot['pw'])


        if np.sum([np.count_nonzero(~np.isnan(item)) for item in multi_obs]) > 10:
            p_tot_pw = 2 * (1 - spstats.norm.cdf(np.abs(z_tot_pw), loc=0, scale=1))
        else:
            # TODO: do we really need this external file ?
            prob_mk_n = np.genfromtext(Path(__file__).parent / 'Prob_MK_n.csv')
            p_tot_pw = prob_mk_n[np.abs(s_tot['pw']),
                                 np.sum([np.count_nonzero(~np.isnan(item)) for item in multi_obs])] # TODO: check this !

        z_tot_tfpw_y = mks.std_normal_var(s_tot['tfpw_y'], var_tot['tfpw_y'])

        # TODO: check this with the new matlab code.
        if np.sum([np.count_nonzero(~np.isnan(item)) for item in multi_obs]) > 10:
            p_tot_tfpw_y = 2 * (1 - spstats.norm.cdf(np.abs(z_tot_pw), loc=0, scale=1))
        else:
            # TODO: do we really need this external file ?
            prob_mk_n = np.genfromtext(Path(__file__).parent / 'Prob_MK_n.csv')
            p_tot_tfpw_y = prob_mk_n[np.abs(s_tot['tfpw_y']),
                                     np.sum([np.count_nonzero(~np.isnan(item))
                                             for item in multi_obs])] # TODO: check this !

        # Determine the statistical significance
        if (p_tot_pw <= 0.05) & (p_tot_tfpw_y <= 0.05):
            # If both methods are above 95%, give the worst of both.
            result[n_tas]['ss'] = 100. * (1 - np.max([p_tot_pw, p_tot_tfpw_y]))
        elif (0.1 >= p_tot_pw > 0.05) & (0.1 >= result_tfpw_y['p'] <= 0.05):
            # Idem, but if both methods are between 90% and 95%
            result[n_tas]['ss'] = 100. * (1 - np.max([p_tot_pw, p_tot_tfpw_y]))
        elif (p_tot_pw > 0.05) & (p_tot_tfpw_y <= 0.05):
            # False positive
            result[n_tas]['ss'] = -1
        elif (p_tot_pw <= 0.05) & (p_tot_tfpw_y > 0.05):
            # False negative
            result[n_tas]['ss'] = -2
        elif (p_tot_pw <= 0.1) & (p_tot_tfpw_y > 0.1):
            #TODO: we will actually never enter this place: we would get caught by the previous one!
            # False positive
            result[n_tas]['ss'] = -3
        else:
            result[n_tas]['ss'] = 0

        # Compute the chi-squre to test the homogeneity between time aggregations. Since the slop is
        # computed from VCTFPW, the homogeneity is also computed from VCTFPW.
        xhomo = np.nansum(z**2)-n_tas*np.nansum(z)**2
        if xhomo <= 4.575:
            result[n_tas]['xhomo'] = 1
        else:
            result[n_tas]['xhomo'] = 0

    # Write the yearly slope and CL
    for item in ['slope', 'ucl', 'lcl']:
        result[n_tas][item] = np.nanmedian([result[key][item] for key in result if key != n_tas])

    result[n_tas]['median'] = np.nanmedian(np.concatenate(multi_obs_pw['vctfpw']))
    result[n_tas]['slope_p'] = result[n_tas]['slope'] * 100./ np.abs(result[n_tas]['median'])
    result[n_tas]['ucl_p'] = result[n_tas]['ucl'] * 100./ np.abs(result[n_tas]['median'])
    result[n_tas]['lcl_p'] = result[n_tas]['lcl'] * 100./ np.abs(result[n_tas]['median'])

    return result
