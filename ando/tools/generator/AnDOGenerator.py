from pathlib import Path
import shutil
import warnings
import argparse
import os
import re


try:
    import pandas as pd
    HAVE_PANDAS = True
except ImportError:
    HAVE_PANDAS = False
from ando.AnDOChecker import build_rule_regexp
from ando.rulesStructured import RULES_SET
from ando.rulesStructured import DATA_EXTENSIONS
from ando.rulesStructured import METADATA_EXTENSIONS

METADATA_LEVELS = {i: r['authorized_metadata_files'] for i,r in enumerate(RULES_SET)}
METADATA_LEVEL_BY_NAME = {build_rule_regexp(v)[0]: k for k, values in METADATA_LEVELS.items() for v in values}

# TODO: These can be extracted from the AnDOData init definition. Check out the
# function inspection options
ESSENTIAL_CSV_COLUMNS = ['sub_id', 'ses_id']
OPTIONAL_CSV_COLUMNS = ['tasks', 'runs']


class AnDOData:

    def __init__(self, sub_id, ses_id, modality='ephys'):
        """
        Representation of a AnDO Data, as specified by in the [ephys BEP](https://docs.google.com/document/d/1oG-C8T-dWPqfVzL2W8HO3elWK8NIh2cOCPssRGv23n0/edit#heading=h.7jcxz3flgq5o)

        The AnDOData object can track multiple realizations of
        `split`, `run`, `task` but only a single realization of `session` and
        `subject`, i.e. to represent multiple `session` folders, multiple
        AnDOData objects are required.

        Args:
            sub_id (str): subject identifier, e.g. '0012' or 'j.s.smith'
            ses_id (str): session identifier, e.g. '2021-01-01' or '007'
            tasks (list): list of strings, the task identifiers used in the 
                session
            runs (list or dict): list of integers, the run identifiers used in
                the session. In case of more than one task a dictionary needs
                to be provided with the task as keys and the list of run
                identifiers as corresponding values
        """

        if modality != 'ephys':
            raise NotImplementedError('AnDO only supports the ephys modality')

        # check for invalid arguments
        for arg in [sub_id, ses_id]:
            invalid_characters = '\/_'  # TODO: Should this be part of the AnDO core?
            if any(elem in arg for elem in invalid_characters):
                raise ValueError(f"Invalid character present in argument ({arg})."
                                 f"The following characters are not permitted: {invalid_characters}")

        self.sub_id = sub_id
        self.ses_id = ses_id
        # self.tasks = tasks
        # self.runs = runs
        self.modality = modality

        # initialize data and metadata structures
        self.data = {}
        self.mdata= {}

        self._basedir = None

    def register_data_files(self, *files, task=None, run=None):
        """
        Register data with the AnDO data structure.

        Args:
            *files: path to files to be added as data files. If multiple files
                are provided they are treated as a single data files split into
                multiple chunks and will be enumerated according to the order
                they are provided in.
        """

        files = [Path(f) for f in files]
        for file in files:
            if file.suffix not in DATA_EXTENSIONS:
                raise ValueError(f'Wrong file format of data {file.suffix}. '
                                 f'Valid formats are {DATA_EXTENSIONS}')

        key = ''
        if task is not None:
            key += f'task_{task}'
        if run is not None:
            key += f'run-{run}'

        if key not in self.data:
            self.data[key] = files
        else:
            self.data['key'].extend(files)

    def register_metadata_files(self, *files):
        files = [Path(f) for f in files]
        for file in files:
            if file.suffix not in METADATA_EXTENSIONS:
                raise ValueError(f'Wrong file format of data {file.suffix}. '
                                 f'Valid formats are {METADATA_EXTENSIONS}')

        self.mdata = files

    # def __str__(self):
    #     return f'{self.date}_{self.sesNumber}_{self.customSesField}'

    @property
    def basedir(self):
        return self._basedir

    @basedir.setter
    def basedir(self, basedir):
        """
        Args:
            basedir (str,path): path to the projects base folder (project root)
        """
        if not Path(basedir).exists():
            raise ValueError('Base directory does not exist')
        self._basedir = basedir

    def get_data_folder(self, mode='absolute'):
        """
        Generate the relative path to the folder of the data files

        Args:
            mode (str): Return the absolute or local path to the data folder.
                Accepted values: 'absolute', 'local'

        Returns:
            path: pathlib.Path of the data folder
        """

        path = Path(f'sub-{self.sub_id}', f'ses-{self.ses_id}', self.modality)

        if mode == 'absolute':
            if self.basedir is None:
                raise ValueError('No base directory set.')
            path = self.basedir / path

        return path

    def generate_structure(self):
        """
        Generate the required folders for storing the dataset

        Returns:
            (path): Path of created data folder
        """

        if self.basedir is None:
            raise ValueError('No base directory set.')

        data_folder = Path(self.basedir).joinpath(self.get_data_folder())
        data_folder.mkdir(parents=True, exist_ok=True)

        return data_folder

    def generate_data_files(self, mode='link'):
        """
        Add datafiles to AnDO structure
        
        Args:
            mode (str): Can be either 'link' 'copy' or 'move'.
        """

        if self.basedir is None:
            raise ValueError('No base directory set.')

        data_folder = self.get_data_folder(mode='absolute')

        # compose BIDS data filenames
        filename_stem = f'sub-{self.sub_id}_ses-{self.ses_id}'

        for key, files in self.data.items():
            # add '_' prefix for filename concatenation
            if key:
                key = '_' + key
            for i, file in enumerate(files):
                # preserve the suffix
                suffix = file.suffix
                # append split postfix if required
                split = ''
                if len(files) > 1:
                    split = f'_split-{i}'

                new_filename = filename_stem + key + split + suffix
                destination = data_folder / new_filename
                create_file(file, destination, mode)


    def generate_metadata_files(self):
        """
        Copy registered metadata files into BIDS structure

        This method currently only takes the file postfix into account
        to determine the target folder.

        """

        data_folder = self.get_data_folder(mode='absolute')

        parents = (data_folder / '_').parents

        for mfile in self.mdata:
            for regex, level in METADATA_LEVEL_BY_NAME.items():
                if re.compile(regex).match(mfile.name):
                    create_file(mfile, parents[(3-level)] / mfile.name,
                                mode='copy')

    def validate(self):
        """
        Validate the generated structure using the AnDO validator

        Returns:
            (bool): True if validation was successful. False if it failed.
        """

        raise NotImplementedError('Ando validation is not implemented yet.')


def create_file(source, destination, mode):
    if mode == 'copy':
        shutil.copy(source, destination)
    elif mode == 'link':
        os.link(source, destination)
    elif mode == 'move':
        shutil.move(source, destination)
    else:
        raise ValueError(f'Invalid file creation mode "{mode}"')


def extract_structure_from_csv(csv_file):

    if not HAVE_PANDAS:
        raise ImportError('Extraction of ando structure from csv requires pandas.')

    df = pd.read_csv(csv_file, dtype=str)

    # ensure all fields contain information
    if df.isnull().values.any():
        raise ValueError(f'Csv file contains empty cells.')

    # standardizing column labels
    # df = df.rename(columns=LABEL_MAPPING)

    # Check is the header contains all required names
    if not set(ESSENTIAL_CSV_COLUMNS).issubset(df.columns):
        raise ValueError(f'Csv file ({csv_file}) does not contain required information '
                         f'({ESSENTIAL_CSV_COLUMNS}). Accepted column names are specified in the BEP.')

    return df


def generate_Struct(csv_file, pathToDir):
    f"""
    Create structure with csv file given in argument
    This file must contain a header row specifying the provided data. Accepted titles are
    defined in the BEP.
    Essential information of the following attributes needs to be present
    {ESSENTIAL_CSV_COLUMNS}

    Args:
        csv_file ([csv file ]): [Csv file that contains a list of directories to create]
        pathToDir ([Path to directory]): [Path to directory where the directories will be created]
    """

    df = extract_structure_from_csv(csv_file)

    df = df[ESSENTIAL_CSV_COLUMNS]

    for session_kwargs in df.to_dict('index').values():
        session = AnDOData(**session_kwargs)
        session.basedir = pathToDir
        session.generate_structure()


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
