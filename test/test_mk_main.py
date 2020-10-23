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

def test_compute_mk_stats():
    """ Test the compute_mk_stats() function.

    This method specifically tests:
        - proper computation

    """

    test_params = {'1': 'default', '2': [90, 95]}

    # Loop through the tests
    for test_id in test_params:

        # Load the test data
        test_in1 = load_test_data('compute_MK_stat_test%s_in1.csv' % (test_id))
        test_in2 = load_test_data('compute_MK_stat_test%s_in2.csv' % (test_id))
        test_in3 = float(load_test_data('compute_MK_stat_test%s_in3.csv' % (test_id)))
        test_out1 = load_test_data('compute_MK_stat_test%s_out1.csv' % (test_id))
        test_out2 = load_test_data('compute_MK_stat_test%s_out2.csv' % (test_id))
        test_out3 = load_test_data('compute_MK_stat_test%s_out3.csv' % (test_id))
        test_out4 = load_test_data('compute_MK_stat_test%s_out4.csv' % (test_id))

        # Create proper datetimes
        test_in1_dts = np.array([datetime(int(item[0]), int(item[1]), int(item[2]),
                                          int(item[3]), int(item[4]), int(item[5]))
                                 for item in test_in1])


        # Run the function
        if test_params[test_id] == 'default':
            out = mk.compute_mk_stat(test_in1_dts, test_in2, test_in3)
        else:
            out = mk.compute_mk_stat(test_in1_dts, test_in2, test_in3,
                                     alpha_mk=test_params[test_id][0],
                                     alpha_cl=test_params[test_id][1])

        for (item_ind, item) in enumerate(['p', 'ss', 'slope', 'ucl', 'lcl']):
            assert np.round(out[0][item], TEST_TOLERANCE) == np.round(test_out1[item_ind],
                                                                                TEST_TOLERANCE)
        assert np.round(out[1], TEST_TOLERANCE) == np.round(test_out2, TEST_TOLERANCE)
        assert np.round(out[2], TEST_TOLERANCE) == np.round(test_out3, TEST_TOLERANCE)
        assert np.round(out[3], TEST_TOLERANCE) == np.round(test_out4, TEST_TOLERANCE)

def test_mk_temp_aggr_single():
    """ Test the mk_temp_aggr() function.

    This method specifically tests:
        - proper computation for a single temporal aggregation
    """

    test_params = {1: 'default',
                   2: [90, 95, 95, 90],
                   3: 'default',
                   4: [90, 95, 95, 90],
                   5: 'default',
                   6: [90, 95, 95, 90]
                   }

    # Loop throught the different tests
    for test_id in test_params:

        # load the data
        test_in = load_test_data('MK_tempAggr_test%i_in.csv' % (np.ceil(test_id/2)))
        if (test_id % 2) == 0:
            test_out = load_test_data('MK_tempAggr_test%i_out_CL.csv' % (np.ceil(test_id/2)))
        else:
            test_out = load_test_data('MK_tempAggr_test%i_out_default.csv' % (np.ceil(test_id/2)))

        # For consistency, make sure the output is always 2-dimensional
        if np.ndim(test_out) == 1:
            test_out = np.array([test_out])

        # How many "seasons" do I have ?
        n_tas = np.shape(test_in)[1] // 7

        # Restructure the input to feed the functions
        # Get the proper datetime
        # Pay attention to the fact that not all seasons have the same number of entries ...
        # Some rowas have NaN as datetimes to fill the gaps in the CSV files. Deal with it.
        test_in_dts = [np.array([datetime(int(item[0]), int(item[1]), int(item[2]),
                                          int(item[3]), int(item[4]), int(item[5]))
                                 for item in test_in[:, tas_ind:tas_ind+7]
                                 if not np.isnan(item[0])])
                       for tas_ind in range(0, n_tas*7, 7)]

        # Idem for the observations
        test_in_obs = [np.array([item[6] for item in test_in[:, tas_ind:tas_ind+7]
                                 if not np.isnan(item[0])])
                       for tas_ind in range(0, n_tas*7, 7)]

        # Run the function
        if test_params[test_id] == 'default':
            out = mk.mk_temp_aggr(test_in_dts, test_in_obs, 0.01)
        else:
            out = mk.mk_temp_aggr(test_in_dts, test_in_obs, 0.01,
                                  alpha_mk=test_params[test_id][0],
                                  alpha_cl=test_params[test_id][1],
                                  alpha_xhomo=test_params[test_id][2],
                                  alpha_ak=test_params[test_id][3])

        for tas_ind in range(0, n_tas+1, 1):
            # The matlab routine does not return the "total" results if there is only 1 time aggr.
            if (n_tas == 1) and (tas_ind > 0):
                continue
            # Else, compare the results for all the parameters
            for (item_ind, item) in enumerate(['p', 'ss', 'slope', 'ucl', 'lcl']):
                if np.isnan(test_out[tas_ind][item_ind]):
                    assert np.isnan(out[tas_ind][item])
                else:
                    assert np.round(out[tas_ind][item], TEST_TOLERANCE) == \
                           np.round(test_out[tas_ind][item_ind], TEST_TOLERANCE)
