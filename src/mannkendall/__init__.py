# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors of the original matlab version of the code listed in
ORIGINAL_AUTHORS.
Copyright (c) 2020 MeteoSwiss, contributors of the Python version of the code listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause
"""

# Get the version of the code to behave as usual
from .mk_version import VERSION as __version__

# To simplify the call of the highest level functions
from .mk_main import *
