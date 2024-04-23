import unittest
import os
import shutil
from pathlib import Path
from bep032.Microscopy_bids_structure import MicroscopyBidsStructure
import utils


class TestMicroscopyBidsStructure(unittest.TestCase):
    def setUp(self):
        self.out_put = utils.initialize_test_directory()
        os.makedirs(self.out_put, exist_ok=True)

    """def tearDown(self):
        shutil.rmtree(self.out_put, ignore_errors=True)"""

    def test_create_bids_structure_microscopy(self):
        sub_id = "Microscopy"
        sess_id = "20242602"
        modality = "micr"
        tasks = ["task1", "task2", "task3"]

        microscopy_instance = MicroscopyBidsStructure(self.out_put, sub_id, sess_id, modality, tasks)
        microscopy_instance.create_bids_structure_microscopy()

        # Add assertions to check if the BIDS structure and files are created as expected
        self.assertTrue(os.path.exists(os.path.join(self.out_put, 'sub-Microscopy')))
        self.assertTrue(os.path.exists(os.path.join(self.out_put, 'sub-Microscopy', 'ses-20242602')))
        # Add more assertions as needed to check the directory structure and files creation


if __name__ == '__main__':
    unittest.main()
