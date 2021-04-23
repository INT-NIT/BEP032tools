import unittest

from ando.tools.generator.tests.utils import *
from ando.tools.generator.utils import *
import pandas as pd
import os
from pathlib import Path

class TestUtils(unittest.TestCase):

    def setUp(self) -> None:
        initialize_test_directory()

    def test_merge_if_file_exist(self):
        pass

    def test_merge_if_file_not_exist(self):
        pass
        # safe_tsv(pd,path)
        # self.assertTrue((path).exists())
        # new_df = DataFrame.from_csv(path, sep='\t', header=0)
        # self.assertEqual(df.columns,new_df.columns)
        # self.assertEqual(df.shape,new_df.shape)

    def test_create_file(self):
        df = pd.DataFrame()
        path_to_save = os.path.join(test_directory, "test_create_file.tsv")
        save_tsv(df, path_to_save)
        self.assertTrue(Path(path_to_save).exists())

    def test_create_dummy_file(self):
        print((test_directory / 'test_files').glob("*"))
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
        res =  pd.DataFrame({
            "a": [0, 1],
            "b": [1, 'NaN'],
            "c": ['NaN', 0],
            "d": ['NaN', 2]
        })
        save_tsv(a, os.path.join(test_directory / 'test_files' / 'dummy.tsv'))
        df_test = pd.read_csv(os.path.join(test_directory / 'test_files' / 'dummy.tsv'), sep='\t')
        self.assertEqual(set(df_test),set(res))



