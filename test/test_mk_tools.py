# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains test functions for the mk_tools module.
"""

# Import from python packages
from datetime import datetime
import numpy as np
import pytest

# Import from current package
from mannkendall import mk_tools as mkt

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

    # Some fake data
    obs = np.array([1, 3, 5, 2, 8, 1, 5, 5, 6, 7, 1, np.nan, np.nan, 4])
    out = mkt.nanautocorr(obs, 2, r=1)

    assert np.all(np.round(out[0], 4) == np.array([1.0, -0.4418, 0.1836]))
    assert np.all(np.round(out[1], 4) == 0.5727)
