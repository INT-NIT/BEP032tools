import json

from pathlib import Path
import os
from bep032.BEP032 import BEP032
import shutil

from bep032.Modality_agnostic_file import ModalityAgnosticFile


class MicroscopyBidsStructure:
    def __init__(self, output_path, sub_id, sess_id, modality='micrs', tasks=None):
        self.output_path = output_path
        self.bep_instance = BEP032(sub_id, sess_id, modality, tasks)
        self.ModalityAgnosticFile = ModalityAgnosticFile(output_path)

    def create_bids_structure_microscopy(self):
        self.bep_instance.create_directory_structure_by_experience(self.output_path)

        self.bep_instance.create_directory_structure_by_experience(self.output_path)
        self.ModalityAgnosticFile.creat_all_files()

