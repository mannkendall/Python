# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors of the original matlab version of the code listed in
ORIGINAL_AUTHORS.
Copyright (c) 2020 MeteoSwiss, contributors of the Python version of the code listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains the core routines for the mannkendall package.
"""

# Import python packages
import warnings
import numpy as np
import scipy.stats as spstats

# Import from this package
from . import mk_hardcoded as mkh
from . import mk_tools as mkt
from . import mk_stats as mks
from . import mk_white as mkw


def prob_3pw(p_pw, p_tfpw_y, alpha_mk):
    """ Estimate the probability of the MK test and its statistical significance.

        1) Estimates the probability of the MK test with the 3PW method. To have the maximal
           certainty, P is taken as the maximum of P_PW and P_TFPW_Y.
        2) Estimates the statistical significance of the MK test as a function of the given
           confidence level alpha_MK.

    Args:
        p_pw (float): probability computed from the PW prewhitened dataset
        p_tfpw_y (float): probability computed from the TFPW_Y prewhitened dataset
        alpha_mk (float): confidence level in % for the MK test.

    Returns:
        (float, int): P, ss

    Todo:
        * improve this docstring

    """

    # Some sanity checks to begin with
    for item in [p_pw, p_tfpw_y, alpha_mk]:
        if not isinstance(item, (int, float)):
            raise Exception('Ouch ! I was expecting a float, not: %s' % (type(item)))

    p_alpha = 1 - alpha_mk/100

    # Compute the probability
    p = np.nanmax([p_pw, p_tfpw_y])

    # Determine the statistical significance
    if (p_pw <= p_alpha) & (p_tfpw_y <= p_alpha):
        ss = alpha_mk
    elif (p_pw > p_alpha) & (p_tfpw_y <= p_alpha): # false positive for TFPW_Y @ alpha %
        ss = -1
    elif (p_tfpw_y > p_alpha) & (p_pw <= p_alpha): # false positive for TFPW_Y
        ss = -2
    elif (p_tfpw_y > p_alpha) & (p_pw > p_alpha): # false positive for PW
        ss = 0

    return (p, ss)


def compute_mk_stat(obs_dts, obs, resolution, alpha_mk=95, alpha_cl=90):
    """ Compute all the components for the MK statistics.

    Args:
        obs_dts (ndarray of datetime.datetime): a list of observation datetimes.
        obs (ndarray of floats): the data array. Must be 1-D.
        resolution (float): delta value below which two measurements are considered equivalent.
        alpha_mk (float, optional): confidence level for the Mann-Kendall test in %. Defaults to 95.
        alpha_cl (float, optional): confidence level for the Sen's slope in %. Defaults to 90.

    Returns:
        (dict, int, float, float): result, s, vari, z

    """

    # Some sanity checks
    for item in [alpha_mk, alpha_cl]:
        if not isinstance(item, (int, float)):
            raise Exception('Ouch! alphas must be of type float, not: %s' %(type(item)))
    if alpha_mk < 0 or alpha_mk > 100 or alpha_cl < 0 or alpha_cl > 100:
        raise Exception("Ouch ! Confidence limits must be 0 <= CL <= 100.")

    result = {}

    t = mkt.nb_tie(obs, resolution)
    (s, n) = mks.s_test(obs, obs_dts)
    vari = mkt.kendall_var(obs, t, n)
    z = mks.std_normal_var(s, vari)

    if len(obs) > 10:
        result['p'] = 2 * (1 - spstats.norm.cdf(np.abs(z), loc=0, scale=1))
    else:
        prob_mk_n = mkh.PROB_MK_N
        result['p'] = prob_mk_n[np.abs(s), len(obs)] # TODO: np.abs(s) + 1 ?

    # Determine the statistic significance
    if result['p'] <= 1- alpha_mk/100:
        result['ss'] = alpha_mk
    else:
        result['ss'] = 0

    (slope, slope_min, slope_max) = mks.sen_slope(obs_dts, obs, vari, alpha_cl=alpha_cl)
    # Transform the slop in 1/yr.
    result['slope'] = slope * 3600 * 24 * 365.25
    result['ucl'] = slope_max * 3600 * 24 *365.25
    result['lcl'] = slope_min * 3600 * 24 * 365.25

    return (result, s, vari, z)

def mk_temp_aggr(multi_obs_dts, multi_obs, resolution, pw_method='3pw',
                 alpha_mk=95, alpha_cl=90, alpha_xhomo=90, alpha_ak=95):
    """ Applies the Mann-Kendall test and the Sen slope on the given time granularity for a data set
    split into different temporal aggregations.

    Five prewhitening methods can be chosen:

        * 3PW (Collaud Coen et al., 2020): 3 prewhitening methods are applied (PW and TFPW_Y to
          determine the statistic significance (ss) of the MK test and the VCTFPW method to compute
          the Sen's slope.
        * PW (prewhitened, Kulkarni and von Storch, 1995)
        * TFPW_Y(trend free PW,Yue et al., 2001)
        * TFPW_WS (trend free PW, Wang and Swail, 2001)
        * VCTFPW (variance corrected trend free PW, Wang et al., 2015)

    For the PW,only ss autocorrelation are taken into account.
    The default ss for the MK test is taken at 95% confidence limit.
    The default ss for upper and lower confidence limits is 90% of the all intervals differences
    distribution.

    The default ss for the autocorrelation coefficient is 95%.
    The default ss for the homogeneity test between temporal aggregation of the MK test is 90%.
    If seasonal Mann-Kendall is applied, the yearly trend is assigned only if the results of the
    seasonal test are homogeneous. The default ss for the homogeneity test between temporal
    aggregation of the seasonal MK test is 90%.


    Args:
        multi_obs_dts (list of 1-D ndarray of datetime.datime): the observation times. Each array
                                                                defines a new season.
        multi_obs (list of 1-D ndarray): the observations. Each array defines a new season.
        resolution (float): interval to determine the number of ties. It should be similar to the
                            resolution of the instrument.
        pw_method (str): must be one of ['3pw', 'pw, 'tfpw_y', 'tfpw_ws', 'vctfpw'].
                         Defaults to '3pw'.
        alpha_mk (float, optional): confidence limit for Mk test in %. Defaults to 95.
        alpha_cl (float, optional): confidence limit for the Sen's slope in %. Defaults to 90.
        alpha_xhomo (float, optional): confidence limit for the homogeneity between seasons in %.
                                       Defaults to 90.
        alpha_ak (float, optional): confidence limit for the first lag autocorrelation in %.
                                    Defaults to 95.

    Returns:
        dict: comprises the following fields

            * 'p' (float): probability for the statistical significance. If 3PW is applied,
              P= max(P_PW, P_TFPW_Y);
            * 'ss' (float): statistical significance:

                - alpha_MK if the test is ss at the alpha confidence level. Defaults to 95.
                - 0 if the test is not ss at the alpha_MK confidence level.
                - -1 if the test is a TFPW_Y false positive at alpha_MK confidence level
                - -2 if the test is a PW false positive at alpha_MK confidence level
            * 'slope' (float): Sen's slope in units/y
            * 'ucl' (float): upper confidence level in units/y
            * 'lcl' (float): lower confidence level in units/y

    Note:
        Sources

            * Collaud Coen et al., Effects of the prewhitening method, the time granularity and the
              time segmentation on the Mann-Kendall trend detection and the associated Sen's slope,
              Atmos. Meas. Tech. Discuss, https://doi.org/10.5194/amt-2020-178, 2020.
            * Sirois, A.: A brief and biased overview of time-series analysis of how to find that
              evasive trend, WMO/EMEP Workshop on Advanced Statistical Methods and Their Application
              to Air Quality Data Sets, Annex E., Global Atmosphere Watch No. 133, TD- No. 956,
              World Meteorological Organization, Geneva, Switzerland, 1998. annexe E, p. 26.
            * Gilbert, R.: Statistical Methods for Environmental Pollution Monitoring, Van Nostrand
              Reinhold Company, New York, 1987.
            * The explanations about MULTMK/PARTMK de C. Libiseller.

    """

    # Some sanity checks first
    if pw_method not in mkh.VALID_PW_METHODS:
        raise Exception('Ouch ! pw_method unknown.')

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

    for item in [alpha_mk, alpha_cl, alpha_xhomo, alpha_ak]:
        if not isinstance(item, (int, float)):
            raise Exception('Ouch ! alpha should be of type float, not: %s' % (type(item)))
        if (item > 100) or (item < 0):
            raise Exception('Ouch ! I need 0 < alpha < 100, not:' % (item))

    # How many different time aggregates do we have ?
    n_tas = len(multi_obs_dts)
    # What is the length of each time aggregate ?
    len_tas = [len(item) for item in multi_obs]

    # First, apply the necessary prewhitening to *all* the data combined.
    # To do that, I need to put the data in order !
    sort_ind = np.concatenate(multi_obs_dts).argsort()
    multi_obs_pw = mkw.prewhite(np.concatenate(multi_obs)[sort_ind],
                                np.concatenate(multi_obs_dts)[sort_ind],
                                resolution, alpha_ak=alpha_ak)

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
                              'lcl': np.nan}
            continue

        # Now, run whichever method was requested
        # Compute the Mann-Kendall parameters for PW method
        if pw_method in ['pw', 'tfpw_y', 'tfpw_ws', 'vctfpw']:
            (result[ta_ind], s, vari, z[ta_ind]) = compute_mk_stat(multi_obs_dts[ta_ind],
                                                                   multi_obs_pw[pw_method][ta_ind],
                                                                   resolution, alpha_mk=alpha_mk,
                                                                   alpha_cl=alpha_cl)
            s_tot['-'] += s
            var_tot['-'] += vari
            #ak = ak_y[pw_method]

        elif pw_method == '3pw':

            (result_pw, s_pw, vari_pw, _) = compute_mk_stat(multi_obs_dts[ta_ind],
                                                            multi_obs_pw['pw'][ta_ind], resolution,
                                                            alpha_mk=alpha_mk, alpha_cl=alpha_cl)
            s_tot['pw'] += s_pw
            var_tot['pw'] += vari_pw

            (result_tfpw_y, s_tfpw_y, vari_tfpw_y, _) = \
                compute_mk_stat(multi_obs_dts[ta_ind], multi_obs_pw['tfpw_y'][ta_ind], resolution,
                                alpha_mk=alpha_mk, alpha_cl=alpha_cl)
            s_tot['tfpw_y'] += s_tfpw_y
            var_tot['tfpw_y'] += vari_tfpw_y

            (result_vctfpw, _, _, z[ta_ind]) = compute_mk_stat(multi_obs_dts[ta_ind],
                                                               multi_obs_pw['vctfpw'][ta_ind],
                                                               resolution, alpha_mk=alpha_mk,
                                                               alpha_cl=alpha_cl)

            # Determine the statistical significance
            (result[ta_ind]['p'], result[ta_ind]['ss']) = prob_3pw(result_pw['p'],
                                                                   result_tfpw_y['p'],
                                                                   alpha_mk)

            # Let's assign the remaining variables
            for item in ['slope', 'ucl', 'lcl']:
                result[ta_ind][item] = result_vctfpw[item]

        else:
            raise Exception('Ouch ! Unknowkn pw_method: %s' % (pw_method))


    # Now let's look at the sum of all the time aggregations.
    result[n_tas] = {}
    #result[n_tas]['ak'] = ak

    if pw_method != '3pw':

        z_tot = mks.std_normal_var(s_tot['-'], var_tot['-'])

        if np.sum([np.count_nonzero(~np.isnan(item)) for item in multi_obs]) > 10:
            result[n_tas]['p'] = 2 * (1 - spstats.norm.cdf(np.abs(z_tot), loc=0, scale=1))
        else:
            # TODO: check this !
            result[n_tas]['p'] = mkh.PROB_MK_N[np.nansum(np.abs(s_tot['-'])),
                                               np.sum([np.count_nonzero(~np.isnan(item)) for item
                                                       in multi_obs])]

        # Compute the statistical significance
        if result[n_tas]['p'] <= 1-alpha_mk/100:
            result[n_tas]['ss'] = alpha_mk
        else:
            result[n_tas]['ss'] = 0

        # Compute the chi-square to test the homogeneity between months
        xhomo = np.nansum(z**2) - n_tas * np.nanmean(z)**2

    if pw_method == '3pw':

        z_tot_pw = mks.std_normal_var(s_tot['pw'], var_tot['pw'])

        if np.sum([np.count_nonzero(~np.isnan(item)) for item in multi_obs]) > 10:
            p_tot_pw = 2 * (1 - spstats.norm.cdf(np.abs(z_tot_pw), loc=0, scale=1))
        else:
            p_tot_pw = mkh.PROB_MK_N[np.nansum(np.abs(s_tot['pw'])),
                                     np.sum([np.count_nonzero(~np.isnan(item)) for item
                                             in multi_obs])] # TODO: check this !

        z_tot_tfpw_y = mks.std_normal_var(s_tot['tfpw_y'], var_tot['tfpw_y'])

        if np.sum([np.count_nonzero(~np.isnan(item)) for item in multi_obs]) > 10:
            p_tot_tfpw_y = 2 * (1 - spstats.norm.cdf(np.abs(z_tot_tfpw_y), loc=0, scale=1))
        else:
            p_tot_tfpw_y = mkh.PROB_MK_N[np.nansum(np.abs(s_tot['tfpw_y'])),
                                         np.sum([np.count_nonzero(~np.isnan(item))
                                                 for item in multi_obs])] # TODO: check this !

        # Determine the statistical significance
        (result[n_tas]['p'], result[n_tas]['ss']) = prob_3pw(p_tot_pw, p_tot_tfpw_y, alpha_mk)

        # Compute the chi-squre to test the homogeneity between time aggregations. Since the slope
        # is computed from VCTFPW, the homogeneity is also computed from VCTFPW.
        xhomo = np.nansum(z**2) - n_tas * np.nanmean(z)**2

    # Write the yearly slope and CL
    # xhomo has a chi-squared distribution with n-1 and 1 degree of freedom. Seasonal trends
    # are homogeneous if xhomo is smaller than the threshold defined by the degree of freedom and
    # the confidence level alpha_xhomo.
    if n_tas == 1 or (xhomo <= spstats.distributions.chi2.ppf(1-alpha_xhomo/100, df=n_tas-1)):
        for item in ['slope', 'ucl', 'lcl']:
            result[n_tas][item] = np.nanmedian([result[key][item] for key in result
                                                if key != n_tas])
    else:
        warnings.warn('The trends for the temporal aggregation are not homogenous.')
        for item in ['slope', 'ucl', 'lcl']:
            result[n_tas][item] = np.nan

    return result
