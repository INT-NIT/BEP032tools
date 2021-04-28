import unittest
from ando.tools.generator.AnDOGenerator import *

from ando.tools.generator.tests.utils import *

class Test_AnDOData(unittest.TestCase):

    def setUp(self):
        test_dir = Path(initialize_test_directory(clean=True))

        self.sub_id = 'sub5'
        self.ses_id = 'ses1'
        self.tasks = None
        self.runs = None
        
        sources = test_dir / 'sources'
        sources.mkdir()
        project = test_dir / 'project-A'
        project.mkdir()
        self.basedir = project

        d = AnDOData(self.sub_id, self.ses_id)
        d.basedir = project

        self.ando_data = d
        prefix = f'sub-{self.sub_id}_ses-{self.ses_id}'
        self.test_data_files = [sources / (prefix + '_ephy.nix'),
                                sources / (prefix + '_ephy.nwb')]
        self.test_mdata_files = [sources / 'dataset_description.json',
                                 sources / (prefix + '_probes.tsv'),
                                 sources / (prefix + '_contacts.json')]

        for f in self.test_mdata_files + self.test_data_files:
            f.touch()

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
        self.ando_data.generate_structure()
        self.ando_data.register_data_files(*self.test_data_files)
        self.ando_data.generate_data_files()

        session_folder = self.ando_data.get_data_folder()
        self.assertTrue(session_folder.exists())
        data_files = list(session_folder.glob('*.nix'))
        data_files += list(session_folder.glob('*.nwb'))
        self.assertEqual(len(self.test_data_files), len(data_files))
        for data_file in data_files:
            self.assertTrue(data_file.name.find("_ephys"))

    def test_data_files_complex(self):
        self.ando_data.generate_structure()
        nix_files = [self.test_data_files[0]] * 3
        runs = ['run1', 'run2']
        tasks = ['task1', 'task2']
        for run in runs:
            for task in tasks:
                self.ando_data.register_data_files(*nix_files,
                                                   run=run, task=task)

        self.ando_data.generate_data_files()

        session_folder = self.ando_data.get_data_folder()
        self.assertTrue(session_folder.exists())
        data_files = list(session_folder.glob('*.nix'))
        self.assertEqual(len(data_files), len(runs) * len(tasks) * len(nix_files))

        for data_file in data_files:
            self.assertTrue(data_file.name.find("_ephys"))

        for run in runs:
            exp = len(tasks) * len(nix_files)
            files = list(session_folder.glob(f'*_run-{run}*.nix'))
            self.assertEqual(len(files), exp)

        for task in tasks:
            exp = len(runs) * len(nix_files)
            files = list(session_folder.glob(f'*_task-{task}*.nix'))
            self.assertEqual(len(files), exp)

        for split in range(len(nix_files)):
            exp = len(runs) * len(tasks)
            files = list(session_folder.glob(f'*_split-{split}*.nix'))
            self.assertEqual(len(files), exp)

    def test_data_files_same_key(self):
        self.ando_data.generate_structure()
        nix_files = [self.test_data_files[0]]
        run = 'run1'
        task = 'task1'

        self.ando_data.register_data_files(*nix_files, run=run, task=task)
        # register more data files in a second step
        self.ando_data.register_data_files(*nix_files, run=run, task=task)

        self.ando_data.generate_data_files()

        session_folder = self.ando_data.get_data_folder()
        self.assertTrue(session_folder.exists())
        data_files = list(session_folder.glob('*.nix'))
        self.assertEqual(len(data_files), 2)

        for data_file in data_files:
            self.assertTrue(data_file.name.find(f"_task-{task}_run-{run}_split-"))

    def test_metadata_files(self):
        self.ando_data.generate_structure()
        self.ando_data.register_metadata_files(*self.test_mdata_files)
        self.ando_data.generate_metadata_files()
        self.ando_data.create_metadata_file_participants()
        self.ando_data.create_metadata_file_tasks()

        prefix = 'sub-sub5_ses-ses1'
        for f in [prefix + '_probes.tsv', prefix + '_contacts.json']:
            self.assertTrue((self.ando_data.get_data_folder() / f).exists())
        self.assertTrue((self.basedir / 'dataset_description.json').exists())
        self.assertTrue((self.basedir / 'participants.json').exists())
        self.assertTrue((self.basedir / 'participants.tsv').exists())
        self.assertTrue((self.basedir / 'tasks.json').exists())
        self.assertTrue((self.basedir / 'tasks.tsv').exists())

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
        generate_struct(self.csv_file, test_directory)

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

