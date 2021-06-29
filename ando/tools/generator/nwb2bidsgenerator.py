import json
import re
import shutil
from collections import defaultdict
from pathlib import Path

import pandas as pd
from pynwb import NWBHDF5IO
from pynwb.ecephys import ElectricalSeries
from tqdm import tqdm

from ando.AnDOChecker import is_valid
from .bidsconverter import BidsConverter


class NwbToBIDS(BidsConverter):

    def __init__(self, dataset_path, **kwargs):
        super().__init__(dataset_path, **kwargs)
        self.datafiles_list = list(self.dataset_path.glob('**/*.nwb'))
        assert len(self.datafiles_list) > 0, 'no nwb files found'
        self._extract_metadata()

    def _extract_metadata(self):
        self._participants_dict.update(data=pd.DataFrame(
                                           columns=['species', 'participant_id', 'sex', 'birthdate', 'age', 'genotype',
                                                    'weight']))
        for file_no, nwb_file in enumerate(tqdm(self.datafiles_list)):
            with NWBHDF5IO(str(nwb_file), 'r') as io:
                nwbfile = io.read()

                # 1) FULL DATASET INFO:
                # subject info:
                sub_df, subject_label = self._get_subject_info(nwbfile, subject_suffix=str(file_no))
                if not self._participants_dict['data']['participant_id'].str.contains(
                        subject_label).any():
                    self._participants_dict['data'].loc[len(self._participants_dict['data'].index)] = sub_df
                # dataset_info:
                if self._dataset_desc_json['data'] is None:
                    self._dataset_desc_json['data'] = self._get_dataset_info(nwbfile)

                # 2) SUBJECT SPECIFIC:
                # session info:
                base_location_1 = Path(f'{subject_label}')
                session_default_dict = dict(name=base_location_1/f'{subject_label}_sessions.tsv',
                                            data=pd.DataFrame(
                                                columns=['session_id', '#_trials', 'comment']))
                session_info = self._get_session_info(nwbfile)
                sessions_label = session_info[0]
                sessions_df = self._sessions_dict.get(subject_label, session_default_dict)['data']
                if not sessions_df['session_id'].str.contains(sessions_label).any():
                    sessions_df.loc[len(sessions_df.index)] = session_info
                    session_default_dict.update(data=sessions_df)
                self._sessions_dict[subject_label] = session_default_dict

                # 3) SUBJECT>SESSION SPECIFIC:
                base_location_2 = Path(subject_label)/Path(sessions_label)/Path('ephys')
                # channels_info:
                channel_default_dict = dict(name=base_location_2/f'{subject_label}_{sessions_label}_channels.tsv',
                                            data=self._get_channels_info(nwbfile))
                self._channels_dict[subject_label].update({sessions_label: channel_default_dict})
                # ephys_json:
                ephys_default_dict = dict(name=base_location_2/f'{subject_label}_{sessions_label}_ephys.json',
                                          data=self._get_ephys_info(nwbfile, **self._kwargs))
                self._ephys_dict[subject_label].update({sessions_label: ephys_default_dict})
                # contacts/probes info:
                contact_df, probes_df = self._get_contacts_info(nwbfile, **self._kwargs)
                contacts_default_dict = dict(name=base_location_2/f'{subject_label}_{sessions_label}_contacts.tsv',
                                             data=contact_df)
                probes_default_dict = dict(name=base_location_2/f'{subject_label}_{sessions_label}_probes.tsv',
                                           data=probes_df)
                self._contacts_dict[subject_label].update({sessions_label: contacts_default_dict})
                self._probes_dict[subject_label].update({sessions_label: probes_default_dict})
                # nwbfile location:
                nwbfile_default_dict = dict(name=base_location_2/f'{subject_label}_{sessions_label}_ephys.nwb',
                                            data=nwb_file)
                self._nwbfile_name_dict[subject_label].update({sessions_label: nwbfile_default_dict})

    @staticmethod
    def _get_subject_info(nwbfile, subject_suffix=''):
        if nwbfile.subject is not None:
            sb = nwbfile.subject
            if sb.subject_id is not None:
                sub_id = re.sub(r'[\W_]+', '', sb.subject_id)
                subject_label = f'sub-{sub_id}'
            else:
                subject_label = f'sub-{sb.date_of_birth.strftime("%Y%m%dT%H%M")}'
            return [sb.species, subject_label, sb.sex[0] if sb.sex is not None else None,
                    sb.date_of_birth, sb.age, sb.genotype, sb.weight], subject_label
        else:
            subject_label = f'sub-noname{subject_suffix}'
            return [None, subject_label, None, None, None, None, None], subject_label

    @staticmethod
    def _get_dataset_info(nwbfile):
        return dict(
            Name='Electrophysiology', BIDSVersion='1.0.X',
            Licence='CC BY 4.0',
            Authors=[
                list(nwbfile.experimenter) if nwbfile.experimenter is not None else None][0])

    @staticmethod
    def _get_session_info(nwbfile):
        trials_len = len(
            nwbfile.trials) if nwbfile.trials is not None else None
        if nwbfile.session_id is not None:
            ses_id = re.sub(r'[\W_]+', '', nwbfile.session_id)
            session_label = f'ses-{ses_id}'
        else:
            session_label = f'ses-{nwbfile.session_start_time.strftime("%Y%m%dT%H%M")}'
        return [session_label, trials_len, nwbfile.session_description]

    @staticmethod
    def _get_channels_info(nwbfile):
        channels_df = pd.DataFrame(
            columns=['channel_id', 'contact_id', 'type', 'units', 'sampling_frequency',
                     'unit_conversion_multiplier'])
        es = [
            i for i in nwbfile.children if isinstance(
                i, ElectricalSeries)]
        if len(es) > 0:
            es = es[0]
            no_channels = es.data.shape[1]
            sampling_frequency = es.rate
            conversion = es.conversion
            unit = es.unit
            for chan_no in range(no_channels):
                channels_df.loc[len(channels_df.index)] = [chan_no, chan_no, 'neural signal',
                                                           unit,
                                                           sampling_frequency, conversion]
        return channels_df

    @staticmethod
    def _get_ephys_info(nwbfile, **kwargs):
        return dict(PowerLineFrequency=kwargs.get('PowerLineFrequency', 50.0),
                    InstitutionName=nwbfile.institution,
                    InstitutionalDepartmentName=nwbfile.lab)

    @staticmethod
    def _get_contacts_info(nwbfile, **kwargs):
        contacts_df = pd.DataFrame(
            columns=[
                'x',
                'y',
                'z',
                'impedance',
                'contact_id',
                'probe_id',
                'location'])
        probes_df = pd.DataFrame(columns=['probe_id', 'type'])
        e_table = nwbfile.electrodes
        if e_table is not None:
            for contact_no in range(len(e_table)):
                contacts_df.loc[len(contacts_df.index)] = [e_table.x[contact_no],
                                                           e_table.y[contact_no],
                                                           e_table.z[contact_no],
                                                           e_table.imp[contact_no],
                                                           contact_no,
                                                           e_table.group[contact_no].device.name,
                                                           e_table.location[contact_no]]
        for probe_id in contacts_df['probe_id'].unique():
            probes_df.loc[len(probes_df.index)] = [
                probe_id, kwargs.get('probe_type', 'acute')]
        return contacts_df, probes_df

    def organize(self, output_path=None, move_nwb=False,
                 re_write=True, validate=True):
        if output_path is None:
            output_path = self.dataset_path.parent/'BIDSExt'/self.dataset_path.name
        else:
            output_path = Path(output_path)
        if re_write and output_path.exists():
            shutil.rmtree(output_path)
        # CREATE FILES:
        # 1) data_desc, participants:
        output_path.mkdir(parents=True, exist_ok=True)
        data, loc = self._parse_data_dict(self._participants_dict, output_path)
        data.dropna(axis='columns', how='all', inplace=True)
        data.to_csv(loc, sep='\t', index=False)
        data, loc = self._parse_data_dict(self._dataset_desc_json, output_path)
        with open(loc, 'w') as j:
            if all([True for au in data['Authors'] if au is None]):
                _ = data.pop('Authors')
            dataset_desc_tosave = {k: v for k,
                                            v in data.items() if v is not None}
            json.dump(dataset_desc_tosave, j)

        # 2) sessions.tsv:
        for ses_file_dict in self._sessions_dict.values():
            data, loc = self._parse_data_dict(ses_file_dict, output_path)
            if not loc.parent.exists():
                loc.parent.mkdir(parents=True)
            data.to_csv(loc, sep='\t', index=False)

        # 3) subject>sessions>ephys specific files:
        for subject_id in self._participants_dict['data']['participant_id']:
            for session_id in self._sessions_dict[subject_id]['data']['session_id']:
                # ephys.json
                base_loc = output_path/subject_id/session_id/'ephys'
                if not base_loc.exists():
                    base_loc.mkdir(parents=True)
                data, loc = self._parse_data_dict(
                    self._ephys_dict[subject_id][session_id],
                    output_path)
                with open(loc, 'w') as j:
                    json.dump(data, j)
                # channels tsv:
                data, loc = self._parse_data_dict(
                    self._channels_dict[subject_id][session_id],
                    output_path)
                self._write_csv(data, loc)
                # contacts/probes tsv:
                data, loc = self._parse_data_dict(
                    self._contacts_dict[subject_id][session_id],
                    output_path)
                self._write_csv(data, loc)
                data, loc = self._parse_data_dict(
                    self._probes_dict[subject_id][session_id],
                    output_path)
                self._write_csv(data, loc)
                # nwbfile move:
                data, loc = self._parse_data_dict(
                    self._nwbfile_name_dict[subject_id][session_id],
                    output_path)
                if move_nwb:
                    if not loc.exists():
                        data.replace(loc)
                else:
                    if not loc.exists():
                        loc.symlink_to(data)

        if validate:
            is_valid(output_path)

    def _parse_data_dict(self, data_dict, output_path):
        return data_dict['data'], output_path/data_dict['name']

    def _write_csv(self, data, loc):
        if not loc.exists():
            data.dropna(axis='columns', how='all', inplace=True)
            data.to_csv(loc, sep='\t', index=False)
