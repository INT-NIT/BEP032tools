import os
import sys
import tempfile
import unittest
import shutil
import json

# Ajouter le chemin du dossier parent pour trouver le package BIDSTools
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from BIDSTools.ProcessBIDSDATA import check_subdir, generate_subdir, generate_datatype_dir, \
    generate_datatype_dir, generate_datatype_dir, generate_session_dir, writeheader, \
    writeheader_tsv_json_files, add_new_experiment_to_tsv


class TestProcessBIDSData(unittest.TestCase):

    def setUp(self):
        """Set up a temporary directory for testing."""
        self.outdir = tempfile.mkdtemp()
        self.sub_id = '1'
        self.session_id = '1'
        self.datatype = 'beh'
        self.bids_dir = os.path.join(self.outdir, 'sub-' + str(self.sub_id))
        os.makedirs(self.bids_dir)
        self.session_dir = os.path.join(self.bids_dir, 'ses-' + self.session_id)
        self.datatype_dir = os.path.join(self.session_dir, self.datatype)
        self.current_dir = self.bids_dir
        self.template_content = {
            " Subject ID": {"Default value": "1"},
            "species": {"Default value": "Homo sapiens"},
            "age": {"Default value": "30"},
            "Sex": {"Default value": "M"},
            "handedness": {"Default value": "R"},
            "strain": {"Default value": ""},
            "strain_rrid": {"Default value": ""}
        }

    def tearDown(self):
        """Clean up the temporary directory after each test."""
        shutil.rmtree(self.outdir)

    def test_check_subdir(self):
        """Test the check_subdir function."""
        self.assertTrue(check_subdir(self.outdir, self.sub_id),
                        "Subdirectory does not exist when it should")
        self.current_dir = os.path.join(self.outdir, 'sub-' + str(self.sub_id))
        print(f"Current Directory in test_check_subdir: {self.current_dir}")

    def test_generate_subdir(self):
        """Test the generate_subdir function."""
        current_dir = generate_subdir(self.outdir, self.sub_id)
        self.assertTrue(os.path.isdir(current_dir), "Subdirectory does not exist when it should")
        self.assertEqual(current_dir, self.bids_dir, "Generated subdirectory path is incorrect")
        self.current_dir = current_dir
        print(f"Current Directory in test_generate_subdir: {self.current_dir}")

    def test_generate_session_dir(self):
        current_dir = generate_session_dir(self.bids_dir, session_id=self.session_id)
        self.assertTrue(os.path.isdir(current_dir),
                        "Session directory does not exist when it should")
        self.assertEqual(current_dir, self.session_dir,
                         "Generated session directory path is incorrect")

    def test_generate_datatype_dir(self):
        current_dir = generate_datatype_dir(self.session_dir, datatype=self.datatype)
        self.assertTrue(os.path.isdir(current_dir),
                        "Datatype directory does not exist when it should")
        self.assertEqual(current_dir, self.datatype_dir,
                         "Generated datatype directory path is incorrect")

    def test_writeheader(self):
        self.file_name = 'test_file.tsv'
        self.file_path = os.path.join(self.current_dir, self.file_name)
        with open(self.file_path, 'w') as f:
            pass
        writeheader(self.template_content, self.file_name, self.current_dir)
        with open(self.file_path, 'r') as f:
            content = f.read()
        expected_header = '\t'.join(self.template_content.keys()) + '\n'
        self.assertEqual(content, expected_header, "Header content incorrect")

    def test_writeheader_tsv_json_files(self):
        tsv_file = "participants.tsv"
        file_path = os.path.join(self.current_dir, tsv_file)
        with open(file_path, 'w') as f:
            pass
        writeheader_tsv_json_files(self.current_dir)
        with open(file_path, 'r') as f:
            content = f.read()
        expected_header = '\t'.join(self.template_content.keys()) + '\n'
        assert content == expected_header, "Header content incorrect"


if __name__ == '__main__':
    unittest.main()
