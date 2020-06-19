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
            + '  It should follow the YYMMDD_XXX_A_UFID_BBBB format, where:\n' \
            + '    - YYMMDD is the date of the session (6 digits, for instance 200430 for April 30, 2020\n' \
            + '    - XXX is the number of the session acquired on that date (3 digits, for instance 001 for the first session)\n' \
            + '    - A is a single letter that designate the species of the animal (m for ???, o for ???, r for ???, s for ???)\n' \
            + '    - UFID is a string containing the User Friendly IDentifier of the animal\n' \
            + '    - BBBB is a string freely usable by the research group / user\n' \
            + '      (for instance to add extra info on the version of the experimental protocol, on the type of preparation etc.)\n'


class SourceError(Exception):

    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 4 error [source folder] at : ' + names[3] + '\n' \
            + '  A single folder called source is authorized within a session folder\n'

class SourceNotFound(Exception):

    def __init__(self, arg):
        names = arg
        self.strerror = 'Level 4 error [source folder missing]\n' \
            + '  A folder called source should be present in the session folder ' + names[2] + '\n'

