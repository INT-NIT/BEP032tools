import unittest
from tools.generator.AnDOGenerator import *

from tools.generator.tests.utils import *

class Test_AnDOData(unittest.TestCase):

    def setUp(self):
        test_dir = initialize_test_directory(clean=True)

        self.sub_id = 'sub5'
        self.ses_id = 'ses1'
        self.tasks = None
        self.runs = None
        self.basedir = test_dir

        d = AnDOData(self.sub_id, self.ses_id)
        d.basedir = self.basedir

        self.ando_data = d


    def test_get_data_folder(self):
        df = self.ando_data.get_data_folder()
        self.assertTrue(df)

        df_abs = self.ando_data.get_data_folder('absolute')
        df_local = self.ando_data.get_data_folder('local')

        self.assertTrue(df_local)
        self.assertTrue(str(df_abs).endswith(str(df_local)))


    def test_generate_structure(self):
        self.ando_data.generate_structure()
        df = self.ando_data.get_data_folder()
        self.assertTrue(df.exists())

    def test_data_files(self):
        self.ando_data.generate_data_files()

    def test_metadata_files(self):
        self.ando_data.generate_metadata_files()

    def tearDown(self):
        initialize_test_directory(clean=True)


class Test_ReadCsv(unittest.TestCase):

    def setUp(self):
        csv_filename = generate_simple_csv_file()
        self.csv_file = csv_filename

    def test_read_csv(self):
        df = extract_structure_from_csv(self.csv_file)
        expected_headers = ['sub_id', 'ses_id']
        self.assertListEqual(expected_headers, list(df))

class Test_GenerateStruct(unittest.TestCase):

    def setUp(self):
        initialize_test_directory(clean=True)
        csv_filename = generate_simple_csv_file()
        self.csv_file = csv_filename

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
        initialize_test_directory(clean=True)


if __name__ == '__main__':
    unittest.main()

