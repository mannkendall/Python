# -*- coding: utf-8 -*-
'''
Copyright (c) 2022 MeteoSwiss, contributors of the original matlab version of the code listed in
ORIGINAL_AUTHORS.
Copyright (c) 2022 MeteoSwiss, contributors of the Python version of the code listed in AUTHORS.

Distributed under the terms of the BSD 3-Clause License.

SPDX-License-Identifier: BSD-3-Clause

This script can be used together with a Github Action to check whether a code version has been
properly incremented.

Created in January 2022; F.P.A. Vogt; frederic.vogt@meteoswiss.ch
Adapted to mannkendall in July 2022; F.P.A. Vogt; frederic.vogt@meteoswiss.ch
'''

import argparse
from pkg_resources import parse_version


def main():
    ''' The main function. '''

    # Use argparse to allow feeding parameters to this script
    parser = argparse.ArgumentParser(description='''Compare the versions between the head and base
                                                 branches of the PR. Fails is Head <= Base.''',
                                     epilog='Feedback, questions, comments: \
                                             frederic.vogt@meteoswiss.ch \n',
                                     formatter_class=argparse.RawTextHelpFormatter)

    parser.add_argument('head', action='store', metavar='version',
                        help='Head version.')

    parser.add_argument('base', action='store', metavar='version',
                        help='Base version.')

    # What did the user type in ?
    args = parser.parse_args()

    # Print the versions fed by the user, for monitoring
    print("Head:", args.head)
    print("Base:", args.base)

    if parse_version(args.head) > parse_version(args.base):
        print("Version was increased. Well done.")
        return True

    raise Exception('Ouch ! Version was not increased ?!')


if __name__ == '__main__':

    main()
