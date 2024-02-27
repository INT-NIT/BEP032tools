import json
import unittest
from pathlib import Path
import os
from bep032.BEP032 import BEP032
import shutil

from bep032.Modality_agnostic_file import ModalityAgnosticFile
from bep032.generator.tests import utils


class TestModalityAgnosticFile(unittest.TestCase):
    def setUp(self):
        output_path = utils.initialize_test_directory()

        self.test_dir = output_path
        os.makedirs(self.test_dir, exist_ok=True)
        self.instance_agnostic = ModalityAgnosticFile(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)

    def test_create_empty_file(self):
        path_txt = os.path.join(self.test_dir, 'empty_file.txt')
        path_json = os.path.join(self.test_dir, 'empty_file.json')
        self.instance_agnostic.create_empty_file('empty_file.txt')  # Corrected method call
        self.instance_agnostic.create_empty_file('empty_file.json')  # Corrected method call
        self.assertTrue(os.path.exists(path_txt))
        self.assertTrue(os.path.exists(path_json))

    def test_data_structure(self):
        inputs = {"tata": 1, "bibi": 2}

        self.instance_agnostic.write_json_to_file("empty_file.json", inputs)
        with open(os.path.join(self.test_dir, 'empty_file.json')) as json_file:
            expected = json.load(json_file)
        self.assertEqual(expected, inputs)


if __name__ == '__main__':
    unittest.main()
