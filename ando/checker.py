# File: checker.py
# Project: ando
# File Created: Tuesday, 30th June 2020 10:50:05 am
# Author: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Last Modified: Thursday, 2nd July 2020 1:29:58 pm
# Modified By: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Copyright - 2020 MIT, Institue de neurosciences de la Timone


# !/usr/bin/python
# -*- coding: utf-8 -*-


import os
import argparse

from ando.engine import is_AnDO, is_AnDO_verbose

dir_rules = os.path.join(os.path.dirname(__file__)) + 'rules/'
def main():

    parser = argparse.ArgumentParser()
    parser.add_argument('-v', '--verbose', action='store_true',
                        help='increase output verbosity')
    parser.add_argument('path', help='Path to your folder ')
    args = parser.parse_args()

    if args.verbose:
        try:
            directory = args.path
        except IndexError:
            directory = '.'
        error = is_AnDO_verbose(directory)
        
        if error == 1:
            print("\n" +
                  directory +
                  ": Is Not validated by AnDOChecker")
        else:
            print("\n" +
                  directory +
                  ": Is validated by AnDOChecker")
    else:
        try:
            directory = args.path
        except IndexError:

            directory = '.'

        error_not_found = is_AnDO(directory)
        if not error_not_found:
            print("\n" +
                  directory +
                  ": Is Not validated by AnDOChecker")
        else:
            print("\n" +
                  directory +
                  ": Is validated by AnDOChecker")

if __name__ == '__main__':
    """
    Main function :

    usage: AnDOChecker.py [-h] [-v] pathToFolder

        positional arguments:
        path           Path to your folder

        optional arguments:
        -h, --help     show this help message and exit
        -v, --verbose  increase output verbosity

    """
    # add argparse for verbose option
    main()