# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains test functions for the mk_white module.
"""

# Import from python packages
from pathlib import Path
import numpy as np

# Import from current package
from mannkendall import mk_white as mkw


# Load some local test_data
TEST_DATA_FN = Path(__file__).parent / 'test_data' / 'test_data_C.csv'
TEST_DATA = np.genfromtxt(TEST_DATA_FN, skip_header=1, delimiter=';',
                          missing_values='NaN', filling_values=np.nan)

#
def test_nanprewhite_arok():
    """ Test the std_normal_var() function.

    This method specifically tests:
        - proper computation of ratio.

    """

    test1 = np.array([1, 3, 5, 2, 8, 1, 5, 5, 6, 7, 1, np.nan, np.nan, 4])
    out1 = [np.array([-0.4418]), np.array([0.2590]), 1-1, test1, 0]

    test2 = TEST_DATA[:, 6]
    # TODO: note that there was a sign typo in the original email for 0.8257
    out2 = [np.array([0.8257]), np.array([0.1701]), 3-1,
            np.array([np.nan, 2.3486, 4.1972, np.nan, np.nan, 9.1559,
                      -2.5368, 7.5045, 4.4632, 5.7246, 6.1604, -0.4039]),
                      95]

    # Loop through the different tests
    for (test_in, test_out) in [(test1, out1), (test2, out2)]:

        out = mkw.nanprewhite_arok(test_in)

        assert np.round(np.array(out[0]), 4) == test_out[0]
        assert np.round(np.array(out[1]), 4) == test_out[1]
        assert out[2] == test_out[2]

        assert len(out[3]) == len(test_out[3])
        for (ind, item) in enumerate(out[3]):
            if np.isnan(item):
                assert np.isnan(test_out[3][ind])
            else:
                assert np.round(item, 4) == test_out[3][ind]

        assert out[4] == test_out[4]
