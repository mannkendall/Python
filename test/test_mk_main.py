# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause
"""

# Import from other Python find_packages
from pathlib import Path
from datetime import datetime
import numpy as np

# Import from current package
from mannkendall import __version__
import mannkendall as mk

# Get the local parameters I need to run the tests
from .test_hardcoded import load_test_data, TEST_TOLERANCE

def test_version():
    """ A basic test to make sure the package version is correct.

    This test really is a quick means to check that tests actually work.

    This method specifically tests:
        - version of installed package matches version fileself.
    """

    # Get the hardcoded version
    with open(Path(__file__).resolve().parent /
              '..' / 'src' / 'mannkendall' / 'mk_version.py') as fid:
        version_ff = next(line.split("'")[1] for line in fid.readlines() if 'VERSION' in line)

    # Compare with the package version
    assert __version__ == version_ff

def test_prob_3pw():
    """ Test the prob_3pw() function.

    This method specifically tests:
        - proper computation
    """

    test_params = {'1': None, '2': None}

    # Loop through the different tests
    for test_id in test_params:

        # Load the test data
        test_in1 = float(load_test_data('Prob_3PW_test%s_in1.csv' % (test_id)))
        test_in2 = float(load_test_data('Prob_3PW_test%s_in2.csv' % (test_id)))
        test_in3 = float(load_test_data('Prob_3PW_test%s_in3.csv' % (test_id)))
        test_out1 = load_test_data('Prob_3PW_test%s_out1.csv' % (test_id))
        test_out2 = int(load_test_data('Prob_3PW_test%s_out2.csv' % (test_id)))

        # Run the function
        out = mk.prob_3pw(test_in1, test_in2, test_in3)

        assert np.round(out[0], TEST_TOLERANCE) == np.round(test_out1, TEST_TOLERANCE)
        assert np.round(out[1], TEST_TOLERANCE) == np.round(test_out2, TEST_TOLERANCE)

def test_mk_multi_tas():
    """ Test the mk_multi_tas() function.
#
#    This method specifically tests:
#        - proper computation
#    """

    # Run the test for the two datasets I have.
    '''
    for (OBS_DTS, OBS) in [[BNB_DTS, BNB_DATA],
                           [HPB_DTS, HPB_DATA]]:

        # Prepare the data to be split in 4 seasons.
        months = np.array([item.month for item in OBS_DTS])
        # Which entry corresponds to which season ?
        #inds = [np.where((months == item[0]) + (months == item[1]) + (months == item[2]))
        #        for item in [[3, 4, 5],[6, 7, 8,], [9, 10, 11], [12, 1, 2]]]
        inds = [np.where((months == ind+1)) for ind in range(12)]

        # Extract the data accordingly
        multi_obs = [OBS[:, 6][ind] for ind in inds]
        multi_obs_dts = [OBS_DTS[ind] for ind in inds]

        # Run the code
        out = mk.mk_multi_tas(multi_obs_dts, multi_obs, 2, pw_method='3pw')

        # Validate the results
        # Todo: do the actual test !!!
        print(out)
    '''
    assert True

    # Todo: also test for month splitting
