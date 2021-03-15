import os
import unittest
from unittest import TestCase
from pathlib import Path
from ando import AnDOChecker as CHK

if os.system('AnDOChecker'):
    HASANDO = True
else:
    HASANDO = False

dir_path = os.path.dirname(os.path.realpath(__file__))

class Test(TestCase):

    ##
    # THE VALID ONES
    ##
    def test_valid(self):
        path = Path(dir_path) / "dataset" / "exp-valid"
        self.assertEqual(CHK.is_valid(path)[0], True)

    def test_validMultipleSession(self):
        path = Path(dir_path) / "dataset" / "exp-validMultipleSession"
        self.assertEqual(CHK.is_valid(path)[0], True)

    def test_valid_full_metadata(self):
        path = Path(dir_path) / "dataset" / "exp-valid_full_metadata"
        self.assertEqual(CHK.is_valid(path)[0], True)

    ##
    # level 0
    ##
    def test_invalid_folder(self):
        path = Path(dir_path) / "datasets" / "non-existent-folder"
        self.assertEqual(CHK.is_valid(path)[0], False)

    ##
    # level 1
    ##
    def test_experimentError(self):
        path = Path(dir_path) / "dataset" / "experimentError"
        self.assertEqual(CHK.is_valid(path)[0], False)

    def test_datasetDescriptionsMissingError(self):
        path = Path(dir_path) / "dataset" / "exp-datasetDescriptionsMissingError"
        self.assertEqual(CHK.is_valid(path)[0], False)

    def test_participantMissingError(self):
        path = Path(dir_path) / "dataset" / "exp-participantsMissingError"
        self.assertEqual(CHK.is_valid(path)[0], False)

    def test_noSubjectsFolder(self):
        path = Path(dir_path) / "dataset" / "exp-noSubjects"
        self.assertEqual(CHK.is_valid(path)[0], False)

    ##
    # level 2
    ##
    def test_subjectError(self):
        path = Path(dir_path) / "dataset" / "exp-subjectError"
        self.assertEqual(CHK.is_valid(path)[0], False)

    ##
    # level 3
    ##
    def test_sessionError(self):
        path = Path(dir_path) / "dataset" / "exp-sessionError"
        self.assertEqual(CHK.is_valid(path)[0], False)

    def test_ephysMissingError(self):
        path = Path(dir_path) / "dataset" / "exp-ephysMissingError"
        self.assertEqual(CHK.is_valid(path)[0], False)

    def test_nonAuthorizedFolderError(self):
        path = Path(dir_path) / "dataset" / "exp-nonAuthorizedFolderError"
        self.assertEqual(CHK.is_valid(path)[0], False)

    def test_nonAuthorizedMetadataFilesError(self):
        path = Path(dir_path) / "dataset" / "exp-nonAuthorizedMetadataFilesError"
        self.assertEqual(CHK.is_valid(path)[0], False)

    def test_nonAuthorizedDataFilesError(self):
        path = Path(dir_path) / "dataset" / "exp-nonAuthorizedDataFilesError"
        self.assertEqual(CHK.is_valid(path)[0], False)

    ##
    # MULTIPLE ERRORS
    ##
    def test_multipleError(self):
        path = Path(dir_path) / "dataset" / "exp-MultipleError"
        self.assertEqual(CHK.is_valid(path)[0], False)
        self.assertEqual(len(CHK.is_valid(path)[1]), 3)  # check if there is 3 error reported


class TestCLI(TestCase):
    @classmethod
    def switch_dir(self, directory):
        os.chdir(directory)

    def setUp(self):
        self.valid_dir = Path(dir_path) / "dataset" / "exp-valid"

    @unittest.skipIf(HASANDO, reason="requires AnDO to be installed")
    # @pytest.mark.skipif(HASANDO, reason="requires AnDO to be installed")
    def test_simple_api(self):
        res = os.system(f'AnDOChecker -v {self.valid_dir}')
        self.assertEqual(res, 0)

    @unittest.skipIf(HASANDO, reason="requires AnDO to be installed")
    # @pytest.mark.skipif(HASANDO, reason="requires AnDO to be installed")
    def test_current_dir(self):
        self.switch_dir(self.valid_dir)
        res = os.system(f'AnDOChecker -v .')
        self.assertEqual(res, 0)

    @unittest.skipIf(HASANDO, reason="requires AnDO to be installed")
    # @pytest.mark.skipif(HASANDO, reason="requires AnDO to be installed")
    def test_high_level_dir(self):
        self.switch_dir(self.valid_dir / "sub-enya")
        res = os.system(f'AnDOChecker -v ..')
        self.assertEqual(res, 0)

