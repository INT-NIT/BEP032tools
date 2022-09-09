from pathlib import Path
from datetime import datetime
import filecmp
import shutil
import argparse
import os
import re

import bep032tools.validator.BEP032Validator

try:
    import pandas as pd
    HAVE_PANDAS = True
except ImportError:
    HAVE_PANDAS = False

try:
    import neo
    HAVE_NEO = True
except ImportError:
    HAVE_NEO = False

from bep032tools.validator.BEP032Validator import build_rule_regexp
from bep032tools.rulesStructured import RULES_SET
from bep032tools.rulesStructured import DATA_EXTENSIONS

METADATA_LEVELS = {i: r['authorized_metadata_files'] for i,r in enumerate(RULES_SET)}
METADATA_LEVEL_BY_NAME = {build_rule_regexp(v)[0]: k for k, values in METADATA_LEVELS.items() for v in values}

# TODO: These can be extracted from the BEP032Data init definition. Check out the
# function inspection options
ESSENTIAL_CSV_COLUMNS = ['sub_id', 'ses_id']
OPTIONAL_CSV_COLUMNS = ['tasks', 'runs', 'data_file']


class BEP032Data:
    """
    Representation of a BEP032 Data, as specified by in the
    [ephys BEP](https://bids.neuroimaging.io/bep032)

    The BEP032Data object can track multiple realizations of `split`, `run`, `task` but only a
    single realization of `session` and `subject`, i.e. to represent multiple `session` folders,
    multiple BEP032Data objects are required. To include multiple realizations of tasks
    or runs, call the `register_data` method for each set of parameters separately.

    Parameters
    ----------
    sub_id : str
        subject identifier, e.g. '0012' or 'j.s.smith'
    ses-id : str
        session identifier, e.g. '20210101' or '007'
    tasks : str
        task identifier of data files
    runs : str
        run identifier of data files


    """
    def __init__(self, sub_id, ses_id, modality='ephys'):

        if modality != 'ephys':
            raise NotImplementedError('BEP032tools only supports the ephys modality')

        # check for invalid arguments
        for arg in [sub_id, ses_id]:
            invalid_characters = r'\/_'  # TODO: Should this be part of the BEP032tools core?
            if any(elem in arg for elem in invalid_characters):
                raise ValueError(f"Invalid character present in argument ({arg})."
                                 f"The following characters are not permitted: {invalid_characters}")

        self.sub_id = sub_id
        self.ses_id = ses_id
        self.modality = modality

        # initialize data and metadata structures
        self.data = {}
        self.mdata = {}

        self._basedir = None

    def register_data_files(self, *files, task=None, run=None, autoconvert=None):
        """
        Register data with the BEP032 data structure.

        Parameters
        ----------
        *files : path to files to be added as data files.
            If multiple files are provided they are treated as a single data files split into
            multiple chunks and will be enumerated according to the order they are provided in.

        task: str
            task name used
        run: str
            run name used
        autoconvert: str
            accepted values: 'nix', 'nwb'. Automatically convert to the specified format.
            Warning: Using this feature can require extensive compute resources. Default: None
        """

        files = [Path(f) for f in files]
        for file_idx in range(len(files)):
            if files[file_idx].suffix not in DATA_EXTENSIONS:
                if autoconvert is None:
                    raise ValueError(f'Wrong file format of data {files[file_idx].suffix}. '
                                     f'Valid formats are {DATA_EXTENSIONS}. Use `autoconvert`'
                                     f'parameter for automatic conversion.')
                elif autoconvert not in ['nwb', 'nix']:
                    raise ValueError(f'`autoconvert` only accepts `nix` and `nwb` as values, '
                                     f'received {autoconvert}.')

                print(f'Converting data file to {autoconvert} format.')
                files[file_idx] = convert_data(files[file_idx], autoconvert)

        key = ''
        if task is not None:
            key += f'task-{task}'
        if run is not None:
            if key:
                key += '_'
            key += f'run-{run}'

        if key not in self.data:
            self.data[key] = files
        else:
            self.data[key].extend(files)

    @property
    def basedir(self):
        return self._basedir

    @basedir.setter
    def basedir(self, basedir):
        """
        Parameters
        ----------
        basedir : (str,path)
            path to the projects base folder (project root).
        """
        if not Path(basedir).exists():
            raise ValueError('Base directory does not exist')
        self._basedir = Path(basedir)

    def get_data_folder(self, mode='absolute', ephys_type='extra'):
        """
        Generates the path to the folder of the data files

        Parameters
        ----------
        mode : str
            Returns an absolute or relative path
            Valid values: 'absolute', 'local'
        ephys_type : str
            Type of electrophysiological data. This decides whether or not to create a session level in the BIDS
            hierarchy (yes for extra-cellular recordings, no for intra-cellular recordings)
            Valid values: 'ece', 'ice' (respectively for extra- and intra-cellular electrophysiology)

        Returns
        ----------
        pathlib.Path
            Path of the data folder
        """

        if ephys_type == 'ece':
            path = Path(f'sub-{self.sub_id}', f'ses-{self.ses_id}', self.modality)
        elif ephys_type == 'ice':
            path = Path(f'sub-{self.sub_id}', self.modality)
        else:
            raise ValueError('The ephys_type option should take the value extra or intra')

        if mode == 'absolute':
            if self.basedir is None:
                raise ValueError('No base directory set.')
            path = self.basedir / path

        return path

    def generate_structure(self):
        """
        Generate the required folders for storing the dataset

        Returns
        ----------
        path
            Path of created data folder
        """

        if self.basedir is None:
            raise ValueError('No base directory set.')

        data_folder = Path(self.basedir).joinpath(self.get_data_folder())
        data_folder.mkdir(parents=True, exist_ok=True)

        return data_folder

    def organize_data_files(self, mode='link'):
        """
        Add datafiles to BEP032 structure
        
        Parameters
        ----------
        mode: str
            Can be either 'link', 'copy' or 'move'.
        """
        postfix = '_ephys'
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

                new_filename = filename_stem + key + split + postfix + suffix
                destination = data_folder / new_filename
                create_file(file, destination, mode, exist_ok=True)

    def generate_metadata_file_participants(self, output):
        raise NotImplementedError()

    def generate_metadata_file_tasks(self, output):
        # here we want to call save_json and save_tsv()
        raise NotImplementedError()

    def generate_metadata_file_dataset_description(self, output):
        raise NotImplementedError()

    def generate_metadata_file_sessions(self, output):
        raise NotImplementedError()

    def generate_metadata_file_probes(self, output):
        raise NotImplementedError()

    def generate_metadata_file_channels(self, output):
        raise NotImplementedError()

    def generate_metadata_file_contacts(self, output):
        raise NotImplementedError()

    def generate_metadata_file_ephys(self, output):
        raise NotImplementedError()

    def generate_metadata_file_scans(self, output):
        raise NotImplementedError()

    def generate_all_metadata_files(self):
        dest_path = self.get_data_folder(mode='absolute')

        self.generate_metadata_file_dataset_description(self.basedir
                                                        / "dataset_description")
        self.generate_metadata_file_participants(self.basedir / f"participants")

        self.generate_metadata_file_tasks(self.basedir / f"tasks")
        self.generate_metadata_file_sessions(self.get_data_folder().parents[1] /
                                             f'sub-{self.sub_id}_sessions')
        for key in self.data.keys():
            stem = f'sub-{self.sub_id}_ses-{self.ses_id}'
            if key:
                stem += f'_{key}'
            self.generate_metadata_file_probes(dest_path / (stem + '_probes'))
            self.generate_metadata_file_contacts(dest_path / (stem + '_contacts'))
            self.generate_metadata_file_channels(dest_path / (stem + '_channels'))
            self.generate_metadata_file_ephys(dest_path / (stem + '_ephys'))
            if re.search('run-\\d+', key):
                runs_dest = stem.split('run')[0] + 'scans'
                runs_path = dest_path / runs_dest
                self.generate_metadata_file_scans(runs_path)

    def validate(self):
        """
        Validate the generated structure using the BEP032 validator

        Parameters
        ----------
        output_folder: str
            path to the folder to validate

        Returns
        ----------
        bool
            True if validation was successful. False if it failed.
        """
        bep032tools.validator.BEP032Validator.is_valid(self.basedir)

    @classmethod
    def generate_struct(cls, csv_file, pathToDir):
        """
        Create structure with csv file given in argument
        This file must contain a header row specifying the provided data. Accepted titles are
        defined in the BEP.
        Essential information of the following attributes needs to be present.
        Essential columns are 'sub_id' and 'ses_id'.
        Optional columns are 'runs', 'tasks' and 'data_file' (only single file per sub_id, ses_id
        combination supported). 'data_file' needs to be a valid path to a nix or nwb file.

        Parameters
        ----------
        csv_file: str
            Csv file that contains sub_id and ses_id and optional columns
        pathToDir: str
            Path to directory where the directories will be created.
        """

        df = extract_structure_from_csv(csv_file)
        df = df[ESSENTIAL_CSV_COLUMNS]

        organize_data = 'data_file' in df

        if not os.path.isdir(pathToDir):
            os.makedirs(pathToDir)

        for session_kwargs in df.to_dict('index').values():
            if organize_data:
                data_file = session_kwargs.pop('data_file')
            session = cls(**session_kwargs)
            session.basedir = pathToDir
            session.generate_structure()
            if organize_data:
                session.register_data_files([data_file])
                session.organize_data_files(mode='copy')
            try:
                session.generate_all_metadata_files()
            except NotImplementedError:
                pass


def convert_data(source_file, output_format):
    if not HAVE_NEO:
        raise ValueError('Conversion of data required neo package to be installed. '
                         'Use `pip install neo`')

    io = neo.io.get_io(source_file)
    block = io.read_block()

    output_file = Path(source_file).with_suffix('.' + output_format)

    if output_format == 'nix':
        io_write = neo.NixIO(output_file, mode='rw')
    elif output_format == 'nwb':
        io_write = neo.NWBIO(str(output_file), mode='w')
    else:
        raise ValueError(f'Supported formats are `nwb` and `nix`, not {output_format}')

    # ensure all required annotations are present for nwb file generation
    start_time = datetime.fromtimestamp(int(block.segments[0].t_start.rescale('s')))
    block.annotations.setdefault('session_start_time', start_time)
    block.annotations.setdefault('session_description', block.file_origin)
    block.annotations['session_description'] = str(block.annotations['session_description'])
    block.annotations.setdefault('identifier', block.file_origin)
    block.annotations['identifier'] = str(block.annotations['identifier'])

    io_write.write_all_blocks([block])

    return output_file


def create_file(source, destination, mode, exist_ok=False):
    """
    Create a file at a destination location

    Parameters
    ----------
    source: str
        Source location of the file.
    destination: str
        Destination location of the file.
    mode: str
        File creation mode. Valid parameters are 'copy', 'link' and 'move'.
    exist_ok: bool
        If False, raise an Error if the destination already exist. Default: False
        
    Raises
    ----------
    ValueError
        In case of invalid creation mode.
    """
    if Path(destination).exists():
        if not exist_ok:
            raise ValueError(f'Destination already exists: {destination}')
        # ensure file content is the same
        elif not filecmp.cmp(source, destination, shallow=True):
            raise ValueError(f'File content of source ({source}) and destination ({destination}) '
                             f'differs.')
        # remove current version to create new version with new mode
        Path(destination).unlink()

    if mode == 'copy':
        shutil.copy(source, destination)
    elif mode == 'link':
        os.link(source, destination)
    elif mode == 'move':
        shutil.move(source, destination)
    else:
        raise ValueError(f'Invalid file creation mode "{mode}"')


def extract_structure_from_csv(csv_file):
    """
    Load csv file that contains folder structure information and return it as pandas.datafram.
    
    Parameters
    ----------
    csv_file: str
        The file to be loaded.

    Returns
    -------
    pandas.dataframe
        A dataframe containing the essential columns for creating an BEP032 structure
    """
    if not HAVE_PANDAS:
        raise ImportError('Extraction of bep032tools structure from csv requires pandas.')

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


def main():
    """

    Notes
    ----------

    Usage via command line: BEP032Generator.py [-h] pathToCsv pathToDir

    positional arguments:
        pathToCsv   Path to your csv file

        pathToDir   Path to your folder

    optional arguments:
        -h, --help  show this help message and exit
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('pathToCsv', help='Path to your csv file')
    parser.add_argument('pathToDir', help='Path to your folder')

    # Create two argument groups

    args = parser.parse_args()

    # Check if directory exists
    if not os.path.isdir(args.pathToDir):
        print('Directory does not exist:', args.pathToDir)
        exit(1)
    BEP032Data.generate_struct(args.pathToCsv, args.pathToDir)


if __name__ == '__main__':
    main()
