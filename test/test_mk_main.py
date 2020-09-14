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


# Load some local test_data
TEST_BNB_FN = Path(__file__).parent / 'test_data' / 'BNB_data.csv'
TEST_HPB_FN = Path(__file__).parent / 'test_data' / 'HPB_data.csv'

BNB_DATA = np.genfromtxt(TEST_BNB_FN, skip_header=1, delimiter=';',
                          missing_values='NaN', filling_values=np.nan)
HPB_DATA = np.genfromtxt(TEST_HPB_FN, skip_header=1, delimiter=';',
                          missing_values='NaN', filling_values=np.nan)

# Make sure the datetime are properly set
BNB_DTS = np.array([datetime(int(row[0]), int(row[1]), int(row[2]),
                                  int(row[3]), int(row[4]), int(row[5])) for row in BNB_DATA])
HPB_DTS = np.array([datetime(int(row[0]), int(row[1]), int(row[2]),
                                  int(row[3]), int(row[4]), int(row[5])) for row in HPB_DATA])

def test_version():
    """ A basic test to make sure the package version is correctself.

    This test really is a quick means to check that tests actually workself.

    This method specifically tests:
        - version of installed package matches version fileself.
    """

    # Get the hardcoded version
    with open(Path(__file__).resolve().parent /
              '..' / 'src' / 'mannkendall' / 'mk_version.py') as fid:
        version_ff = next(line.split("'")[1] for line in fid.readlines() if 'VERSION' in line)

    # Compare with the package version
    assert __version__ == version_ff

#def test_mk_year():
#    """ Test the mk_year() function.

#    This method specifically tests:
#        - proper computation
#    """

#    out = mk.mk_year(TEST_OBS_DTS, TEST_DATA[:, 6], 2, pw_method='3pw')

#    print(out)

#    assert False

def test_mk_multi_tas():
    """ Test the mk_multi_tas() function.
#
#    This method specifically tests:
#        - proper computation
#    """

    # Run the test for the two datasets I have.
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

        assert True

    # Todo: also test for month splitting
