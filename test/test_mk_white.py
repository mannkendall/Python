# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains test functions for the mk_white module.
"""

# Import from python packages
from datetime import datetime
import numpy as np

# Import from current package
from mannkendall import mk_white as mkw

# Get the local parameters I need to run the tests
from .test_hardcoded import load_test_data, TEST_TOLERANCE

def test_nanprewhite_arok():
    """ Test the std_normal_var() function.

    This method specifically tests:
        - proper computation of ratio.

    """

    test_params = {'1':95, '2':90}

    # Loop throught the different tests
    for test_id in test_params:
        # Load the data
        test_in = load_test_data('nanprewhite_arok_test%s_in.csv' % (test_id))
        test_out1 = load_test_data('nanprewhite_arok_test%s_out1.csv' % (test_id))
        test_out2 = load_test_data('nanprewhite_arok_test%s_out2.csv' % (test_id))
        test_out3 = load_test_data('nanprewhite_arok_test%s_out3.csv' % (test_id))

        # Run the function
        out = mkw.nanprewhite_arok(test_in, alpha_ak=test_params[test_id])

        # Assert the outcome
        assert np.round(np.array(out[0]), TEST_TOLERANCE) == np.round(test_out1, TEST_TOLERANCE)
        assert len(out[1]) == len(test_out2)
        # Assert the vector, also if it contains NaNs.
        for (ind, item) in enumerate(out[1]):
            if np.isnan(item):
                assert np.isnan(test_out2[ind])
            else:
                assert np.round(item, TEST_TOLERANCE) == np.round(test_out2[ind], TEST_TOLERANCE)

        assert out[2] == test_out3


def test_prewhite():
    """ test the prewhite() function.

    This method specifcally tests:
        - proper computation by the routine.

    """

    test_params = {'1': 2, '2': 0.01}

    # loop throught the different tests
    for test_id in test_params:

        # Load the test data
        test_in = load_test_data('prewhite_test%s_in.csv' % (test_id))
        test_out = load_test_data('prewhite_test%s_out.csv' % (test_id), skip_header=1)

        # Convert into proper datetime objects
        test_in_dts = np.array([datetime(int(item[0]), int(item[1]), int(item[2]),
                                         int(item[3]), int(item[4]), int(item[5]))
                                for item in test_in])

        # Run the function
        out = mkw.prewhite(test_in[:, 6], test_in_dts, test_params[test_id])

        # Check the output
        for (ind, item) in enumerate(['pw', 'pw_cor', 'tfpw_y', 'tfpw_ws', 'vctfpw']):
            for (jnd, jtem) in enumerate(test_out[:, ind+1]):
                if np.isnan(out[item][jnd]):
                    assert np.isnan(jtem)
                else:
                    assert np.round(out[item][jnd], TEST_TOLERANCE) == np.round(jtem,
                                                                                TEST_TOLERANCE)
