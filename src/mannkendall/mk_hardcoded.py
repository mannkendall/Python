# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors of the original matlab version of the code listed in
ORIGINAL_AUTHORS.
Copyright (c) 2020 MeteoSwiss, contributors of the Python version of the code listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains the hardcoded parameters for the mannkendall package.
"""

import numpy as np

#: list: supported pre-whitening methods "tags"
VALID_PW_METHODS = ['pw', 'tfpw_y', 'tfpw_ws', 'vctfpw', '3pw']

#: ndarray: MannKendall probability array
PROB_MK_N = np.array([
    [np.nan, np.nan, np.nan, 0.625, 0.592, np.nan, np.nan, 0.548, 0.54, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, 0.5, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, 0.375, 0.408, np.nan, np.nan, 0.452, 0.46, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, 0.36, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, 0.167, 0.242, np.nan, np.nan, 0.36, 0.381, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, 0.235, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, 0.042, 0.117, np.nan, np.nan, 0.274, 0.306, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, 0.136, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, 0.042, np.nan, np.nan, 0.199, 0.238, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, 0.068, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, 0.0083, np.nan, np.nan, 0.138, 0.179, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, 0.028, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.089, 0.13, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, 0.0083, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.054, 0.09, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, 0.0014, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.031, 0.06, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.016, 0.038, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.0071, 0.022, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.0028, 0.012, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.00087, 0.0063, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.00019, 0.0029, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 2.50E-05, 0.0012, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.00043, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.00012, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 2.50E-05, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 2.80E-06, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan]])
