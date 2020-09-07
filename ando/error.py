# File: error.py
# Project: ando
# File Created: Tuesday, 30th June 2020 10:50:05 am
# Author: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Last Modified: Thursday, 2nd July 2020 1:31:40 pm
# Modified By: garcia.j (Jeremy.garcia@univ-amu.fr)
# -----
# Copyright - 2020 MIT, Institue de neurosciences de la Timone


# !/usr/bin/python
# -*- coding: utf-8 -*-

"""[Exception raise when the name doesn't follow the AnDO specification

    self.strerror : corresponding to the output in CLI mod
    self.strout : corresponding to the output of web mod by returning
     html

    ]
"""

# flake8: noqa: E501
class ExperimentError(Exception):
    """
    Exception raise when the name doesn't follow the AnDO specification


    Args:
        Exception ([Exception]): [raised in engine.py]
    """

    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 1 error [experiment folder] at : ' + names[0] + '\n' \
            + '  It should follow the exp-NAME format, where:\n' \
            + '    - NAME is a string designating the name of your experiment\n'
        self.strout = '<div class="card"><div class="card-header bg-danger text-white">' \
                + '1 error found at Source folder level.  </div><div class="card-body"> ' \
                + '<h4 class="em-header clearfix"><strong class="em-header pull-left">Error 4 type ' \
                + "[Experiment folder error] at : "+names[0]+" </strong></h4><br><b><i>" \
                + '</b></i>It should follow the exp-NAME format, where:  '\
                + ' <ul><li> NAME is a string designating the name of your experiment</li><ul></div></div>'

class SubjectError(Exception):
    """Exception raise when the name doesn't follow the AnDO specification of subject level


    Args:
        Exception ([Exception]): [raised in engine.py]
    """

    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 2 error [subject folder] at : ' + names[1] + '\n' \
            + '  It should follow the sub-ID format, where:\n' \
            + '    - ID is a string designating the IDentifier of the animal\n'
        self.strout = '<div class="card"><div class="card-header bg-danger text-white">' \
                + '1 error found at Source folder level.  </div><div class="card-body"> ' \
                + '<h4 class="em-header clearfix"><strong class="em-header pull-left">Error 4 type ' \
                + "[Subject folder error] at : "+names[0]+" </strong></h4><br><b><i>" \
                + '</b></i>It should follow the sub-ID format, where:  '\
                + ' <ul><li> ID is a string designating the IDentifier of the animal</li><ul></div></div>'

class SessionError(Exception):
    """Exception raise when the name doesn't follow the AnDO specification of session level


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
                + '1 error found at Source folder level.  </div><div class="card-body"> ' \
                + '<h4 class="em-header clearfix"><strong class="em-header pull-left">Error 4 type ' \
                + "[session folder error] at : "+names[2]+" </strong></h4><br><b><i>" \
                + '</b></i>It should follow the Session format, where:  '\
                + ' <ul><li>‘ses-’ is an imposed prefix</li>
                + '<li>‘YYYYMMDD’ is the date of the session (8 digits, for instance 20180430 for April 30, 2018)</li>'
                + '<li>BBBB is a string freely usable by the research group / user</li>
                + '<li>this string cannot contain the underscore character.</li><ul></div></div>'

class SourceError(Exception):
    """Exception raise when the name doesn't follow the AnDO specification of error level


    Args:
        Exception ([Exception]): [raised in engine.py]
    """

    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 4 error [source folder] at : ' + names[2] + '\n' \
            + '  A single folder called source is authorized within a session folder\n'

        self.strout = '<div class="card"><div class="card-header bg-danger text-white">' \
                + '1 error found at Source folder level.  </div><div class="card-body"> ' \
                + '<h4 class="em-header clearfix"><strong class="em-header pull-left">Error 4 type ' \
                + "[source folder error] at : "+names[2]+" </strong></h4><br><b><i>" \
                + '</b></i> A folder called  <i><b>"source" </i></b>'\
                + ' should be present in the session folder. OR does not follow specification</div></div>'
class RawDataError(Exception):
    """Exception raise when the name doesn't follow the AnDO specification of rawdata level


    Args:
        Exception ([Exception]): [raised in engine.py]
    """

    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 4 error [rawdata folder missing]\n' \
            + '  A folder called rawdata should be present in the session folder ' + names[2] + '\n'
        self.strout = '<div class="card"><div class="card-header bg-danger text-white">' \
                + '1 error found at Source folder level.  </div><div class="card-body"> ' \
                + '<h4 class="em-header clearfix"><strong class="em-header pull-left">Error 4 type ' \
                + "[rawdata folder error] at : "+names[2]+" </strong></h4><br><b><i>" \
                + '</b></i> A folder called  <i><b>"rawdata" </i></b>'\
                + ' should be present in the session folder.</div></div>'
class MetaDataError(Exception):
    """Exception raise when the name doesn't follow the AnDO specification of rawdata level


    Args:
        Exception ([Exception]): [raised in engine.py]
    """

    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 4 error [metadata folder missing]\n' \
            + '  A folder called metadata should be present in the session folder ' + names[2] + '\n'
        self.strout = '<div class="card"><div class="card-header bg-danger text-white">' \
                + '1 error found at Source folder level.  </div><div class="card-body"> ' \
                + '<h4 class="em-header clearfix"><strong class="em-header pull-left">Error 4 type ' \
                + "[metadata folder error] at : "+names[2]+" </strong></h4><br><b><i>" \
                + '</b></i> A folder called  <i><b>"metadata" </i></b>'\
                + ' should be present in the session folder.</div></div>'
class DerivativeDataError(Exception):
    """Exception raise when the name doesn't follow the AnDO specification of derivatives level


    Args:
        Exception ([Exception]): [raised in engine.py]
    """

    def __init__(self, arg):
        names = arg
        self.strerror ='Level 4 error [derivatives folder missing]\n' \
            + '  A folder called derivatives should be present in the session folder ' + names[2] + '\n'
        self.strout = '<div class="card"><div class="card-header bg-danger text-white">' \
                + '1 error found at Source folder level.  </div><div class="card-body"> ' \
                + '<h4 class="em-header clearfix"><strong class="em-header pull-left">Error 4 type ' \
                + "[derivatives folder error] at : "+names[2]+" </strong></h4><br><b><i>" \
                + '</b></i> A folder called  <i><b>"derivatives" </i></b>'\
                + ' should be present in the session folder.</div></div>'

class SourceNotFound(Exception):
    """Exception raise when the name doesn't follow the AnDO specification of source level


    Args:
        Exception ([Exception]): [raised in engine.py]
     """
    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 4 error [source folder missing]\n' \
            + '  A folder called source should be present in the session folder ' + names[2] + '\n'

        self.strout = '<div class="card"><div class="card-header bg-danger text-white">' \
            + '1 error found at Source folder level.  </div><div class="card-body"> ' \
            + '<h4 class="em-header clearfix"><strong class="em-header pull-left">Error 4 type ' \
            + "[Source folder error] at : "+names[2]+" </strong></h4><br><b><i>" \
            + '</b></i> A folder called  <i><b>"source" </i></b>'\
            + ' should be present in the session folder.</div></div>'

