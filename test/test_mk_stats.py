# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains test functions for the mk_stats module.
"""

# Import from python packages
from datetime import datetime
import numpy as np

# Import from current package
from mannkendall import mk_stats as mks

# Get the local parameters I need to run the tests
from .test_hardcoded import load_test_data, TEST_TOLERANCE

def test_std_normal_var():
    """ Test the std_normal_var() function.

    This method specifically tests:
        - proper computation of ratio.

    """

    # Load the test data
    test_in1 = int(load_test_data('STD_normal_var_test1_in1.csv'))
    test_in2 = float(load_test_data('STD_normal_var_test1_in2.csv'))
    test_out = load_test_data('STD_normal_var_test1_out.csv')

    # Run the function
    out = mks.std_normal_var(test_in1, test_in2)

    assert np.round(out, TEST_TOLERANCE) == np.round(test_out, TEST_TOLERANCE)

def test_s_test():
    """ Test the s_test() function.

    This method specifically tests:
        - proper computation of s.

    """

    # Load the data
    test_in1 = load_test_data('S_test_test1_in1.csv')
    test_in2 = load_test_data('S_test_test1_in2.csv')
    test_out1 = load_test_data('S_test_test1_out1.csv')
    test_out2 = load_test_data('S_test_test1_out2.csv')

    # Create proper datetime entries
    test_in2_dts = np.array([datetime(int(item[0]), int(item[1]), int(item[2]),
                                      int(item[3]), int(item[4]), int(item[5]))
                             for item in test_in2])

    # Run the function
    out = mks.s_test(test_in1, test_in2_dts)

    # Validate the output
    assert np.round(out[0], TEST_TOLERANCE) == np.round(test_out1, TEST_TOLERANCE)
    assert np.all([np.round(item, TEST_TOLERANCE) == np.round(test_out2[item_ind], TEST_TOLERANCE)
                   for (item_ind, item) in enumerate(out[1])])

def test_sen_slope():
    """ Test the sen_slope() function.

    This method specifically tests:
        - proper computation of slope.

    """

    # Load the data
    test_in1 = load_test_data('Sen_slope_test1_in1.csv')
    test_in2 = load_test_data('Sen_slope_test1_in2.csv')
    test_in3 = float(load_test_data('Sen_slope_test1_in3.csv'))
    test_out1 = load_test_data('Sen_slope_test1_out1.csv')
    test_out2 = load_test_data('Sen_slope_test1_out2.csv')
    test_out3 = load_test_data('Sen_slope_test1_out3.csv')

    # Create proper datetime entries
    test_in1_dts = np.array([datetime(int(item[0]), int(item[1]), int(item[2]),
                                      int(item[3]), int(item[4]), int(item[5]))
                             for item in test_in1])

    # Run the function
    out = mks.sen_slope(test_in1_dts, test_in2, test_in3)

    # Here, I need to remember that the slopes return are in 1/s, but matlab gives them in 1/d
    out = np.array(out) * 3600 * 24

    # Validate the output
    assert np.round(out[0], TEST_TOLERANCE) == np.round(test_out1, TEST_TOLERANCE)
    assert np.round(out[1], TEST_TOLERANCE) == np.round(test_out2, TEST_TOLERANCE)
    assert np.round(out[2], TEST_TOLERANCE) == np.round(test_out3, TEST_TOLERANCE)
