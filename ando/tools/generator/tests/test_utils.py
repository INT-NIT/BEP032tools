import copy
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

from ando.tools.generator.tests.utils import (initialize_test_directory,
                                              test_directory)
from ando.tools.generator.utils import (save_tsv, save_json,
                                        merge_dfs_by_index, merge_dict)


class TestUtils(unittest.TestCase):

    def setUp(self) -> None:
        initialize_test_directory()

    def test_create_file(self):
        df = pd.DataFrame()
        path_to_save = test_directory / "test_create_file.tsv"
        save_tsv(df, path_to_save)
        self.assertTrue(Path(path_to_save).exists())

    def test_create_dummy_file(self):
        df = pd.read_csv(test_directory / 'test_files' / 'participants.tsv',
                         sep='\t', index_col=0)
        path_to_save = test_directory / "test_create_dummy_file.tsv"
        save_tsv(df, path_to_save)

        self.assertTrue(Path(path_to_save).exists())
        df_read = pd.read_csv(test_directory / "test_create_dummy_file.tsv",
                              sep='\t', index_col=0)
        self.assertTrue(df_read.equals(df))

    def test_save_to_existing_file(self):
        a = pd.DataFrame({
            "i": [1, 2, 3, 4],
            "a": ['a1', 'a2', 'a3', None],
            "b": [None, 'b2', None, 'b4']
        })
        a.set_index('i', inplace=True)
        b = pd.DataFrame({
            "i": [2, 3, 4],
            "b": ['b2', 'b3', None],
            "c": ['c2', None, 'c4']
        })
        b.set_index('i', inplace=True)

        expected = merge_dfs_by_index(a, b)

        a.to_csv(test_directory / 'test_files' / 'a.tsv', sep='\t', index=True)
        b.to_csv(test_directory / 'test_files' / 'b.tsv', sep='\t', index=True)
        expected.to_csv(test_directory / 'test_files' / 'merged_ab.tsv',
                        sep='\t', index=True)

        # merge a -> b
        save_tsv(a, test_directory / 'test_files' / 'b.tsv')

        # read merged version of b
        merged_ab_read = pd.read_csv(test_directory / 'test_files' / 'b.tsv',
                                     sep='\t', index_col=0)

        self.assertTrue(expected.equals(merged_ab_read))

    def test_create_json(self):
        data = {'test': 'dummy'}
        path_to_save = test_directory / "dummy.json"
        save_json(data, path_to_save)
        self.assertTrue(Path(path_to_save).exists())

    def test_create_json_file_existing(self):
        data = {'test': 'dummy',
                'list': ['dummy'],
                "test_dict": {
                    "key_in_dict_1": "1",
                }
                }
        result = copy.deepcopy(data)
        path_to_save = test_directory / 'test_files' / "dummy_file.json"
        save_json(result, path_to_save)
        # verify that all 1st level keys and values are preserved
        self.assertTrue(
            all([k in result for k in data.keys()]))  # key at first lvl
        self.assertTrue(all([data[k] == result[k] for k in data.keys() if
                             not hasattr(data[k], '__iter__')]))
        self.assertEqual(result["test_dict"]["key_in_dict_1"],
                         "1")  # 2nd lvl hard coded

    def test_merge_dfs(self):
        a = pd.DataFrame({
            "i": [1, 2, 3, 4],
            "a": ['a1', 'a2', 'a3', None],
            "b": [None, 'b2', None, 'b4']
        })
        a.set_index('i', inplace=True)
        b = pd.DataFrame({
            "i": [2, 3, 4, 5],
            "b": ['b2', 'b3', None, 'b5'],
            "c": ['c2', None, 'c4', 'c5']
        })
        b.set_index('i', inplace=True)
        res = pd.DataFrame({
            "i": [1, 2, 3, 4, 5],
            "a": ['a1', 'a2', 'a3', None, None],
            "b": [None, 'b2', 'b3', 'b4', 'b5'],
            "c": [None, 'c2', None, 'c4', 'c5'],
        })
        res.set_index('i', inplace=True)

        for df in [a, b, res]:
            df.fillna(value=np.nan, inplace=True)

        merged_df = merge_dfs_by_index(a, b)

        self.assertTrue(res.equals(merged_df))

    def test_merge_dfs_with_conflict(self):
        a = pd.DataFrame({
            "i": [1, 2],
            "a": ['a1', 'a2']
        })
        a.set_index('i', inplace=True)
        b = pd.DataFrame({
            "i": [1, 2],
            "a": ['b1', 'a2'],
        })
        b.set_index('i', inplace=True)
        # res = pd.DataFrame({
        #     "i": [1, 2, 3, 4, 5],
        #     "a": ['a1', 'a2', 'a3', None, None],
        #     "b": [None, 'b2', 'b3', 'b4', 'b5'],
        #     "c": [None, 'c2', None, 'c4', 'c5'],
        # })
        # res.set_index('i', inplace=True)

        for df in [a, b]:
            df.fillna(value=np.nan, inplace=True)

        with self.assertRaises(ValueError):
            merged_df = merge_dfs_by_index(a, b)

    def test_merge_dict_simple_values(self):
        d1 = {'key1': 1,
              'shared_key': 2}
        d2 = {'key2': 1,
              'shared_key': 2}

        expected = {'key1': 1,
                    'key2': 1,
                    'shared_key': 2}
        merged = merge_dict(d1, d2)

        self.assertDictEqual(expected, merged)

    def test_merge_dict_list_values(self):
        d1 = {'key1': [1, 2],
              'shared_key': [1, 2, 3]}
        d2 = {'key2': [2, 3],
              'shared_key': ['a', 'b', 'c']}

        expected = {'key1': [1, 2],
                    'key2': [2, 3],
                    'shared_key': [1, 2, 3, 'a', 'b', 'c']}
        merged = merge_dict(d1, d2)

        self.assertDictEqual(expected, merged)

    def test_merge_dict_simple_nested(self):
        d1 = {'shared': {'simple_value': 1,
                         'complex_value': [1, 2]},
              'only_1': {'simple_value': 1,
                         'complex_value': [1, 2]}}

        d2 = {'shared': {'simple_value': 1,
                         'complex_value': [3, 4]},
              'only_2': {'simple_value': 2,
                         'complex_value': [5, 6]}}

        expected = {'shared': {'simple_value': 1,
                               'complex_value': [1, 2, 3, 4]},
                    'only_1': {'simple_value': 1,
                               'complex_value': [1, 2]},
                    'only_2': {'simple_value': 2,
                               'complex_value': [5, 6]}}
        merged = merge_dict(d1, d2)

        self.assertDictEqual(expected, merged)
