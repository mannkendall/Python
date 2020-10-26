# -*- coding: utf-8 -*-
"""
Copyright (c) 2020 MeteoSwiss, contributors listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause
"""

from pathlib import Path
from setuptools import setup, find_packages  # Always prefer setuptools over distutils

# Get the VERSION from the dedicate file
with open(Path('.') / 'src' / 'mannkendall' / 'mk_version.py') as fid:
    version = next(line.split("'")[1] for line in fid.readlines() if 'VERSION' in line)

# Extract the long description from the README
with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    dependency_links=[],
    name="mannkendall",
    version=version,
    license='BSD 3-Clause',

    # Include all packages under src
    packages=find_packages("src"),

    # Tell setuptools packages are under src
    package_dir={"": "src"},

    url="https://github.com/MeteoSwiss-MDA/mannkendall",
    author="MeteoSwiss",
    author_email="fpavogt@users.noreply.github.com",
    description="TBD",
    long_description=long_description,
    long_description_content_type="text/markdown",
    python_requires='>=3.8.0',
    install_requires=["numpy>=1.19.2",
                      "scipy>=1.5.0",
                      "statsmodels>=0.12.0",
                      "pytest"],

    classifiers=[

        # How mature is this project? Common values are
        #   3 - Alpha
        #   4 - Beta
        #   5 - Production/Stable
        'Development Status :: 4 - Beta',

        # Indicate who your project is intended for
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Atmospheric Science',

        # Pick your license as you wish (should match "license" above)
        'License :: OSI Approved :: BSD License',

        # Specify the Python versions you support here. In particular, ensure
        # that you indicate whether you support Python 2, Python 3 or both.
        'Programming Language :: Python :: 3.8',

    ],

    include_package_data=True,  # If True, non .py files make it onto pypi !

)
