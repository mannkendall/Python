# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains some hardcoded test parameters.
"""

from pathlib import Path
import numpy as np

# Number of decimals to match in the assertions
TEST_TOLERANCE = 9

# Location of the test data files.
TEST_DATA_LOC = Path(__file__).parent.absolute() / 'test_data'

# A function to load the data, to save me the trouble of writing it all the time
def load_test_data(fn, loc=TEST_DATA_LOC, missing_values='NaN', delimiter=',', skip_header=0):
    """ Loads a specific test data set in memory.

    Args:
        fn (str): filename
        loc (pathlib.Path, optional): the location of the test data. Defaults to TEST_DATA_LOC.
        missing_values (str, optional): string corresponding to missing values. Defaults to 'NaN'.
        delimiter (str, optional): str for separating entries. Defaults to ','.
        skip_header(int, optional): header lines to skip. Defaults to 0.

    Returns:
        ndarray: the test data

    """
    test_data = np.genfromtxt(loc / fn,
                              skip_header=skip_header, delimiter=delimiter,
                              missing_values=missing_values, filling_values=np.nan)

    return test_data
