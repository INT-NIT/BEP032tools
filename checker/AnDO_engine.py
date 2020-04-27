#!/usr/bin/python
# -*- coding: utf-8 -*-

import os
import json
import re
from AnDO_Error import (
    SourceError,
    DateError,
    SubError)

dir_rules = os.path.join(os.path.dirname(__file__)) + '/rules/'


def is_AnDO(names):
    """
    Check if file path adheres to BIDS.
    Main method of the validator. uses other class methods for checking
    different aspects of the directory path.

    :param names: 
    """
    validate = []
    validate.append(is_session(names))
    validate.append(is_source(names))
    validate.append(is_subject(names))

    return all(validate)


def is_AnDO_verbose(names):
    """
    Check if file path adheres to BIDS.
    Main method of the validator. uses other class methods for checking
    different aspects of the directory path.
    
    :param names: list of names founds in the path
    """
    bool_error = 0
    if is_session(names):
        bool_error = 0
    else:
        try:
            raise SessionError(names)
        except DateError as e:
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
            raise SourceError(names)
        except SourceError as e:
            print(e.strerror)
            bool_error = 1

    return bool_error


def is_session(names):
    """
    Check names follows session rules 
    
    :param names: list of names founds in the path
    """

    regexps = get_regular_expressions(dir_rules + 'session_rules.json')
    conditions = []
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
    exemple:
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
