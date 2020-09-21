# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This file contains some hardcoded test parameters.
"""

from pathlib import Path

# Number of decimals to match in the assertions
TEST_TOLERANCE = 10

# Location of the test data files.
TEST_DATA_LOC = Path(__file__).parent.absolute() / 'test_data'
