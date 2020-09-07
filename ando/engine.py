# File: engine.py
# Project: ando
# File Created: Tuesday, 30th June 2020 10:50:05 am
# Author: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Last Modified: Thursday, 2nd July 2020 1:32:33 pm
# Modified By: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Copyright - 2020 MIT, Institue de neurosciences de la Timone

# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import re
import pathlib
from ando.error import ExperimentError, SourceError, SourceNotFound, \
    SessionError, SubjectError, MetaDataError, DerivativeDataError, \
    RawDataError


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

    def _test_is_included(my_list_of_lists, list_elem):
        for my_list_elem in my_list_of_lists:
            if all([val[0] == val[1] for val in zip(my_list_elem,
                   list_elem)]):
                return True

        return False

    def _merge_duplicates(my_list_of_lists, max_length=3):
        """Transform this
        [
            ['Landing', 'sub-anye', '180116_001_m_anye_land-001', 'source']
            ['Landing', 'sub-anye', '180116_001_m_anye_land-001', 'metadata']
            ['Landing', 'sub-anye', '180116_001_m_anye_land-001', 'rawdata']
            ['Landing', 'sub-anye', '180116_001_m_anye_land-001','derivatives']
        ]
        to
        [
            [
                'Landing', 'sub-anye',
                '180116_001_m_anye_land-001',
                'rawdata',
                'metadata',
                'derivatives',
                'source'
            ]
        ]

        Args:
            my_list_of_lists ([list]): [list of path to process]
            max_length (int, optional): [number of folder in session directory
            coresponding torawdata metadata derivatives and sources].
            Defaults to 3.

        Returns:
            [list]: [list of concatenate sub folder at the end of the list ]

        todo:
            This might have to be re-implemented more efficiently.
        """
        merged_list = []
        for my_list_elem in my_list_of_lists:
            simil_list = []
            for my_list_elem2 in my_list_of_lists:
                if all([val[0] == val[1] for i, val in
                        enumerate(zip(my_list_elem, my_list_elem2))
                        if i < max_length]):

                    simil_list.append(my_list_elem2)

            if len(simil_list) > 1:
                new_list = simil_list[0][:max_length]
                for remain_list in simil_list:
                    new_list.append(remain_list[max_length])
                merged_list.append(new_list)

            else:
                merged_list.append(simil_list[0])

        return merged_list

    new_list_of_lists = []
    for list_elem in sorted(nested_list_of_dir,
                            key=lambda sublist: len(sublist), reverse=True):
        if not _test_is_included(new_list_of_lists, list_elem):
            new_list_of_lists.append(list_elem)
    # Removing duplicate
    new_list_of_lists = _merge_duplicates(new_list_of_lists)
    unique_data = [list(x) for x in set(tuple(x)for x in new_list_of_lists)]
    return unique_data


def create_nested_list_of_path(directory):
    """
    Function that get the path given in arg
    to create a list of path as follow
    take the last element of the path and walks through to get every sub
    dir as follow:
    /home/garciaj/AnDOChecker/checker/tests/ds001/Data/Landing/
    to
    [['Landing', 'sub-enya', 'y180116-land-001', 'Sources']]

    """

    list_of_dir = []
    # take the last folder pass in arg: tests/ds007/data/Landing -> Landing

    path = pathlib.PurePath(directory)
    sub = directory.split(path.name)[0]

    # take everything before last tests/ds007/data/Landing -> tests/ds007/data

    for (root, dirs, _) in os.walk(directory):
        for d in dirs:
            list_of_dir.append(os.path.join(root, d).replace(sub, ''))
    nested_list_of_dir = []

    for each in list_of_dir:
        nested_list_of_dir.append(each.split(os.sep))
    nested_list_of_dir_parsed = parse_all_path(nested_list_of_dir)
    return nested_list_of_dir_parsed


def is_AnDO_R(subpath, level, validate):
    """

    Check if file path adheres to AnDO.
    Main method of the validator. uses other class methods for checking
    different aspects of the directory path.


    Args:
        subpath ([list]): [list of names]
        level ([int]): [level of the folder , 0 : experiment, 1 : subject ...]
        validate ([list]): [list of boolean corresponding of each level]

    Returns:
        [list]: [validate : list of boolean corresponding of each level]
    """

    if level < len(subpath):
        if level == 0:
            validate.append(is_experiment(subpath[level]))
            is_AnDO_R(subpath, level + 1, validate)
        if level == 1:
            validate.append(is_subject(subpath[level]))
            is_AnDO_R(subpath, level + 1, validate)
        if level == 2:
            validate.append(is_session(subpath[level]))
            is_AnDO_R(subpath, level + 1, validate)
        if level == 3:
            validate.append(is_source(subpath[level]))
            is_AnDO_R(subpath, level + 1, validate)
        if level == 4:
            validate.append(is_metadata(subpath[level]))
            is_AnDO_R(subpath, level + 1, validate)
        if level == 5:
            validate.append(is_derivatives(subpath[level]))
            is_AnDO_R(subpath, level + 1, validate)
        if level == 6:
            validate.append(is_rawdata(subpath[level]))
            is_AnDO_R(subpath, level + 1, validate)
    elif level < 7:
        validate.append(False)
    return validate


def is_AnDO(directory):
    """

    Check if file path adheres to AnDO.
    Main method of the validator. uses other class methods for checking
    different aspects of the directory path.


    Args:
        directory ([str]): [names of the directory to check]

    Returns:
        [bool]: [does the directory adheres to the ando specification]
    """

    validate = []
    names = create_nested_list_of_path(directory)

    for item in names:
        is_AnDO_R(item, 0, validate)

    return all(validate)


def is_AnDO_verbose(directory):
    """
    Call the function is_AnDO_verbose_Format on every path in the list


    Args:
        directory ([str]): [names of the directory to check]

    Returns:
        [bool]: [does the directory adheres to the ando specification]
    """

    validate = []
    names = create_nested_list_of_path(directory)

    for item in names:
        validate.append(is_AnDO_verbose_Format(item))
    
    return any(validate)


def is_AnDO_verbose_Format(names):
    """
    Check if file path adheres to AnDO.
    Main method of the validator. uses other class methods for checking
    different aspects of the directory path.

    Args:
        names ([list]): [names to check]

    Raises:
        ExperimentError: raised if it doesn't the experiment rules
        SessionError: raised if it doesn't the session rules
        SubjectError: raised if it doesn't the subject rules
        SourceError: raised if it doesn't the source rules
        RawDataError: raised if it doesn't the rawdata rules
        DerivativeDataError: raised if it doesn't the derivatives rules
        MetaDataError: raised if it doesn't the metadata rules
        SourceNotFound: raised if it doesn't the source rules

    Returns:
        [bool]: true if error is found else false
        [out]: feedback for the web api
    """

    bool_error = 0
    out = list()
    # only error that exit without checking other folder

    if is_experiment(names[0]):
        bool_error = 0
    else:
        try:
            raise ExperimentError(names)
        except ExperimentError as e:
            print(e.strerror)
            out.append(e.strout)
            bool_error = 1
            return bool_error, out

    if is_session(names):
        bool_error = 0
    else:
        try:
            raise SessionError(names)
        except SessionError as e:
            print(e.strerror)
            out.append(e.strout)
            bool_error = 1
    if is_subject(names):
        bool_error = 0
    else:
        try:
            raise SubjectError(names)
        except SubjectError as e:
            print(e.strerror)
            out.append(e.strout)
            bool_error = 1
    if len(names) == 7:

        if is_source(names):
            bool_error = 0
        else:
            try:
                raise SourceError(names)
            except SourceError as e:
                print(e.strerror)
                out.append(e.strout)
                bool_error = 1
        if is_rawdata(names):
            bool_error = 0
        else:
            try:
                raise RawDataError(names)
            except RawDataError as e:
                print(e.strerror)
                out.append(e.strout)
                bool_error = 1
        if is_derivatives(names):
            bool_error = 0
        else:
            try:
                raise DerivativeDataError(names)
            except DerivativeDataError as e:
                print(e.strerror)
                out.append(e.strout)
                bool_error = 1
        if is_metadata(names):
            bool_error = 0
        else:
            try:
                raise MetaDataError(names)
            except MetaDataError as e:
                print(e.strerror)
                out.append(e.strout)
                bool_error = 1

    else:

        if not is_metadata(names):
            try:
                raise MetaDataError(names)
            except MetaDataError as e:
                print(e.strerror)
                out.append(e.strout)
                bool_error = 1
        if not is_rawdata(names):
            try:
                raise RawDataError(names)
            except RawDataError as e:
                print(e.strerror)
                out.append(e.strout)
                bool_error = 1
        if not is_derivatives(names):
            try:
                raise DerivativeDataError(names)
            except DerivativeDataError as e:
                print(e.strerror)
                out.append(e.strout)
                bool_error = 1
        if not is_source(names):
            try:
                raise SourceNotFound(names)
            except SourceNotFound as e:
                print(e.strerror)
                out.append(e.strout)
                bool_error = 1
    if len(out) >1 :
        return bool_error, out
    else:
        return bool_error


def is_experiment(names):
    """[Check names follows experiment rules]

    Args:
        names ([str]): [names founds in the path]

    Returns:
        [type]: [true or false ]
    """

    regexps = get_regular_expressions(dir_rules
                                      + 'experiment_rules.json')
    conditions = []
    if type(names) == str:

        conditions.append([re.compile(x).search(names) is not None
                          for x in regexps])
    elif type(names) == list:

        for word in names:
            conditions.append([re.compile(x).search(word) is not None
                              for x in regexps])

    return any(flatten(conditions))


def is_rawdata(names):
    """[Check names follows rawdata rules]

    Args:
        names ([str]): [names founds in the path]

    Returns:
        [bool]: [true or false ]
    """

    regexps = get_regular_expressions(dir_rules
                                      + 'rawdata_rules.json')
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


def is_metadata(names):
    """[Check names follows metadata rules]

    Args:
        names ([str]): [names founds in the path]

    Returns:
        [bool]: [true or false ]
    """

    regexps = get_regular_expressions(dir_rules
                                      + 'metadata_rules.json')
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


def is_derivatives(names):
    """[Check names follows derivatives rules]

    Args:
        names ([str]): [names founds in the path]

    Returns:
        [bool]: [true or false ]
    """

    regexps = get_regular_expressions(dir_rules
                                      + 'derivatives_rules.json')
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
    """[Check names follows session rules]

    Args:
        names ([str]): [names founds in the path]

    Returns:
        [bool]: [true or false ]
    """

    regexps = get_regular_expressions(dir_rules + 'session_rules.json')
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


def is_subject(names):
    """[Check names follows subject rules]

    Args:
        names ([str]): [names founds in the path]

    Returns:
        [bool]: [true or false ]
    """

    regexps = get_regular_expressions(dir_rules + 'subject_rules.json')
    conditions = []
    if type(names) == str:
        conditions.append([re.compile(x).search(names) is not None
                          for x in regexps])
    elif type(names) == list:

        for word in names:
            conditions.append([re.compile(x).search(word) is not None
                              for x in regexps])

        #  print(flatten(conditions))

    return any(flatten(conditions))


def is_source(names):
    """[Check names follows sources rules]

    Args:
        names ([str]): [names founds in the path]

    Returns:
        [bool]: [true or false ]
    """

    regexps = get_regular_expressions(dir_rules + 'source_rules.json')
    conditions = []
    if type(names) == str:
        conditions.append([re.compile(x).search(names) is not None
                          for x in regexps])
    elif type(names) == list:

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
