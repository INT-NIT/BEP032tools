#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import errno
import json

import argparse

from AnDO_engine import is_bids, is_bids_verbose

dir_rules = os.path.join(os.path.dirname(__file__)) + 'rules/'


def path_hierarchy(path):
    """[make a json tree structure of the folder given in parameter]
    Arguments:
        path {[type]} -- [Path to the folder]
    Returns:
        [json] -- [Tree of the folder]
    """

    hierarchy = {'type': 'directory', 'name': os.path.basename(path),
                 'path': path}

    try:
        hierarchy['children'] = [path_hierarchy(os.path.join(path,
                                 contents)) for contents in
                                 os.listdir(path)]
    except OSError as e:
        if e.errno != errno.ENOTDIR:
            raise
        hierarchy['type'] = 'file'

    return hierarchy


def get_name_in_dir(list_dict, names):
    """[Get all the name of directories in the Dict recusively]
    Arguments:
        list_dict {[Dict]} -- [Json to dict ]
        names {[list]} -- [Names of directories founds]
    Returns:
        [list] -- [Names of directories founds]
    """

    for my_dict in list_dict:

        if my_dict['type'] == 'directory':
            names.append(my_dict['name'])
            names = get_name_in_dir(my_dict['children'], names)

    return names


if __name__ == '__main__':

    # add argparse for verbose option

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
        names = []
        dic_data = json.loads(json.dumps(path_hierarchy(directory),
                              indent=2, sort_keys=True))
        names = get_name_in_dir([dic_data], names)

        error = is_bids_verbose(names)

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

        dic_data = json.loads(json.dumps(path_hierarchy(directory),
                              indent=2, sort_keys=True))

        names = []
        names = get_name_in_dir([dic_data], names)
        error_not_found = is_bids(names)
        if not error_not_found:
            print("\n" +
                  directory +
                  ": Is Not validated by AnDOChecker")
        else:
            print("\n" +
                  directory +
                  ": Is validated by AnDOChecker")
