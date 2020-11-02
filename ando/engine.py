# File: engine.py
# Project: ando
# File Created: Tuesday, 30th June 2020 10:50:05 am
# Author: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Last Modified: Thursday, 2nd July 2020 1:32:33 pm
# Modified By: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Copyright - 2020 MIT, Institut de Neurosciences de la Timone,CNRS

# !/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import re
import pathlib
from ando.error import ExperimentError, \
    SessionError, SubjectError, MetaDataError, DerivativeDataError, \
    RawDataError


dir_rules = os.path.join(os.path.dirname(__file__)) + '/rules/'


def parse_all_path(nested_list_of_dir):
    """
    Transforms this
    [
        ['Landing', 'sub-anye', '180116_001_m_anye_land-001', 'source'],
        ['Landing', 'sub-enya', '180116_001_m_enya_land-001', 'source'],
        ['Landing', 'sub-enyo'],
        ['Landing', 'sub-enyo', '180116_001_m_enyo_land-001']
    ]
    into
    [
        ['Landing', 'sub-anye', '180116_001_m_anye_land-001', 'source'],
        ['Landing', 'sub-enya', '180116_001_m_enya_land-001', 'source'],
    ]
    Checking for the longest chain with the same sub-chain
    """

    def _test_is_included(my_list_of_lists, list_elem):
        for my_list_elem in my_list_of_lists:
            if all([val[0] == val[1] for val in zip(my_list_elem,
                   list_elem)]):
                return True

        return False

    def _merge_duplicates(my_list_of_lists, max_length=3):
        """
        Transform this
        [

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
            ]
        ]

        Args:
            my_list_of_lists ([list]): [list of path to process]
            max_length (int, optional): [number of folder in session directory
            coresponding to rawdata metadata derivatives and sources].
            Defaults to 3.

        Returns:
            [list]: [list of concatenate sub folder at the end of the list ]

        todo:
            This might have to be re-implemented more efficiently.
            At the moment this is the best solution so far to get feedbacks on where does the error happen.
            if we use the BIDS implementation we can just say if the Directory follows the AnDO specs .

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


def is_AnDO(directory, verbose):
    """

    Check if file path adhere to AnDO.
    Main method of the validator. uses other class methods for checking
    different aspects of the directory path.


    Args:
        directory ([str]): [names of the directory to check]

    Returns:
        [bool]: [does the directory adhere to the ando specification]
    """

    validate = []
    names = create_nested_list_of_path(directory)
    for item in names:
        validate.append(check_Path(item, verbose))
    return any(validate)


def check_Path(names, verbose):
    """
    Check if file path adhere to AnDO.
    Main method of the validator. uses other class methods for checking
    different aspects of the directory path.

    Args:
        names ([list]): [names to check]

    Raises:
        ExperimentError: raised if it does not  respect the experiment rules
        SessionError: raised if it does not respect  the session rules
        SubjectError: raised if it does not respect the subject rules
        RawDataError: raised if it does not respect the rawdata rules
        DerivativeDataError: raised if it does not respect the derivatives rules
        MetaDataError: raised if it does not respect the metadata rules

    Returns:
        [bool]: true if error is found else false
        [out]: feedback for the web page
    """
    bool_error = 0
    out = list()
    # only error that exit without checking other folder
    if not is_experiment(names[0]):
        try:
            raise ExperimentError(names)
        except ExperimentError as e:
            if verbose is True:
                print(e.strerror)
            out.append(e.strout)
            bool_error = 1
            return bool_error, out

    if not is_session(names):
        try:
            raise SessionError(names)
        except SessionError as e:
            if verbose is True:
                print(e.strerror)
            out.append(e.strout)
            bool_error = 1
    if not is_subject(names):
        try:
            raise SubjectError(names)
        except SubjectError as e:
            if verbose is True:
                print(e.strerror)
            out.append(e.strout)
            bool_error = 1

    if len(names) == 6:

        if not is_rawdata(names):
            try:
                raise RawDataError(names)
            except RawDataError as e:
                if verbose is True:
                    print(e.strerror)
                out.append(e.strout)
                bool_error = 1
        if not is_derivatives(names):
            try:
                raise DerivativeDataError(names)
            except DerivativeDataError as e:
                if verbose is True:
                    print(e.strerror)
                out.append(e.strout)
                bool_error = 1
        if not is_metadata(names):
            try:
                raise MetaDataError(names)
            except MetaDataError as e:
                if verbose is True:
                    print(e.strerror)
                out.append(e.strout)
                bool_error = 1

    else:

        if not is_metadata(names):
            try:
                raise MetaDataError(names)
            except MetaDataError as e:
                if verbose is True:
                    print(e.strerror)
                out.append(e.strout)
                bool_error = 1
        if not is_rawdata(names):
            try:
                raise RawDataError(names)
            except RawDataError as e:
                if verbose is True:
                    print(e.strerror)
                out.append(e.strout)
                bool_error = 1
        if not is_derivatives(names):
            try:
                raise DerivativeDataError(names)
            except DerivativeDataError as e:
                if verbose is True:
                    print(e.strerror)
                out.append(e.strout)
                bool_error = 1
    if len(out) >= 1:
        return bool_error, out
    else:
        return bool_error


def is_experiment(names):
    """[Check names follows experiment rules]

    Args:
        names ([str]): [names founds in the path]

    Returns:
        [type]: [True or false ]
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
