import unittest
import warnings
import os
import json
import csv
import yaml
from unittest.mock import patch, mock_open, MagicMock
from bep32v01.agnostic_file_template import data_description_json_template, \
    participant_json_template, Citation_template, Sample_template
from bep32v01.writing_agnoticfile import extract_primary_key
from bep32v01.writing_agnoticfile import get_agnostic_file_arguments
from bep32v01.writing_agnoticfile import write_agnostic_files,complete_agnostic_file


class TestAgnosticFiles(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.data_description_template = data_description_json_template
        cls.participant_template = participant_json_template

    def test_extract_primary_key(self):


        template = {
            "Key1": {"Requirement Level": "REQUIRED"},
            "Key2": {"Requirement Level": "RECOMMENDED"},
            "Key3": {"Requirement Level": "OPTIONAL"}
        }
        expected_result = {
            "Key1": "REQUIRED",
            "Key2": "RECOMMENDED",
            "Key3": "OPTIONAL"
        }
        self.assertEqual(extract_primary_key(template), expected_result)

    def test_get_agnostic_file_arguments(self):
        template = {
            "Key1": {"Requirement Level": "REQUIRED"},
            "Key2": {"Requirement Level": "RECOMMENDED"},
            "Key3": {"Requirement Level": "OPTIONAL"}
        }
        expected_result = {
            "Key1": None,
            "Key2": None,
            "Key3": None
        }
        self.assertEqual(get_agnostic_file_arguments(template), expected_result)

    @patch('builtins.open', new_callable=mock_open)
    def test_write_agnostic_files_json(self, mock_open):
        path_to_save = 'output.json'
        template = {
            "Key1": {"Requirement Level": "REQUIRED"},
            "Key2": {"Requirement Level": "RECOMMENDED"},
            "Key3": {"Requirement Level": "OPTIONAL"}
        }
        expected_result = {
            "Key1": "REQUIRED",
            "Key2": "RECOMMENDED",
            "Key3": "OPTIONAL"
        }
        result = write_agnostic_files(path_to_save, template)
        mock_open.assert_called_once_with(path_to_save, 'w')
        mock_open().write.assert_called()
        self.assertEqual(result, expected_result)

    @patch('builtins.open', new_callable=mock_open)
    def test_write_agnostic_files_tsv(self, mock_open):
        path_to_save = 'output.tsv'
        template = {
            "Key1": {"Requirement Level": "REQUIRED"},
            "Key2": {"Requirement Level": "RECOMMENDED"},
            "Key3": {"Requirement Level": "OPTIONAL"}
        }
        expected_result = {
            "Key1": "REQUIRED",
            "Key2": "RECOMMENDED",
            "Key3": "OPTIONAL"
        }
        result = write_agnostic_files(path_to_save, template)
        mock_open.assert_called_once_with(path_to_save, 'w')
        mock_open().write.assert_called()
        self.assertEqual(result, expected_result)

    @patch('builtins.open', new_callable=mock_open)
    def test_write_agnostic_files_yaml(self, mock_open):
        path_to_save = 'output.cff'
        template = {
            "Key1": {"Requirement Level": "REQUIRED"},
            "Key2": {"Requirement Level": "RECOMMENDED"},
            "Key3": {"Requirement Level": "OPTIONAL"}
        }
        expected_result = {
            "Key1": "REQUIRED",
            "Key2": "RECOMMENDED",
            "Key3": "OPTIONAL"
        }
        result = write_agnostic_files(path_to_save, template)
        mock_open.assert_called_once_with(path_to_save, 'w')
        mock_open().write.assert_called()
        self.assertEqual(result, expected_result)

    @patch('os.listdir')
    @patch('os.path.isfile')
    @patch('bep32v01.writing_agnoticfile.write_agnostic_files')
    def test_complete_agnostic_file(self, mock_write_agnostic_files, mock_isfile, mock_listdir):
        output_dir = '/mocked_path'
        mock_listdir.return_value = ['participants.json', 'dataset_description.json',
                                     'CITATION.cff']
        mock_isfile.return_value = True
        complete_agnostic_file(output_dir, BIDSVersion='1.0.0')
        self.assertTrue(mock_write_agnostic_files.called)


if __name__ == '__main__':
    unittest.main()
