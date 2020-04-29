#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function
import os
import errno
import json

import argparse

from AnDO_engine import is_AnDO, is_AnDO_verbose

dir_rules = os.path.join(os.path.dirname(__file__)) + 'rules/'


def path_hierarchy(path):
    """
    Make a json tree structure of the folder given in parameter]
    
    :param path: Path to the folder 
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
    """
    Get all the name of directories in the Dict recusively
    
    :param list_dict: Json to dict 
    :param names: Names of directories founds
    """

    for my_dict in list_dict:

        if my_dict['type'] == 'directory':
            names.append(my_dict['name'])
            names = get_name_in_dir(my_dict['children'], names)

    return names

def fast_scandir(dirname):
    subfolders= [f.path for f in os.scandir(dirname) if f.is_dir()]
    for dirname in list(subfolders):
        subfolders.extend(fast_scandir(dirname))
    return subfolders

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

        error = is_AnDO_verbose(names)

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
        
          
        #print([x[0] for x in os.walk(directory)])
        
        
        names = []
        names = get_name_in_dir([dic_data], names)
        
        error_not_found = is_AnDO(directory)
        if not error_not_found:
            print("\n" +
                  directory +
                  ": Is Not validated by AnDOChecker")
        else:
            print("\n" +
                  directory +
                  ": Is validated by AnDOChecker")
