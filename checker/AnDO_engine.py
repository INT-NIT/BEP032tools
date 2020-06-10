#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import re
import pathlib
from AnDO_Error import (
    ExperimentError,
    SourceError,
    SourceNotFound,
    SessionError,
    SubError)
from collections import OrderedDict
import itertools
import pprint
dir_rules = os.path.join(os.path.dirname(__file__)) + '/rules/'

def parse_all_path(nested_list_of_dir):
    """
    Transform this
    [
        ['Landing', 'sub-anye', '180116_001_m_anye_land-001', 'source'],
        ['Landing', 'sub-enya', '180116_001_m_enya_land-001', 'source'],
        ['Landing', 'sub-enyo'],
        ['Landing', 'sub-enyo', '180116_001_m_enyo_land-001']
    ]
    to
    [
        ['Landing', 'sub-anye', '180116_001_m_anye_land-001', 'source'],
        ['Landing', 'sub-enya', '180116_001_m_enya_land-001', 'source'],
    ]
    Checking for the longest chain with the same sub chain
    """

    main_list = sorted(nested_list_of_dir, key= lambda sublist: len(sublist))

    # TODO : optimize
    i=0
    j=1
    while i < len(main_list) -1:
        if j <= len(main_list) -1:
            if len(main_list[i]) <= len(main_list[j]):
                all_in = True
                for elmt in main_list[i]:
                    if elmt not in main_list[j]:
                        all_in = False

                if all_in:
                    for elmt_to_add in main_list[j]:
                        if elmt_to_add not in main_list[i]:
                            main_list[i].append(elmt_to_add)
                    main_list.pop(j)

                else:
                    if j < len(main_list) - 1:
                        j+=1
                    else:
                        i +=1
                        j =i+1
            else:
                i+=1
                j=i+1
        else:
            break
    return main_list

def create_path(directory):
    """
    New function to get the path given in arg
    to create a list of path .
    """
    list_of_dir=[]
    last = directory.split('/').pop()# take the last folder pass in arg so tests/ds007/data/Landing -> Landing
    path = pathlib.PurePath(directory)
    sub=directory.split(path.name)[0]# take evrything befor last tests/ds007/data/Landing -> tests/ds007/data
    for root,dirs,_ in os.walk(directory):
        for d in dirs:
                list_of_dir.append((os.path.join(root,d).replace(sub,"")))
                 # substract sub to all path : tests/ds007/data/Landing/sub-anye/180116_001_m_enya_land-001 -> Landing/sub-anye/180116_001_m_enya_land-001
    nested_list_of_dir =[]

    for each in list_of_dir:
            nested_list_of_dir.append((each.split(os.sep)))

    nested_list_of_dir_parsed=parse_all_path(nested_list_of_dir)
    final_list=parse_all_path(nested_list_of_dir_parsed)
    return final_list


def is_AnDO_R(subpath,level,validate):
    """
    Check if file path adheres to AnDO.
    Main method of the validator. uses other class methods for checking
    different aspects of the directory path.

    :param names:
     """
    if level < len(subpath):
        if  level == 0 :

            validate.append(is_experiment(subpath[level]))
            is_AnDO_R(subpath,level+1,validate)
        if  level == 1 :

            validate.append(is_subject(subpath[level]))
            is_AnDO_R(subpath,level+1,validate)
        if  level == 2 :

            validate.append(is_session(subpath[level]))
            is_AnDO_R(subpath,level+1,validate)
        if  level == 3 :

            validate.append(is_source(subpath[level]))
    return validate

def is_AnDO(directory):
    """
    Check if file path adheres to AnDO.
    Main method of the validator. uses other class methods for checking
    different aspects of the directory path.

    :param names:
    """
    validate=[]
    names= create_path(directory)
    for item in names:
        is_AnDO_R(item,0,validate)

    return(all(validate))

def is_AnDO_verbose(directory):
    """
    Call the function is_AnDO_verbose_Format on every path in the list

    :param names:
    """
    validate=[]
    names= create_path(directory)
    for item in names:
        validate.append(is_AnDO_verbose_Format(item))

    return(any(validate))


def is_AnDO_verbose_Format(names):
    """
    Check if file path adheres to AnDO.
    Main method of the validator. uses other class methods for checking
    different aspects of the directory path.

    :param names: list of names founds in the path
    """

    bool_error = 0
    #only error that exit without checking other folder
    if is_experiment(names[0]):
            bool_error = 0
    else:
        try:
            raise ExperimentError(names)
        except ExperimentError as e:
            print(e.strerror)
            bool_error = 1
            exit(1)
    if is_session(names):
        bool_error = 0
    else:
        try:
            raise SessionError(names)
        except SessionError as e:
            print(e.strerror)
            bool_error = 1
    if is_subject(names):
        bool_error = 0
    else:
        try:
            raise SubError(names)
        except SubError as e:
            print(e.strerror)
            bool_error = 1
    if is_source(names):
        bool_error = 0
    else:
        try:
            if(len(names)<=3):
                raise SourceNotFound(names)
            else:
                raise SourceError(names)
        except (SourceError, SourceNotFound) as e:
            print(e.strerror)
            bool_error = 1

    return bool_error


def is_experiment(names):
    """
    Check names follows experiment rules

    :param names: list of names founds in the path
    """

    regexps = get_regular_expressions(dir_rules + 'experiment_rules.json')
    conditions = []

    if type(names) == str:

        conditions.append([re.compile(x).search(names) is not None
                          for x in regexps])
    elif type(names) == list:

        for word in names:
            conditions.append([re.compile(x).search(word) is not None
                            for x in regexps])

        # print(flatten(conditions))

    return any(flatten(conditions))

def is_session(names):
    """
    Check names follows session rules

    :param names: list of names founds in the path
    """

    regexps = get_regular_expressions(dir_rules + 'session_rules.json')
    conditions = []
    if type(names) == str:
           conditions.append([re.compile(x).search(names) is not None
                          for x in regexps])
    else:
        for word in names:
            conditions.append([re.compile(x).search(word) is not None
                            for x in regexps])

        # print(flatten(conditions))

    return any(flatten(conditions))


def is_subject(names):
    """
    Check names follows subject rules

    :param names: list of names founds in the path
    """

    regexps = get_regular_expressions(dir_rules + 'subject_rules.json')
    conditions = []
    if type(names) == str:
           conditions.append([re.compile(x).search(names) is not None
                          for x in regexps])
    else:
        for word in names:
            conditions.append([re.compile(x).search(word) is not None
                            for x in regexps])

        #  print(flatten(conditions))

    return any(flatten(conditions))


def is_source(names):
    """
    Check names follows source rules

    :param names: list of names founds in the path
    """

    regexps = get_regular_expressions(dir_rules + 'source_rules.json')
    conditions = []
    if type(names) == str:
           conditions.append([re.compile(x).search(names) is not None
                          for x in regexps])
    else:
        for word in names:
            conditions.append([re.compile(x).search(word) is not None
                            for x in regexps])

        #  print(flatten(conditions))

    return any(flatten(conditions))


def get_regular_expressions(fileName):
    '''
    https://github.com/bids-standard/bids-validator/tree/master/bids-validator/

    using function to read regex in rule files

    '''

    regexps = []

    with open(fileName, 'r') as f:
        rules = json.load(f)

    for key in list(rules.keys()):
        rule = rules[key]

        regexp = rule['regexp']

        if 'tokens' in rule:
            tokens = rule['tokens']

            for token in list(tokens):
                regexp = regexp.replace(token, '|'.join(tokens[token]))

        regexps.append(regexp)

    return regexps


def flatten(seq):
    """
    Format list the proper way
    example:
    [[x],[y],[z]]--->[x,y,z]
    :param seq: list to format
    """
    list_flaten = []
    for elt in seq:
        t = type(elt)
        if t is tuple or t is list:
            for elt2 in flatten(elt):
                list_flaten.append(elt2)
        else:
            list_flaten.append(elt)
    return list_flaten