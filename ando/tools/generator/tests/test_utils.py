import unittest

from ando.tools.generator.tests.utils import *
from ando.tools.generator.utils import *
import pandas as pd
import os
import json
from pathlib import Path
import copy

class TestUtils(unittest.TestCase):

    def setUp(self) -> None:
        initialize_test_directory()

    def test_create_file(self):
        df = pd.DataFrame()
        path_to_save = os.path.join(test_directory, "test_create_file.tsv")
        save_tsv(df, path_to_save)
        self.assertTrue(Path(path_to_save).exists())

    def test_create_dummy_file(self):
        df = pd.read_csv(os.path.join(test_directory / 'test_files' / 'participants.tsv'), sep='\t')
        path_to_save = os.path.join(test_directory, "test_create_dummy_file.tsv")
        save_tsv(df, path_to_save)

        self.assertTrue(Path(path_to_save).exists())
        df_test = pd.read_csv(os.path.join(test_directory, "test_create_dummy_file.tsv"), sep='\t')

        self.assertEqual(set(df.columns), set(df_test.columns))
        self.assertEqual(df.shape, df_test.shape)
        self.assertEqual(set(df), set(df_test))

    def test_create_dummy_file_existing(self):
        a = pd.DataFrame({
            "a": [1],
            "c": [0],
            "d": [2]
        })
        res = pd.DataFrame({
            "a": [0, 1],
            "b": [1, 'NaN'],
            "c": ['NaN', 0],
            "d": ['NaN', 2]
        })
        save_tsv(a, os.path.join(test_directory / 'test_files' / 'dummy.tsv'))
        df_test = pd.read_csv(os.path.join(test_directory / 'test_files' / 'dummy.tsv'), sep='\t')
        self.assertEqual(set(df_test), set(res))

    def test_create_json(self):
        data = {'test': 'dummy'}
        path_to_save = os.path.join(test_directory, "dummy.json")
        save_json(data, path_to_save)
        self.assertTrue(Path(path_to_save).exists())

    def test_create_json_file_existing(self):
        data = {'test': 'dummy' ,
                'list': ['dummy'],
                "test_dict": {
                    "key_in_dict_1": "1",
                    }
                }
        result = copy.deepcopy(data)
        path_to_save = os.path.join(test_directory / 'test_files' /"dummy_file.json")
        save_json(result, path_to_save)
        self.assertTrue(all([k in result for k in data.keys()])) # key at first lvl
        self.assertTrue(all([data[k] == result[k] for k in data.keys() if not hasattr(data[k], '__iter__')])) # check keys are the same
        self.assertEqual(result["test_dict"]["key_in_dict_1"], "1") # 2nd lvl hard coded

