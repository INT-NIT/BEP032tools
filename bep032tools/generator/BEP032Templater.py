import shutil
import argparse
import re

import bep032tools.validator.BEP032Validator

try:
    import pandas as pd

    HAVE_PANDAS = True
except ImportError:
    HAVE_PANDAS = False
from bep032tools.validator.BEP032Validator import build_rule_regexp
from bep032tools.rulesStructured import RULES_SET
from bep032tools.generator.utils import *
from bep032tools.generator.BEP032Generator import BEP032Data

METADATA_LEVELS = {i: r['authorized_metadata_files'] for i, r in enumerate(RULES_SET)}
METADATA_LEVEL_BY_NAME = {build_rule_regexp(v)[0]: k for k, values in METADATA_LEVELS.items() for v
                          in values}

# TODO: These can be extracted from the BEP032Data init definition. Check out the
# function inspection options
ESSENTIAL_CSV_COLUMNS = ['sub_id', 'ses_id']
OPTIONAL_CSV_COLUMNS = ['tasks', 'runs']


class BEP032TemplateData(BEP032Data):
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

    def __init__(self, sub_id, ses_id):
        super().__init__(sub_id, ses_id, modality='ephys')

    def generate_metadata_file_participants(self, output):
        participant_df = pd.DataFrame([
            ['sub-' + self.sub_id, 'rattus norvegicus', 'p20', 'M', '2001-01-01T00:00:00']],
            columns=['participant_id', 'species', 'age', 'sex', 'birthday'])
        if not output.with_suffix('.tsv').exists():
            save_tsv(participant_df, output)

    def generate_metadata_file_tasks(self, output):
        # here we want to call save_json and save_tsv()
        pass

    def generate_metadata_file_dataset_description(self, output):
        task_dict = {
            "Name": "Electrophysiology",
            "BIDSVersion": "1.6.0",
            "License": "CC BY 4.0",
            "Authors": ["James Bond", "Santa Claus"],
            "Acknowledgements": " We thank the Rudolf the reindeer, the christmas gnomes and "
                                "Miss Moneypenny.",
            "HowToAcknowledge": "Bond J, Claus S (2000) How to deliver 1 Million parcel in one "
                                "night. https://doi.org/007/007 ",
            "Funding": ["The north pole fund 007"],
            "ReferencesAndLinks": "https://doi.org/007/007",
        }
        save_json(task_dict, output)

    def generate_metadata_file_sessions(self, output):
        session_df = pd.DataFrame([
            ['ses-' + self.ses_id, '2009-06-15T13:45:30', '120']],
            columns=['session_id', 'acq_time', 'systolic_blood_pressure'])
        if not output.with_suffix('.tsv').exists():
            save_tsv(session_df, output)

    def generate_metadata_file_probes(self, output):
        probes_df = pd.DataFrame([
            ['e380a', 'multi-shank', 0, 'iridium-oxide', 0, 0, 0, 'circle', 20],
            ['e380b', 'multi-shank', 1.5, 'iridium-oxide', 0, 100, 0, 'circle', 20],
            ['t420a', 'tetrode', 3.6, 'iridium-oxide', 0, 200, 0, 'circle', 20],
            ['t420b', 'tetrode', 7, 'iridium-oxide', 500, 0, 0, 'circle', 20]],
            columns=['probe_id', 'type', 'coordinate_space', 'material', 'x', 'y', 'z', 'shape',
                     'contact_size'])
        save_tsv(probes_df, output)

    def generate_metadata_file_channels(self, output):
        channels_df = pd.DataFrame([
            [129, 1, 'neuronal', 'mV', 30000, 30, 'good'],
            [130, 3, 'neuronal', 'mV', 30000, 30, 'good'],
            [131, 5, 'neuronal', 'mV', 30000, 30, 'bad'],
            [132, 'n/a', 'sync_pulse', 'V', 1000, 1, 'n/a']],
            columns=['channel_id', 'contact_id', 'type', 'units', 'sampling_frequency', 'gain',
                     'status'])
        save_tsv(channels_df, output)

    def generate_metadata_file_contacts(self, output):
        contact_df = pd.DataFrame([
            [1, 'e380a', 0, 1.1, 'iridium-oxide', 0, 0, 0, 'circle', 20],
            [2, 'e380a', 0, 1.5, 'iridium-oxide', 0, 100, 0, 'circle', 20],
            [3, 'e380a', 0, 3.6, 'iridium-oxide', 0, 200, 0, 'circle', 20],
            [4, 'e380a', 1, 7, 'iridium-oxide', 500, 0, 0, 'circle', 20],
            [5, 'e380a', 1, 7, 'iridium-oxide', 500, 100, 0, 'circle', 20],
            [6, 'e380a', 1, 7, 'iridium-oxide', 500, 200, 0, 'circle', 20]],
            columns=['contact_id', 'probe_id', 'shank_id', 'impedance', 'material', 'x', 'y', 'z',
                     'shape',
                     'contact_size'])
        save_tsv(contact_df, output)

    def generate_metadata_file_ephys(self, output):
        ephys_dict = {
            "PowerLineFrequency": 50,
            "PowerLineFrequencyUnit": "Hz",
            "Manufacturer": "OpenEphys",
            "ManufacturerModelName": "OpenEphys Starter Kit",
            "ManufacturerModelVersion": "",
            "SamplingFrequency": 30000,
            "SamplingFrequencyUnit": "Hz",
            "Location": "Institut de Neurosciences de la Timone, Faculté de Médecine, 27, "
                        "Boulevard Jean Moulin, 13005 Marseille - France",
            "Software": "Cerebus",
            "SoftwareVersion": "1.5.1",
            "Creator": "John Doe",
            "Maintainer": "John Doe jr.",
            "Procedure": {
                "Pharmaceuticals": {
                    "isoflurane": {
                        "PharmaceuticalName": "isoflurane",
                        "PharmaceuticalDoseAmount": 50,
                        "PharmaceuticalDoseUnit": "ug/kg/min",
                    },
                    "ketamine": {
                        "PharmaceuticalName": "ketamine",
                        "PharmaceuticalDoseAmount": 0.1,
                        "PharmaceuticalDoseUnit": "ug/kg/min",
                    },
                },
            },
        }
        save_json(ephys_dict, output)

    def generate_metadata_file_scans(self, output):
        pass

    def generate_all_metadata_files(self):
        dest_path = self.get_data_folder(mode='absolute')

        self.generate_structure()
        self.generate_metadata_file_dataset_description(
            self.basedir / "dataset_description")
        self.generate_metadata_file_participants(self.basedir / f"participants")

        self.generate_metadata_file_tasks(self.basedir / f"tasks")
        self.generate_metadata_file_sessions(
            self.get_data_folder().parents[1] / f'sub-{self.sub_id}_sessions')
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


def create_file(source, destination, mode):
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

    Raises
    ----------
    ValueError
        In case of invalid creation mode.
    """
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
        raise ImportError('Extraction of bep032 structure from csv requires pandas.')

    df = pd.read_csv(csv_file, dtype=str)

    # ensure all fields contain information
    if df.isnull().values.any():
        raise ValueError(f'Csv file contains empty cells.')

    # standardizing column labels
    # df = df.rename(columns=LABEL_MAPPING)

    # Check is the header contains all required names
    if not set(ESSENTIAL_CSV_COLUMNS).issubset(df.columns):
        raise ValueError(f'Csv file ({csv_file}) does not contain required information '
                         f'({ESSENTIAL_CSV_COLUMNS}). '
                         f'Accepted column names are specified in the BEP.')

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
    BEP032TemplateData.generate_struct(args.pathToCsv, args.pathToDir)


if __name__ == '__main__':
    main()
