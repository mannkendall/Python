# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause
"""

# Import from other Python find_packages
from pathlib import Path

# Import from current package
from mannkendall import __version__

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
