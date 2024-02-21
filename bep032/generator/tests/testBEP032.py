import shutil
import unittest
from pathlib import Path
import os
from bep032.BEP032 import BEP032

import shutil


class TestBEP032(unittest.TestCase):
    def setUp(self):  # <- Corrected method name
        # creat a tmp repository
        output_path = Path('/home/pourtoi/Bureau/Nouveau dossier/BEP/test')
        self.test_dir = output_path
        os.makedirs(self.test_dir, exist_ok=True)
        # Init test values
        self.sub_id = '0012'
        self.sess_id = "20230126"
        self.modality = "ephys"
        self.tasks = ["task1", "task2"]

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_create_directory_structure_by_experience(self):
        # creat a test instance
        bep_instance = BEP032(self.sub_id, self.sess_id, self.modality, self.tasks)

        # creat a test directory
        bep_instance.create_directory_structure_by_experience(self.test_dir)

        # check if directory is created
        subject_dir = self.test_dir / f'sub_{self.sub_id}'
        session_dir = subject_dir / f'ses_{self.sess_id}'
        modality_dir = session_dir / self.modality
        self.assertTrue(subject_dir.exists())
        self.assertTrue(session_dir.exists())
        self.assertTrue(modality_dir.exists())

    def test_create_files_in_directory(self):
        # Creat  a BEP032 instance
        bep032_instance = BEP032(self.sub_id, self.sess_id, self.modality, self.tasks)

        # call the build function for files
        bep032_instance.create_files_in_directory(self.test_dir)

        #  check if all files was created
        subject_dir = self.test_dir / f'sub_{self.sub_id}'
        session_dir = subject_dir / f'ses_{self.sess_id}'
        modality_dir = session_dir / self.modality

        #  files in sub _directory
        self.assertTrue(os.path.exists(subject_dir / f'sub_{self.sub_id}_sessions.json'))
        self.assertTrue(os.path.exists(subject_dir / f'sub_{self.sub_id}_sessions.tsv'))

        # tasks files
        for task in self.tasks:
            self.assertTrue(os.path.exists(modality_dir / f'sub_{self.sub_id}_ses_{self.sess_id}_task_{task}.tsv'))


if __name__ == '__main__':
    unittest.main()
