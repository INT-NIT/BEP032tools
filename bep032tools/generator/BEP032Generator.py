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

METADATA_LEVELS = {i: r['authorized_metadata_files'] for i, r in enumerate(RULES_SET)}
METADATA_LEVEL_BY_NAME = {build_rule_regexp(v)[0]: k for k, values in METADATA_LEVELS.items() for v
                          in values}

# TODO: These can be extracted from the BEP032Data init definition. Check out the
# function inspection options
ESSENTIAL_CSV_COLUMNS = ['sub_id']
OPTIONAL_CSV_COLUMNS = ['ses_id', 'task', 'run', 'data_source']


class BEP032Data:
    """
    Representation of a BEP032 Data, as specified by in the
    [ephys BEP](https://bids.neuroimaging.io/bep032)

    The BEP032Data object can track multiple realizations of `split`, `run`, `task` but only a
    single realization of `session` and `subject`, i.e. to represent multiple `session` folders,
    multiple BEP032Data objects are required. To include multiple realizations of tasks
    or runs, call the `register_data_sources` method for each set of parameters separately.

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

    def __init__(self, sub_id, ses_id=None, modality='ephys', custom_metadata_source=None):

        if modality != 'ephys':
            raise NotImplementedError('BEP032tools only supports the ephys modality')

        # check for invalid arguments
        for arg in [sub_id]:
            invalid_characters = r'\/_'  # TODO: Should this be part of the BEP032tools core?
            if any(elem in arg for elem in invalid_characters):
                raise ValueError(f"Invalid character present in argument ({arg})."
                                 f"The following characters are not permitted: {invalid_characters}")

        self.sub_id = sub_id
        self.ses_id = ses_id
        self.modality = modality
        self.custom_metadata_sources = custom_metadata_source

        # initialize data and metadata structures
        self.data = {}
        self.mdata = {}

        self.filename_stem = None
        self._basedir = None

    def register_data_sources(self, *sources, task=None, run=None):
        """
        Gather all the info about the input data sources (files or directories) that will be
        yield an output data file in the BIDS data structure.

        Parameters
        ----------
        *sources : path to recording files or folders to be added as data files.
            If multiple sources are provided they are treated as multiple chunks
            of the same recording and will be enumerated according to their order.
        task: str
            task name used
        run: str
            run name used
        """

        sources = [Path(f) for f in sources]

        key = ''
        if task is not None:
            key += f'task-{task}'
        if run is not None:
            if key:
                key += '_'
            key += f'run-{run}'

        if key not in self.data:
            self.data[key] = sources
        else:
            self.data[key].extend(sources)

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

    def get_data_folder(self, mode='absolute'):
        """
        Generates the path to the folder of the data files

        Parameters
        ----------
        mode : str
            Returns an absolute or relative path
            Valid values: 'absolute', 'local'

        Returns
        ----------
        pathlib.Path
            Path of the data folder
        """

        if self.ses_id is None:
            # if no session id is given as input (e.g in most cases for intra-cellular ephys), there is no
            # session-level directory in the BIDS hierarchy
            path = Path(f'sub-{self.sub_id}', self.modality)
        else:
            # if a session id exists, a session-level directory is used in the BIDS hierarchy
            # as in most cases for extra-cellular ephys
            path = Path(f'sub-{self.sub_id}', f'ses-{self.ses_id}', self.modality)

        if mode == 'absolute':
            if self.basedir is None:
                raise ValueError('No base directory set.')
            path = self.basedir / path

        return path

    def generate_directory_structure(self):
        """
        Generate the hierarchy of folders that will host the data and metadata files

        Returns
        ----------
        path
            Path of created data folder
        """

        if self.basedir is None:
            raise ValueError('No base directory set.')

        data_folder = Path(self.basedir).joinpath(self.get_data_folder())
        data_folder.mkdir(parents=True, exist_ok=True)

        if self.ses_id is None:
            self.filename_stem = f'sub-{self.sub_id}'
        else:
            self.filename_stem = f'sub-{self.sub_id}_ses-{self.ses_id}'

        return data_folder

    def organize_data_files(self, mode='link', autoconvert=None):
        """
        Add all the data files for which info has been gathered in register_data_sources to the
        BIDS data structure
        
        Parameters
        ----------
        mode: str
            Can be either 'link', 'copy' or 'move'.
        autoconvert: str
            accepted values: 'nix', 'nwb'. Automatically convert to the specified format.
            Warning: Using this feature can require extensive compute resources. Default: None
        """
        postfix = '_ephys'
        if self.basedir is None:
            raise ValueError('No base directory set.')

        if self.filename_stem is None:
            raise ValueError('No filename stem set.')

        data_folder = self.get_data_folder(mode='absolute')

        for key, sources in self.data.items():
            converted_data_files = []

            # add '_' prefix for filename concatenation
            if key:
                key = '_' + key

            # convert each source to single data of valid format if required
            for source_idx, source in enumerate(sources):
                if autoconvert is None:
                    if source.suffix not in DATA_EXTENSIONS:
                        raise ValueError(
                            f'Wrong file format of data {source.suffix}. '
                            f'Valid formats are {DATA_EXTENSIONS}. Use `autoconvert`'
                            f'parameter for automatic conversion.')
                    converted_data_files.append(source)
                elif autoconvert not in ['nwb', 'nix']:
                    raise ValueError(
                        f'`autoconvert` only accepts `nix` and `nwb` as values, '
                        f'received {autoconvert}.')
                elif source.suffix != f'.{autoconvert}':
                    print(f'Converting data file to {autoconvert} format.')
                    converted_data_files.append(convert_data(source, autoconvert))

            for i, file in enumerate(converted_data_files):
                # preserve the suffix
                suffix = file.suffix
                # append split postfix if required
                split = ''
                if len(converted_data_files) > 1:
                    # note JS & ST 2022/11/30: this test is incorrect and should be reimplemented
                    # splits should be introduced only if several data files have
                    # the same values for all their entities (sub, ses, task, run etc.)
                    split = f'_split-{i}'

                new_filename = self.filename_stem + key + split + postfix + suffix
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

        if any(['task' in self.data.keys()]):
            self.generate_metadata_file_tasks(self.basedir / f"tasks")
        if self.ses_id:
            self.generate_metadata_file_sessions(self.get_data_folder().parents[1] /
                                                 f'sub-{self.sub_id}_sessions')
        for key in self.data.keys():
            if self.filename_stem is None:
                raise ValueError('No filename stem set.')
            else:
                stem = self.filename_stem
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
        -------
        bool
            True if validation was successful. False if it failed.
        """
        bep032tools.validator.BEP032Validator.is_valid(self.basedir)

    @classmethod
    def generate_bids_dataset(cls, csv_file, pathToDir, autoconvert=None):
        """
        Create a bids dataset from specifications in a csv file.
        One row of the csv file corresponds to one BEP032 data file in the output BIDS dataset.
        The first row has to contain header labels for each row. Valid headers are:
        Mandatory headers are 'sub_id' and 'ses_id'.
        Optional headers are 'run', 'task' and 'data_source'.

        'data_source' can be: i) an input file (in any raw data format) that needs to be converted to the BIDS-supported
        file formats, ii) an input directory where several raw data files are present that need to be combined and
        converted to a single file in a BIDS-supported format, iii) a file already in a BIDS-supported format that 
        will be copied or linked into the BIDS dataset.

        An example csv table could contain:

        | sub_id  | ses_id     | data_source        | run | task    |
        |---------|------------|--------------------|-----|---------|
        | mouse-A | 2000-01-01 | my_data_file_1.abf | 1   | running |
        | mouse-A | 2000-01-01 | my_data_file_2.abf | 2   | running |
        | mouse-B | 2000-01-01 | my_data_folder_2   |     | rest    |

        Parameters
        ----------
        csv_file: str
            Csv file that contains sub_id and ses_id and optional columns
        pathToDir: str
            Path to directory where the directories will be created.
        autoconvert: str
            see `organize_data_files`
        """

        df = extract_structure_from_csv(csv_file)

        if not os.path.isdir(pathToDir):
            os.makedirs(pathToDir)

        for data_kwargs in df.to_dict('index').values():
            data_source = data_kwargs.pop('data_source', None)

            # extract task and run information if present in the input csf file
            # this should probably be extended to support all BIDS-supported entities
            task = data_kwargs.pop('task', '')
            run = data_kwargs.pop('run', '')

            # replace empty values by good defaults for later function calls
            if task == '':
                task = None
            if run == '':
                run = None

            data_instance = cls(**data_kwargs)
            data_instance.basedir = pathToDir
            data_instance.generate_directory_structure()
            if data_source is not None:
                data_instance.register_data_sources(data_source, task=task, run=run)
                data_instance.organize_data_files(mode='copy', autoconvert=autoconvert)
            try:
                data_instance.generate_all_metadata_files()
            except NotImplementedError:
                pass


def convert_data(source_file_or_folder, output_format):
    if not HAVE_NEO:
        raise ValueError('Conversion of data required neo package to be installed. '
                         'Use `pip install neo`')

    io_read = neo.io.get_io(source_file_or_folder)
    block = io_read.read_block()

    output_file = Path(source_file_or_folder).with_suffix('.' + output_format)

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

    for io in (io_read, io_write):
        if hasattr(io, 'close'):
            io.close()

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

    df = pd.read_csv(csv_file, dtype=str, na_filter=False)

    # standardizing column labels
    # df = df.rename(columns=LABEL_MAPPING)

    # Check is the header contains all required names
    if not set(ESSENTIAL_CSV_COLUMNS).issubset(df.columns):
        raise ValueError(f'Csv file ({csv_file}) does not contain required information '
                         f'({ESSENTIAL_CSV_COLUMNS}). Accepted column names are specified in the BEP.')

    # ensure all fields contain information
    if df[ESSENTIAL_CSV_COLUMNS].isnull().values.any():
        raise ValueError(f'Csv file contains empty cells for mandatory fields.')

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
    BEP032Data.generate_bids_dataset(args.pathToCsv, args.pathToDir)


if __name__ == '__main__':
    main()
