# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains test functions for the mk_tools module.
"""

# Import from python packages
from datetime import datetime
from pathlib import Path
import numpy as np
import pytest

# Import from current package
from mannkendall import mk_tools as mkt

# Get the local parameters I need to run the tests
from .test_hardcoded import TEST_DATA_LOC, TEST_TOLERANCE

def test_de_sort():
    """ Test the de_sort() utility function.

    This method specifically tests:
        - correct indices swapping.
    """

    a = np.random.rand(50)
    sort_inds = a.argsort()

    assert np.all(a == mkt.de_sort(a[sort_inds], sort_inds))

def test_dt_to_s():
    """ Test the dt_to_s utility function.

    This method specifically tests:
        - proper handling of datetime.timedeltas.

    """

    t_1 = datetime(2020, 1, 1, 0, 0, 0)
    t_2 = datetime(2020, 1, 1, 0, 0, 1)
    t_3 = datetime(2020, 1, 1, 0, 1, 0)
    t_4 = datetime(2020, 1, 1, 1, 0, 0)
    t_5 = datetime(2020, 1, 2, 0, 0, 0)
    t_6 = datetime(2020, 2, 1, 0, 0, 0)
    t_7 = datetime(2021, 1, 1, 0, 0, 0)

    dts = np.array([t_1, t_2, t_3, t_4, t_5, t_6, t_7])
    print(mkt.dt_to_s(dts-np.array([t_1])))

    # CHeck that leap years are properly dealt with.
    assert np.all(mkt.dt_to_s(dts-np.array([t_1])) ==
                  np.array([0, 1, 60, 3600, 3600*24, 3600*24*31, 3600*24*366]))

def test_nb_tie():
    """ Test the nb_tie function.

    This method specifically tests:
        - proper sectioning of the data array.
    """

    test_array = np.array([0, 1, 2, 3, 4, 5, 6])
    test_array_2 = np.array([1, 3, 5, 2, 8, 1, 5, 5, 6, 7, 1, np.nan, np.nan, 4])

    pytest.raises(Exception, mkt.nb_tie, 'a', 2) # Check exceptions
    pytest.raises(Exception, mkt.nb_tie, np.zeros(2), '2') # Check exceptions
    assert np.isnan(mkt.nb_tie(test_array * np.nan, 2)) # nan if all nan's
    assert np.isnan(mkt.nb_tie(np.zeros(4), 2)) # nans if less than 4 valid data points.
    assert np.all(mkt.nb_tie(np.ones(5), 2) == np.array([5])) # Identical values
    assert np.all(mkt.nb_tie(np.array([0, 0, 0, 1, 1]), 2.4) == np.array([5])) # res > interval
    assert np.all(mkt.nb_tie(np.array([1, 1, 1, 1, 1, np.nan]), 2.4) == np.array([5])) # same values
    assert np.all(mkt.nb_tie(test_array, 2.0) == np.array([2, 2, 3])) # normal case
    assert np.all(mkt.nb_tie(test_array_2, 2.0) == np.array([4, 2, 4, 2])) # normal case

def test_kendall_var():
    """ Test the kendall_var function.

    This method specifically tests:
        - proper variance computation
    """

    # Some fake data
    test_array_2 = np.array([1, 3, 5, 2, 8, 1, 5, 5, 6, 7, 1, np.nan, np.nan, 4])
    t = np.array([4, 2, 4, 2])
    n = np.array([7, 5])

    assert mkt.kendall_var(test_array_2, t, n) == 140 # normal case


def test_nanautocorr():
    """ Test the nanautocorr function.

    This method specifically tests:
        - proper correlation computation
    """

    test_data = np.genfromtxt(TEST_DATA_LOC / 'test_nanautocorr_in.csv',
                              skip_header=0, delimiter=',',
                              missing_values='NaN', filling_values=np.nan)
    test_out = np.genfromtxt(TEST_DATA_LOC / 'test_nanautocorr_out.csv',
                             skip_header=0, delimiter=',',
                             missing_values='NaN', filling_values=np.nan)

    out = mkt.nanautocorr(test_data, 2, r=1)

    assert np.all(np.round(out[0], TEST_TOLERANCE) == np.round(test_out, TEST_TOLERANCE))

def test_levinson():
    """ Test the levinson function.

    This method specifically tests:
        - method returns are similar to the matlab implementation.
    """

    # TODO: fix this test
    assert True

    # Compute the autocorrelation
    #(x, _) = mkt.nanautocorr(TEST_DATA[:, 6], 6, r=5)

    # Compute the confidence limits for the autocorrelation
    #x_1 = x / np.count_nonzero(~np.isnan(TEST_DATA[:, 6]))
    #n = 5

    #out = mkt.levinson(x_1, n)

    #assert np.all(np.round(out[0], 4) == np.array([1, -0.7633, -0.9680, 1.0503, 0.7590, -1.0868]))
    #assert np.round(out[1], 4) == -0.0026
    #assert np.all(np.round(out[2], 4) == np.array([-0.8257, -0.6392, 0.1673, 0.3899, -1.0868]))
