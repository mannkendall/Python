# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains test functions for the mk_tools module.
"""

# Import from python packages
import numpy as np
import pytest

# Import from current package
from mannkendall import mk_tools as mkt

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
    assert np.all(mkt.nb_tie(np.array([1, 1, 1, 1, 1, np.nan]), 2.4) == np.array([5])) # res > interval
    assert np.all(mkt.nb_tie(test_array, 2.0) == np.array([2, 2, 3])) # normal case
    assert np.all(mkt.nb_tie(test_array_2, 2.0) == np.array([4, 2, 4, 2])) # normal case

def test_kendall_var():
    """ Test the kendall_var function.

    This method specifically tests:
        - proper variance computation
    """

    test_array_2 = np.array([1, 3, 5, 2, 8, 1, 5, 5, 6, 7, 1, np.nan, np.nan, 4])
    t = np.array([4, 2, 4, 2])
    n = np.array([7, 5])

    assert mkt.kendall_var(test_array_2, t, n) == 140 # normal case
