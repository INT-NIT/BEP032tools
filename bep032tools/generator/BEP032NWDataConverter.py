from pathlib import Path
from datetime import datetime
import filecmp
import shutil
import argparse
import os
import re
import glob
import numpy as np

import tempfile

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
from bep032tools.generator.BEP032Generator import BEP032Data

METADATA_LEVELS = {i: r['authorized_metadata_files'] for i,r in enumerate(RULES_SET)}
METADATA_LEVEL_BY_NAME = {build_rule_regexp(v)[0]: k for k, values in METADATA_LEVELS.items() for v in values}

# TODO: These can be extracted from the BEP032Data init definition. Check out the
# function inspection options
ESSENTIAL_CSV_COLUMNS = ['sub_id', 'ses_id']
OPTIONAL_CSV_COLUMNS = ['tasks', 'runs', 'data_file']


class BEP032PatchClampNWData(BEP032Data):
    """
    Representation of a patchclamp dataset recorded by NW at INT, Marseille, France, as a
    BEP032 object, as specified by in the
    [ephys BEP](https://bids.neuroimaging.io/bep032)

    The BEP032Data object can track multiple realizations of `split`, `run`, `task` but only a
    single realization of `session` and `subject`, i.e. to represent multiple `session` folders,
    multiple BEP032Data objects are required. To include multiple realizations of tasks
    or runs, call the `register_data` method for each set of parameters separately.
    The particularity of patchclamp data is that we do not use the concept of `session`, nor the
    corresponding directory in the BIDS hierarchy. Therefore, for now, this implementation is
    a bit of a hack (no change in the core of the class definition), but it might evolve in the
    future and require changes in the core of the class.

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

    def generate_metadata_file_participants(self, output):
        print("participaaaaaaaaaaaaaants")
        age = self.md['participants_md']['age']
        date = self.md['participants_md']['date']
        participant_df = pd.DataFrame([
            ['sub-' + self.sub_id, 'rattus norvegicus', age, 'M', '2001-01-01T00:00:00']],
            columns=['participant_id', 'species', 'age', 'sex', 'birthday'])
        participant_df.set_index('participant_id', inplace=True)
        if not output.with_suffix('.tsv').exists():
            # create participants.tsv file
            participant_df.to_csv(output.with_suffix('.tsv'), mode='w', index=True, header=True, sep='\t')
            #save_tsv(participant_df, output)
        else:
            # append new subject to existing participants.tsv file
            participant_df.to_csv(output.with_suffix('.tsv'), mode='a', index=True, header=False, sep='\t')

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
        print("reading metadata xls file")
        metadata = read_metadata_xls_file_nw(self.custom_metadata_sources)
        self.md = metadata
        dest_path = self.get_data_folder(mode='absolute')
        print(self.basedir / f"dataset_description")
        self.generate_metadata_file_participants(self.basedir / f"participants")
        self.generate_metadata_file_dataset_description(self.basedir / f"dataset_description")

        self.generate_metadata_file_tasks(self.basedir / f"tasks")
        self.generate_metadata_file_sessions(self.get_data_folder().parents[1] / f'sub-{self.sub_id}_sessions')
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


def generate_csv_file_nw(pathToRawInputDir, sub_id, metadata_source):
    """
    Generate a csv file that can be used as input to the generate_bids_dataset function, in the particular usecase
    of the conversion of the existing patchclamp data of NW

    Parameters
    ----------
    pathToRawInputDir: str
        Path to the directory containing the raw patchclamp NW data

    sub_id: str
        ID of the animal, corresponding to a subdirectory within the raw patchclamp NW directory

    metadata_source: str
        Filename of the xls file containing the metadata for this data directory

    Returns
    -------
    pathToInputCsv: str
        Path of a csv file containing details about the data set to be converted
    """

    # identify the input ephys data files for this session, as the abf files available in the data directory
    data_path_filter = os.path.join(pathToRawInputDir, sub_id, '*.abf')
    data_files = glob.glob(data_path_filter)
    print(data_files)

    n_sources = len(data_files)
    sources_df = pd.DataFrame(columns=['sub_id', 'ses_id', 'run', 'data_source'])
    for source_ind in range(n_sources):
        ses_id = sub_id
        data_source = data_files[source_ind]
        current_sample_df = pd.DataFrame([[sub_id, ses_id, source_ind, data_source, metadata_source]],
                                         columns=['sub_id', 'ses_id', 'run', 'data_source', 'custom_metadata_source'])
        sources_df = pd.concat([sources_df, current_sample_df])
    sources_df.set_index('sub_id', inplace=True)

    f = tempfile.NamedTemporaryFile(suffix='.tsv', delete=False)
    sources_df.to_csv(f.name, mode='w', index=True, header=True, sep=',')

    return f.name


def read_metadata_xls_file_nw(metadata_xls_file):
    """
    Read the excel file containing the metadata associated with one recording day / one animal in the patchclamp NW
    data set

    Parameters
    ----------
    metadata_xls_file: str
        Path to the excel file containing the metadata

    Returns
    -------
    metadata:
        badly formatted python directory accumulating all the info contained in the excel file
    """
    md = pd.read_excel(metadata_xls_file)

    metadata = {}

    participants_metadata = {}
    samples_metadata_list = []

    participants_metadata.update({'date': str(md.columns[1])})
    participants_metadata.update({'sex': np.array(md.loc[(md[md.columns[1]]=='Sexe')][md.columns[2]])[0]})
    participants_metadata.update({'strain': np.array(md.loc[(md[md.columns[1]]=='Mice Line')][md.columns[2]])[0]})
    participants_metadata.update({'weight': np.array(md.loc[(md[md.columns[1]]=='Weight')][md.columns[2]])[0]})
    participants_metadata.update({'age': np.array(md.loc[(md[md.columns[1]]=='Age')][md.columns[2]])[0]})
    participants_metadata.update({'participant_id': 'sub-{}'.format(participants_metadata['date'][0:10])})

    samples_inds_list = md.loc[(md[md.columns[1]]=='Slice')].index

    all_filenames_list = []
    for ind, sample_ind in enumerate(samples_inds_list):
        # create sub data frame for the current sample / cell
        start_ind = sample_ind
        if ind < len(samples_inds_list) - 1:
            end_ind = samples_inds_list[ind+1]
        else:
            end_ind = len(md)
        sf = md[start_ind:end_ind]
        slice_nbr = np.array(sf.loc[(sf[sf.columns[1]]=='Slice')][sf.columns[2]])[0]
        cell_nbr = np.array(sf.loc[(sf[sf.columns[1]]=='Cell')][sf.columns[2]])[0]
        sample_id = "slice{:02d}cell{:02d}".format(slice_nbr, cell_nbr)
        current_sample_metadata = {}
        current_sample_metadata.update({'sample_id': 'sample-{}'.format(sample_id)})
        current_sample_metadata.update({'sample_type': 'in vitro differentiated cells'})
        current_sample_metadata.update({'participant_id': participants_metadata['participant_id'] })

        re_value = np.array(sf.loc[(sf[sf.columns[1]] == 'Re')][sf.columns[2]])[0]
        current_sample_metadata.update({'re_value': re_value})
        re_unit = np.array(sf.loc[(sf[sf.columns[1]] == 'Re')][sf.columns[3]])[0]
        current_sample_metadata.update({'re_unit': re_unit})
        # offset_value = np.array(sf.loc[(sf[sf.columns[1]] == 'Offset')][sf.columns[2]])[0]
        # current_sample_metadata.update({})
        # offset_unit = np.array(sf.loc[(sf[sf.columns[1]] == 'Offset')][sf.columns[3]])[0]
        # current_sample_metadata.update({})
        # rseal_value = np.array(sf.loc[(sf[sf.columns[1]] == 'Rseal')][sf.columns[2]])[0]
        # current_sample_metadata.update({})
        # rseal_unit = np.array(sf.loc[(sf[sf.columns[1]] == 'Rseal')][sf.columns[3]])[0]
        # current_sample_metadata.update({})
        # hc_value = np.array(sf.loc[(sf[sf.columns[1]] == 'hc')][sf.columns[2]])[0]
        # current_sample_metadata.update({})
        # hc_unit = np.array(sf.loc[(sf[sf.columns[1]] == 'hc')][sf.columns[3]])[0]
        # current_sample_metadata.update({})
        pipcap_valueunit = np.array(sf.loc[(sf[sf.columns[1]] == 'Pipette Capacitance')][sf.columns[3]])[0]
        current_sample_metadata.update({'pipette_capacitance': pipcap_valueunit})
        # vr_value = np.array(sf.loc[(sf[sf.columns[4]] == 'VR')][sf.columns[5]])[0]
        # current_sample_metadata.update({})
        # vr_unit = np.array(sf.loc[(sf[sf.columns[4]] == 'VR')][sf.columns[6]])[0]
        # current_sample_metadata.update({})
        # rm_value = np.array(sf.loc[(sf[sf.columns[4]] == 'Rm')][sf.columns[5]])[0]
        # current_sample_metadata.update({})
        # rm_unit = np.array(sf.loc[(sf[sf.columns[4]] == 'Rm')][sf.columns[6]])[0]
        # current_sample_metadata.update({})
        # hc70_value = np.array(sf.loc[(sf[sf.columns[4]] == 'hc at -70 mV')][sf.columns[5]])[0]
        # current_sample_metadata.update({})
        # hc70_unit = np.array(sf.loc[(sf[sf.columns[4]] == 'hc at -70 mV')][sf.columns[6]])[0]
        # current_sample_metadata.update({})
        # rs_value = np.array(sf.loc[(sf[sf.columns[4]] == 'Rs')][sf.columns[5]])
        # current_sample_metadata.update({})
        # rs_unit = np.array(sf.loc[(sf[sf.columns[4]] == 'Rs')][sf.columns[6]])
        # current_sample_metadata.update({})
        # cm_value = np.array(sf.loc[(sf[sf.columns[4]] == 'Cm')][sf.columns[5]])[0]
        # current_sample_metadata.update({})
        # cm_unit = np.array(sf.loc[(sf[sf.columns[4]] == 'Cm')][sf.columns[6]])[0]
        # current_sample_metadata.update({})

        c = np.array(sf)[:,3]
        t = c[np.where(c=='File')[0][0]+1:]
        # find strings in there... they correspond to the file names containing the ephys data for this sample/cell
        files_inds = np.where(np.array([type(t[i]) for i in range(len(t))])==str)[0]
        # extract all the filenames (all this to deal with the - indicating that several files
        filenames_list = []
        for f_ind in files_inds:
            file_string = t[f_ind]
            dash_ind = file_string.find('-')
            if dash_ind == -1:
                filenames_list.append(file_string)
            else:
                # compute length of what's after the dash in this string... this will give us the length of what
                # we should extract before the string!
                substring_length = len(file_string) - dash_ind - 1
                start_file_number = int(file_string[dash_ind-substring_length:dash_ind])
                end_file_number = int(file_string[dash_ind+1:dash_ind+1+substring_length])
                for nbr in range(start_file_number,end_file_number+1):
                    if substring_length == 3:
                        this_file_string = file_string[0:dash_ind-substring_length] + '{:03d}'.format(nbr)
                    elif substring_length == 2:
                        this_file_string = file_string[0:dash_ind-substring_length] + '{:02d}'.format(nbr)
                    elif substring_length == 1:
                        this_file_string = file_string[0:dash_ind-substring_length] + '{:1d}'.format(nbr)
                    filenames_list.append(this_file_string)
        current_sample_metadata.update({'data_files': filenames_list})
        all_filenames_list.extend(filenames_list)
        samples_metadata_list.append(current_sample_metadata)


    metadata.update({"participants_md":participants_metadata})
    metadata.update({"samples_md":samples_metadata_list})

    #print(metadata)

    return metadata






def main():
    """

    Notes
    ----------

    Usage via command line: BEP032NWDataConverter.py [-h] pathToRawInputDir pathToBIDSOutputDir

    positional arguments:
        pathToRawInputDir     Path to the directory containing the raw patchclamp NW data

        pathToBIDSOutputDir   Path to the directory of the output BIDS dataset

    optional arguments:
        -h, --help  show this help message and exit

    example usage:
         python3 BEP032NWDataConverter.py ~/amubox/ShareElec/nw_data/sourcedata/2016-03/ ~/tmp/tmp_ando_data/
    """

    parser = argparse.ArgumentParser()
    parser.add_argument('pathToRawInputDir', help='Path to the directory containing the raw patchclamp NW data')
    parser.add_argument('pathToBIDSOutputDir', help='Path to the directory of the output BIDS dataset')

    # Create two argument groups

    args = parser.parse_args()

    # Check if directory exists
    if not os.path.isdir(args.pathToBIDSOutputDir):
        print('Directory does not exist:', args.pathToBIDSOutputDir)
        exit(1)

    ###
    # 1. browse the input directory to select the recording days (corresponding to one subject) that will be included
    ###
    recording_days_list = os.listdir(args.pathToRawInputDir)
    # select recording days for which the excel file exists... those will give us the list of subjects we will include
    # in the outbut BIDS dataset (i.e the list of animals because we have one animal per day)
    sub_ids_list = []
    metadata_file_list = []
    for current_day in recording_days_list:
        xls_file = os.path.join(args.pathToRawInputDir,current_day,current_day,'*.xls*')
        xls_list = glob.glob(xls_file)
        if len(xls_list) == 1:
            sub_ids_list.append(str(current_day))
            metadata_file_list.append(xls_list[0])
            print('The following recording date has been selected: ' + current_day)
        elif len(xls_list) == 0:
            print('No excel file for this recording date: ' + current_day + '. Skipping...')
        else:
            print('Several excel files for this recording date: ' + current_day + '. Skipping...')

    print(sub_ids_list)
    print(recording_days_list)


    ###
    # 2. loop over recording days / subjects to generate the BIDS dataset
    ###
    for sub_ind, sub_id in enumerate(sub_ids_list):
        # Construct the csv file that will be used as input to the generate_bids_dataset function
        pathToInputCsv = generate_csv_file_nw(args.pathToRawInputDir, sub_id, metadata_file_list[sub_ind])
        # Read the set of metadata from the excel file
        #this_metadata = read_metadata_xls_file_nw(metadata_file_list[sub_ind])
        # the following needs to be rethought and checked to see whether it's adequate / possible
        #this_bep032data = BEP032PatchClampNWData(sub_id)
        #this_bep032data.md = this_metadata
        BEP032PatchClampNWData.generate_bids_dataset(pathToInputCsv, args.pathToBIDSOutputDir, autoconvert="nix")


if __name__ == '__main__':
    main()
