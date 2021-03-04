from unittest import TestCase
from pathlib import Path
from .. import AnDOChecker as CHK
import os

dir_path = os.path.dirname(os.path.realpath(__file__))


class Test(TestCase):

    ##
    # THE VALID ONES
    ##
    def test_expValid(self):
        path = Path(dir_path) / "dataset" / "exp-valid"
        self.assertEqual(CHK.is_valid(path)[0], True)

    def test_expValidMultipleSession(self):
        path = Path(dir_path) / "dataset" / "exp-validMultipleSession"
        self.assertEqual(CHK.is_valid(path)[0], True)

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
