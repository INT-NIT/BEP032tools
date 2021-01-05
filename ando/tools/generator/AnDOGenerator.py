from pathlib import Path
import datetime
import warnings
import argparse
import os
import re

try:
    import pandas as pd
    HAVE_PANDAS = True
except ImportError:
    HAVE_PANDAS = False

import ando
from ando.engine import check_Path, get_regular_expressions

# mapping of human readable labels to AnDO session parameters
LABEL_TRANSLATOR = {'expName': ['experiment_name', 'experiment_names', 'experiments_name'],
                    'guid': ['subName', 'subject_name', 'subject_names', 'subjects_names'],
                    'date': ['date', 'dates'],
                    'year': ['year', 'years'],
                    'month': ['month', 'months'],
                    'day': ['day', 'days'],
                    'sesNumber': ['session_number', 'session_numbers', 'sessions_numbers'],
                    'customSesField': ['customField', 'comment', 'comments']}

ESSENTIAL_PARAMS = ['expName', 'guid', 'date', 'sesNumber']

LABEL_MAPPING = {label: param for param, labels in LABEL_TRANSLATOR.items() for label in labels}

MANDATORY_SUBFOLDER = "ephys"
class AnDOSesID:

    def __init__(self, sesID=None, date=None, sesNumber=None, customSesField=None):
        """
        Representation of an AnDO session ID, as defined in `ando/rules/session_rules.json`

        Parameters
        ----------
        sesID: (str)
            complete session identifier, e.g. `20000101_001_test`
        date: (str or datetime)
            date subinfo of session ID, e.g. `20000101`
        sesNumber: (str)
            session number subinfo of session ID, e.g. `001`
        customSesField: (str)
            custom session field subinfo of session ID
        """

        # Inform user if insufficient or duplicate information is provided
        if sesID is not None:
            if (date is None) or (sesNumber is None) or (customSesField is None):
                warnings.warn(f'Using sesID ({sesID}) in favour alternative parameters date, '
                              f'sesNumber and customSesField')
        elif (date is None) or (sesNumber is None):
            raise ValueError('Incomplete information for generating a session ID.')

        if sesID is None:
            self.sesNumber = sesNumber

            # Define default value for custom session field
            if customSesField is None:
                self.customSesField = ''
            else:
                self.customSesField = customSesField

            if isinstance(date, datetime.datetime):
                self.date = date.strftime('%Y%m%d')
            else:
                # TODO: Check this has the right fomat
                self.date = date

        # if only sesID is provided, we use the session regex to extract infos
        else:
            rules_dir = os.path.join(os.path.dirname(ando.__file__), 'rules')
            regexps = get_regular_expressions(os.path.join(rules_dir, 'session_rules.json'))
            for regexp in regexps:
                match = re.match(regexp, f'ses-{sesID}')
                if match:
                    self.date = match.groupdict()['date']
                    self.sesNumber = match.groupdict()['sesNumber']
                    self.customSesField = match.groupdict()['customSesField']

    def __str__(self):
        return f'{self.date}_{self.sesNumber}_{self.customSesField}'


class AnDOSession:

    def __init__(self, expName=None, guid=None, sesID=None, date=None, sesNumber=None,
                 customSesField=None):
        """
        Representation of all AnDO Session, as specified by the AnDOChecker

        Parameters
        ----------
        expName: (str)
            The name of the experiment
        guid: (str)
            Global unique identifier of the subject
        sesID: (str)
            complete session identifier, e.g. `20000101_001_test`
        date: (str or datetime)
            date subinfo of session ID, e.g. `20000101`
        sesNumber: (str)
            session number subinfo of session ID, e.g. `001`
        customSesField: (str)
            custom session field subinfo of session ID
        """

        if expName is None:
            raise ValueError('The experiment name (expName) can not be `None`.')
        if guid is None:
            raise ValueError('The global unique identifier (guid) can not be `None`.')

        self.expName = expName
        self.guid = guid
        self.sesID = AnDOSesID(sesID=sesID,
                               date=date,
                               sesNumber=sesNumber,
                               customSesField=customSesField)

    def get_session_path(self):
        path = os.path.join(f'exp-{self.expName}',
                            f'sub-{self.guid}',
                            f'ses-{self.sesID}',
                            )
        return path

    def get_all_folder_paths(self):
        paths = []
        session = self.get_session_path()
        for datafolder in [MANDATORY_SUBFOLDER]:
            paths.append(os.path.join(session, datafolder))

        # validate generated paths with AnDO
        combined_paths = []
        for path in paths:
            for folder in path.split(os.path.sep):
                if folder not in combined_paths:
                    combined_paths.append(folder)
        assert not check_Path(combined_paths, verbose=False)[0], \
            'Error in AnDO path generation. Generated paths are not consistent with AnDO ' \
            'specifications'
        return paths

    def generate_folders(self, basedir, clean=False):
        session_folders = self.get_all_folder_paths()

        complete_paths = [os.path.join(basedir, path) for path in session_folders]

        # remove existing folders if clean is True
        for path in complete_paths:
            if clean and os.path.exists(path):
                warnings.warn(f'Replacing existing folder: {path}')
                os.remove(path)

        # create all folders
        for path in complete_paths:
            Path(path).mkdir(parents=True)


def extract_structure_from_csv(csv_file):

    if not HAVE_PANDAS:
        raise ImportError('Extraction of ando structure from csv requires pandas.')

    df = pd.read_csv(csv_file)

    # ensure all fields contain information
    if df.isnull().values.any():
        raise ValueError(f'Csv file contains empty cells.')

    # standardizing column labels
    df = df.rename(columns=LABEL_MAPPING)

    # Formatting month, day and session_number
    df["month"] = df.month.map("{:02}".format)
    df["day"] = df.day.map("{:02}".format)
    df["sesNumber"] = df.sesNumber.map("{:03}".format)

    # unifying data representation in favour of datetime object
    if "date" not in df.columns:
        df["date"] = pd.to_datetime(df.loc[:, ["year", "month", "day"]])
        df = df.drop(["year", "month", "day"], axis=1)
    else:
        df["date"] = pd.to_datetime(df.loc[:, "date"])

    # Check is the header contains all required names
    if not set(ESSENTIAL_PARAMS).issubset(df.columns):
        raise ValueError(f'Csv file ({csv_file}) does not contain required information '
                         f'({ESSENTIAL_PARAMS}). Accepted column names are {LABEL_MAPPING}')

    return df


def generate_Struct(csv_file, pathToDir):
    f"""
    Create structure with csv file given in argument
    This file must contain a header row specifying the provided data. Accepted titles are
    
    {LABEL_MAPPING}
    Essential information of the following attributes needs to be present
    {ESSENTIAL_PARAMS}

    Args:
        csv_file ([csv file ]): [Csv file that contains a list of directories to create ]
        pathToDir ([Path to directory]): [Path to directory where the directories will be created]
    """

    df = extract_structure_from_csv(csv_file)

    for session_kwargs in df.to_dict('index').values():
        session = AnDOSession(**session_kwargs)
        session.generate_folders(pathToDir)


def main():
    """
    usage: AnDOGenerator.py [-h] pathToCsv pathToDir

    positional arguments:
    pathToCsv   Path to your folder
    pathToDir   Path to your csv file

    optional arguments:
    -h, --help  show this help message and exit
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('pathToCsv', help='Path to your folder')
    parser.add_argument('pathToDir', help='Path to your csv file')

    # Create two argument groups

    args = parser.parse_args()

    # Check if directory exists
    if not os.path.isdir(args.pathToDir):
        print('Directory does not exist:', args.pathToDir)
        exit(1)
    generate_Struct(args.pathToCsv, args.pathToDir)


if __name__ == '__main__':
    main()
