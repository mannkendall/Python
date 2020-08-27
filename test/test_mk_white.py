# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains test functions for the mk_white module.
"""

# Import from python packages
from pathlib import Path
from datetime import datetime
import numpy as np

# Import from current package
from mannkendall import mk_white as mkw


# Load some local test_data
TEST_DATA_FN = Path(__file__).parent / 'test_data' / 'test_data_C.csv'
#TEST_DATA_FN = Path(__file__).parent / 'test_data' / 'BNB_data.csv'
#TEST_DATA_FN = Path(__file__).parent / 'test_data' / 'HPB_data.csv'
TEST_DATA = np.genfromtxt(TEST_DATA_FN, skip_header=1, delimiter=';',
                          missing_values='NaN', filling_values=np.nan)
# Make sure the datetime are properly set
TEST_OBS_DTS = np.array([datetime(int(row[0]), int(row[1]), int(row[2]),
                                  int(row[3]), int(row[4]), int(row[5])) for row in TEST_DATA])
#
def test_nanprewhite_arok():
    """ Test the std_normal_var() function.

    This method specifically tests:
        - proper computation of ratio.

    """

    test1 = np.array([1, 3, 5, 2, 8, 1, 5, 5, 6, 7, 1, np.nan, np.nan, 4])
    out1 = [-0.4418, 0.2590, test1, 0]

    test2 = TEST_DATA[:, 6]
    out2 = [0.8257, 0.1701, np.array([np.nan, 2.3486, 4.1972, np.nan, np.nan, 9.1559,
                                      -2.5368, 7.5045, 4.4632, 5.7246, 6.1604, -0.4039]), 95]

    # Loop through the different tests
    for (test_in, test_out) in [(test1, out1), (test2, out2)]:

        out = mkw.nanprewhite_arok(test_in)

        assert np.round(np.array(out[0]), 4) == test_out[0]
        assert np.round(np.array(out[1]), 4) == test_out[1]

        assert len(out[2]) == len(test_out[2])
        for (ind, item) in enumerate(out[2]):
            if np.isnan(item):
                assert np.isnan(test_out[2][ind])
            else:
                assert np.round(item, 4) == test_out[2][ind]

        assert out[3] == test_out[3]


def test_prewhite():
    """ test the prewhite() function.

    This method specifcally tests:
        - proper computation by the routine.

    """

    out = mkw.prewhite(TEST_DATA[:, 6], TEST_OBS_DTS, 2)
    #print('pw:')

    for (ind, item) in enumerate(['pw', 'pw_cor', 'tfpw_y', 'tfpw_ws', 'vctfpw']):
    #for (ind, item) in enumerate(['pw', 'tfpw_y', 'tfpw_ws', 'vctfpw']):
        for j in range(len(out[0][item])):
            if np.isnan(out[0][item][j]):
                assert np.isnan(TEST_DATA[j, 7+ind])
            else:
                # TODO: could this be more accurate ?
                assert np.abs(out[0][item][j] - TEST_DATA[j, 7+ind]) < 2e-3
