# File: error.py
# Project: ando
# File Created: Tuesday, 30th June 2020 10:50:05 am
# Author: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Last Modified: Thursday, 2nd July 2020 1:31:40 pm
# Modified By: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Copyright - 2020 MIT, Institut de Neurosciences de la Timone,CNRS


# !/usr/bin/python
# -*- coding: utf-8 -*-

"""[Exception raised  when the name does not follow the AnDO specification

    self.strerror : corresponding to the output in CLI mod
    self.strout : corresponding to the output of web mod by returning
     html

    ]
"""

# flake8: noqa: E501
class ExperimentError(Exception):
    """
    Exception raised when the name does not follow the AnDO specification


    Args:
        Exception ([Exception]): [raised in engine.py]
    """

    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 1 error [experiment folder] at : ' + names[0] + '\n' \
            + '  It should follow the exp-NAME format, where:\n' \
            + '    - NAME is a string designating the name of your experiment\n'
        self.strout = '<div class="card"><div class="card-header bg-danger text-white">' \
                + '1 error found at experiment folder level.  </div><div class="card-body"> ' \
                + '<h4 class="em-header clearfix"><strong class="em-header pull-left">Error 4 type ' \
                + "[Experiment folder error] at : "+names[0]+" </strong></h4><br><b><i>" \
                + '</b></i>It should follow the exp-NAME format, where:  '\
                + ' <ul><li> NAME is a string designating the name of your experiment</li><ul></div></div>'

class SubjectError(Exception):
    """Exception raised when the name does not follow the AnDO specification of subject level


    Args:
        Exception ([Exception]): [raised in engine.py]
    """

    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 2 error [subject folder] at : ' + names[1] + '\n' \
            + '  It should follow the sub-ID format, where:\n' \
            + '    - ID is a string designating the IDentifier of the animal\n'
        self.strout = '<div class="card"><div class="card-header bg-danger text-white">' \
                + '1 error found at subject folder level.  </div><div class="card-body"> ' \
                + '<h4 class="em-header clearfix"><strong class="em-header pull-left">Error 4 type ' \
                + "[Subject folder error] at : "+names[0]+" </strong></h4><br><b><i>" \
                + '</b></i>It should follow the sub-ID format, where:  '\
                + ' <ul><li> ID is a string designating the IDentifier of the animal</li><ul></div></div>'

class SessionError(Exception):
    """Exception raised when the name does not follow the AnDO specification of session level


    Args:
        Exception ([Exception]): [raised in engine.py]
    """

    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 3 error [session folder] at : ' + names[2] + '\n' \
            + '  It should follow the ses-YYYYMMDD_XXX_BBBB format, where:\n' \
            + '    - ‘ses-’ is an imposed prefix\n' \
            + '    - ‘YYYYMMDD’ is the date of the session (8 digits, for instance 20180430 for April 30, 2018)\n' \
            + '    - XXX is the number of the session acquired on that date (3 digits, for instance 001 for the first session)\n' \
            + '    - BBBB is a string freely usable by the research group / user\n' \
            + '      (is a string freely usable by the research group / user (for instance to add extra info on \n' \
            + '      the version of the experimental protocol, on the type of preparation, on the user-friendly name of the animal etc.);\n' \
            + '      this string cannot contain the underscore character.\n'
        self.strout = '<div class="card"><div class="card-header bg-danger text-white">' \
                + '1 error found at Session folder level.  </div><div class="card-body"> ' \
                + '<h4 class="em-header clearfix"><strong class="em-header pull-left">Error 4 type ' \
                + "[session folder error] at : "+names[2]+" </strong></h4><br><b><i>" \
                + '</b></i>It should follow the ses-YYYYMMDD_XXX_BBBB format format, where:  '\
                + ' <ul><li>"ses-" is an imposed prefix</li>'\
                + '<li>"YYYYMMDD" is the date of the session (8 digits, for instance 20180430 for April 30, 2018)</li>'\
                + '<li>"BBBB" is a string freely usable by the research group / user , this string cannot contain the underscore character.</li>'\
                + '<ul></div></div>'

class EphysError(Exception):
    """Exception raised when the name does not follow the AnDO specification on the ephy level


    Args:
        Exception ([Exception]): [raised in engine.py]
    """

    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 3 error [Ephys folder] at : ' + names[2] + '\n' \
            + '  Ephys folder is missing or does not follow the AnDO specification rules:\n' \
            + '    - Ephys \n'
        self.strout = '<div class="card"><div class="card-header bg-danger text-white">' \
                + '1 error found at session folder level.  </div><div class="card-body"> ' \
                + '<h4 class="em-header clearfix"><strong class="em-header pull-left">Error 4 type ' \
                + "[Subject ephys error] at : "+names[2]+" </strong></h4><br><b><i>" \
                + '</b></i>Ephys folder is missing or does not follow the AnDO specification rules:  '\
                + ' <ul><li> ephys</li><ul></div></div>'
