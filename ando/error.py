#!/usr/bin/python
# -*- coding: utf-8 -*-


class ExperimentError(Exception):

    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 1 error [experiment folder] at : ' + names[0] + '\n' \
            + '  It should follow the exp-NAME format, where:\n' \
            + '    - NAME is a string designating the name of your experiment\n'

class SubjectError(Exception):

    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 2 error [subject folder] at : ' + names[1] + '\n' \
            + '  It should follow the sub-ID format, where:\n' \
            + '    - ID is a string designating the IDentifier of the animal\n'

class SessionError(Exception):

    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 3 error [session folder] at : ' + names[2] + '\n' \
            + '  It should follow the ses-YYYYMMDD_XXX_BBBB format, where:\n' \
            + '    - ‘ses-’ is an imposed prefix\n' \
            + '    - ‘YYYYMMDD’ is the date of the session (6 digits, for instance 20180430 for April 30, 2018)\n' \
            + '    - XXX is the number of the session acquired on that date (3 digits, for instance 001 for the first session)\n' \
            + '    - BBBB is a string freely usable by the research group / user\n' \
            + '      (is a string freely usable by the research group / user (for instance to add extra info on \n' \
            + '      the version of the experimental protocol, on the type of preparation, on the user-friendly name of the animal etc.);\n' \
            + '      this string cannot contain the underscore character.\n'


class SourceError(Exception):

    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 4 error [source folder] at : ' + names[2] + '\n' \
            + '  A single folder called source is authorized within a session folder\n'
class RawDataError(Exception):

    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 4 error [rawdata folder missing]\n' \
            + '  A folder called rawdata should be present in the session folder ' + names[2] + '\n'
class MetaDataError(Exception):

    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 4 error [metadata folder missing]\n' \
            + '  A folder called metadata should be present in the session folder ' + names[2] + '\n'
class DerivativeDataError(Exception):

    def __init__(self, arg):
        names = arg
        self.strerror ='Level 4 error [derivatives folder missing]\n' \
            + '  A folder called derivatives should be present in the session folder ' + names[2] + '\n'

class SourceNotFound(Exception):

    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 4 error [source folder missing]\n' \
            + '  A folder called source should be present in the session folder ' + names[2] + '\n'

