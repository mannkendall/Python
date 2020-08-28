# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains test functions for the mk_stats module.
"""

# Import from python packages
from pathlib import Path
from datetime import datetime
import numpy as np

# Import from current package
from mannkendall import mk_stats as mks


# Load some local test_data
TEST_DATA_FN = Path(__file__).parent / 'test_data' / 'test_data_C.csv'
TEST_DATA = np.genfromtxt(TEST_DATA_FN, skip_header=1, delimiter=';',
                          missing_values='NaN', filling_values=np.nan)
# Make sure the datetime are properly set
TEST_OBS_DTS = np.array([datetime(int(row[0]), int(row[1]), int(row[2]),
                                  int(row[3]), int(row[4]), int(row[5])) for row in TEST_DATA])

def test_std_normal_var():
    """ Test the std_normal_var() function.

    This method specifically tests:
        - proper computation of ratio.

    """

    assert np.round(mks.std_normal_var(27, 118.9091), 4) == 2.3843 # Normal case

def test_s_test():
    """ Test the s_test() function.

    This method specifically tests:
        - proper computation of s.

    """

    assert mks.s_test(TEST_DATA[:, 6], TEST_OBS_DTS)[0] == 27
    assert np.all(mks.s_test(TEST_DATA[:, 6], TEST_OBS_DTS)[1] == np.array([5, 6]))

def test_sen_slope():
    """ Test the sen_slope() function.

    This method specifically tests:
        - proper computation of slope.

    """

    out = mks.sen_slope(TEST_OBS_DTS, TEST_DATA[:, 6], 118.9091, confidence=90)
    # Check the outcome., remembering that the python routine *always* returns the slope in 1/s !
    # TODO: make this test with bigger precision, to check that the lcl and ucl are correct.
    assert np.all(np.round(np.array(out) * 24 * 3600, 4) == np.array([0.0328, 0.0246, 0.0354]))
