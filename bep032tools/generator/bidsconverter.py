from abc import ABC, abstractmethod
from collections import defaultdict
from pathlib import Path


class BidsConverter(ABC):

    def __init__(self, dataset_path, **kwargs):
        self.dataset_path = Path(dataset_path)
        self._kwargs = kwargs
        self._participants_dict = dict(name=Path('participants.tsv'),
                                       data=None)
        self._dataset_desc_json = dict(name=Path('dataset_description.json'),
                                       data=None)
        self._sessions_dict = defaultdict(dict)
        self._channels_dict = defaultdict(dict)
        self._contacts_dict = defaultdict(dict)
        self._ephys_dict = defaultdict(dict)
        self._probes_dict = defaultdict(dict)
        self._nwbfile_name_dict = defaultdict(dict)
        self.datafiles_list = []

    @abstractmethod
    def _extract_metadata(self):
        pass

    @abstractmethod
    def organize(self):
        pass

    def get_subject_names(self):
        return list(self._participants_dict['data']['ParticipantID'])

    def get_session_names(self, subject_name=None):
        if subject_name is None:
            subject_name = self.get_subject_names()[0]
        return list(self._sessions_dict[subject_name]['data']['session_id'])

    def get_channels_info(self, subject_name=None, session_name=None):
        if subject_name is None:
            subject_name = self.get_subject_names()[0]
        if session_name is None:
            session_name = self.get_session_names()[0]
        return self._channels_dict[subject_name][session_name]['data'].to_dict()

    def get_contacts_info(self, subject_name=None, session_name=None):
        if subject_name is None:
            subject_name = self.get_subject_names()[0]
        if session_name is None:
            session_name = self.get_session_names()[0]
        return self._contacts_dict[subject_name][session_name]['data'].to_dict()

    def get_ephys_info(self, subject_name=None, session_name=None):
        if subject_name is None:
            subject_name = self.get_subject_names()[0]
        if session_name is None:
            session_name = self.get_session_names()[0]
        return self._ephys_dict[subject_name][session_name]['data']

    def get_probes_info(self, subject_name=None, session_name=None):
        if subject_name is None:
            subject_name = self.get_subject_names()[0]
        if session_name is None:
            session_name = self.get_session_names()[0]
        return self._probes_dict[subject_name][session_name]['data'].to_dict()

    def get_participants_info(self):
        return self._participants_dict['data'].to_dict()

    def get_dataset_description(self):
        return self._dataset_desc_json['data']

    def get_session_info(self, subject_name=None):
        if subject_name is None:
            subject_name = self.get_subject_names()[0]
        return self._sessions_dict[subject_name]['data'].to_dict()
