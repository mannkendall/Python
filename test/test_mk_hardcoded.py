# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains test functions for the mk_hardcoded module.
"""

# Import from other Python find_packages
import numpy as np

# Import from current package
from mannkendall import mk_hardcoded as mkh

def test_prob_mk_n():
    """ A basic test to make sure the hardcoded matrix is correct.

    This method specifically tests:
        - values of the matrix seem correct
    """

    # Check the sum of the non-nan values
    assert np.round(np.nansum(mkh.PROB_MK_N), 8) == 12.69898888

    # CHeck the total number of nans and non-nans
    n_nans = len(mkh.PROB_MK_N[np.isnan(mkh.PROB_MK_N)])

    assert n_nans == 374
    assert np.size(mkh.PROB_MK_N) - n_nans == 86
