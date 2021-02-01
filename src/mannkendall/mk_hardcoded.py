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
    [np.nan, np.nan, np.nan, 0.625, 0.592, np.nan, np.nan, 0.548, 0.540, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, 0.500, 0.500, np.nan, np.nan, 0.500],
    [np.nan, np.nan, np.nan, 0.375, 0.408, np.nan, np.nan, 0.452, 0.46, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, 0.360, 0.386, np.nan, np.nan, 0.431],
    [np.nan, np.nan, np.nan, 0.167, 0.242, np.nan, np.nan, 0.360, 0.381, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, 0.235, 0.281, np.nan, np.nan, 0.364],
    [np.nan, np.nan, np.nan, 0.042, 0.117, np.nan, np.nan, 0.274, 0.306, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, 0.136, 0.191, np.nan, np.nan, 0.300],
    [np.nan, np.nan, np.nan, np.nan, 0.042, np.nan, np.nan, 0.199, 0.238, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, 0.068, 0.119, np.nan, np.nan, 0.242],
    [np.nan, np.nan, np.nan, np.nan, 0.0083, np.nan, np.nan, 0.138, 0.179, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, 0.028, 0.068, np.nan, np.nan, 0.190],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.089, 0.130, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, 0.0083, 0.035, np.nan, np.nan, 0.146],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.054, 0.090, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, 0.0014, 0.015, np.nan, np.nan, 0.108],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.031, 0.060, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.0054, np.nan, np.nan, 0.078],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.016, 0.038, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.0014, np.nan, np.nan, 0.054],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.0071, 0.022, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.0002, np.nan, np.nan, 0.036],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.0028, 0.012, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.023],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.00087, 0.0063, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.014],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.00019, 0.0029, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.0083],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 2.50E-05, 0.0012, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.0046],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.00043, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.0023],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.00012, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.0011],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 2.50E-05, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.00047],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 2.80E-06, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 0.00018],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 5.80E-05],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 1.50E-05],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 2.80E-06],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan],
    [np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, np.nan, 2.80E-07]])
