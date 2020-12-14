import unittest
import shutil
import tempfile
from tools.generator.AnDOGenerator import *

test_directory = os.path.join(tempfile.gettempdir(), 'ando_testfiles')

class Test_AnDOSesID(unittest.TestCase):

    def setUp(self):
        self.date = '20000101'
        self.sesNumber = '100'
        self.customSesField = 'test'
        self.sesID = f'{self.date}_{self.sesNumber}_{self.customSesField}'

    def test_user_input_warning(self):
        with self.assertWarns(Warning):
            AnDOSesID(sesID=self.sesID, date=self.date, sesNumber=self.sesNumber)

    def test_insufficient_input_error(self):
        with self.assertRaises(ValueError):
            AnDOSesID()

    def test_datetime(self):
        date_obj = datetime.datetime.strptime(self.date, '%Y%m%d')
        sesID = AnDOSesID(date=date_obj, sesNumber=self.sesNumber)
        self.assertEqual(self.date, sesID.date)

    def test_only_sesID(self):
        sesID = AnDOSesID(sesID=self.sesID)

        self.assertEqual(self.sesID, str(sesID))
        self.assertEqual(self.date, sesID.date)
        self.assertEqual(self.sesNumber, sesID.sesNumber)
        self.assertEqual(self.customSesField, sesID.customSesField)

    def test_no_sesID(self):
        sesID = AnDOSesID(date=self.date, sesNumber=self.sesNumber, customSesField=self.customSesField)

        self.assertEqual(self.sesID, str(sesID))
        self.assertEqual(self.date, sesID.date)
        self.assertEqual(self.sesNumber, sesID.sesNumber)
        self.assertEqual(self.customSesField, sesID.customSesField)


class Test_AnDOSession(unittest.TestCase):

    def setUp(self):
        os.mkdir(test_directory)
        self.expName = 'exp23'
        self.guid = '1234'
        self.date = '20000101'
        self.sesNumber = '100'
        self.customSesField = 'test'
        self.sesID = f'{self.date}_{self.sesNumber}_{self.customSesField}'


    def test_insufficient_input(self):
        with self.assertRaises(ValueError):
            AnDOSession(None, self.guid)

        with self.assertRaises(ValueError):
            AnDOSession(self.expName, None)

    def test_simple_parameters(self):
        ses = AnDOSession(self.expName, self.guid, self.sesID)

        self.assertEqual(self.expName, ses.expName)
        self.assertEqual(self.guid, ses.guid)
        self.assertEqual(self.sesID, str(ses.sesID))

    def test_complex_parameters(self):
        ses = AnDOSession(self.expName,
                          self.guid,
                          sesNumber=self.sesNumber,
                          date=self.date,
                          customSesField=self.customSesField)

        self.assertEqual(self.expName, ses.expName)
        self.assertEqual(self.guid, ses.guid)
        self.assertEqual(self.sesID, str(ses.sesID))

    # TODO: This check is still failing, review engine/check_Path for consistency
    def test_paths(self):
        ses = AnDOSession(self.expName, self.guid, self.sesID)

        expected = os.path.join(f'exp-{self.expName}', f'sub-{self.guid}', f'ses-{self.sesID}')
        self.assertEqual(expected, ses.get_session_path())

        self.assertEqual(3, len(ses.get_all_folder_paths()))

    def test_generate_folders(self):
        ses = AnDOSession(self.expName, self.guid, self.sesID)

        paths = ses.get_all_folder_paths()

        # delete paths in case they already exist
        for path in paths:
            if os.path.exists(os.path.join(test_directory, path)):
                os.remove(path)

        ses.generate_folders(basedir=test_directory)

        for path in paths:
            self.assertTrue(os.path.exists(os.path.join(test_directory, path)))

    def doCleanups(self):
        shutil.rmtree(test_directory)


class Test_ReadCsv(unittest.TestCase):

    def setUp(self):
        self.csv_file = 'example.csv'

    def test_read_csv(self):
        df = extract_structure_from_csv(self.csv_file)
        expected_headers = ['expName', 'guid', 'sesNumber', 'customSesField', 'date']
        self.assertListEqual(expected_headers, list(df))

class Test_GenerateStruct(unittest.TestCase):

    def setUp(self):
        try:
            os.mkdir(test_directory)
        except FileExistsError:
            self.doCleanups()
            os.mkdir(test_directory)
        self.csv_file = 'example.csv'

    def test_generate_example_structure(self):
        generate_Struct(self.csv_file, test_directory)

        # extract all paths that exist in the test directory
        existing_paths = [p[0] for p in os.walk(test_directory)]

        # find path that is corresponding to each line of the csv file
        with open(self.csv_file) as f:
            header = f.readline()
            # iterate through sessions
            for line in f.readlines():
                found_path = False
                for existing_path in existing_paths:
                    if all(key in existing_path for key in line.strip().split(',')):
                        found_path = True
                        break
                if not found_path:
                    print(line.strip().split(','))

                self.assertTrue(found_path)

    def doCleanups(self):
        shutil.rmtree(test_directory)


if __name__ == '__main__':
    unittest.main()

