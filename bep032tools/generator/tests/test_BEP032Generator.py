import os
import unittest
from parameterized import parameterized
from pathlib import Path
import numpy as np

from bep032tools.generator.tests.utils import (initialize_test_directory, test_directory,
                                               generate_simple_csv_file)
from bep032tools.generator.BEP032Generator import BEP032Data, extract_structure_from_csv


class Test_BEP032Data_ece(unittest.TestCase):
    '''
    Test class for a typical extra-cellular ephys (ece) data set.
    In particular, ses_id is defined, and a session-level directory is used in the BIDS hierarchy
    '''

    def setUp(self):
        self.test_dir = Path(initialize_test_directory(clean=True))
        self.sub_id = 'sub5'
        self.ses_id = 'ses1'
        self.tasks = None
        self.runs = None
        
        sources = self.test_dir / 'sources'
        sources.mkdir()
        project = self.test_dir / 'project-A'
        project.mkdir()
        self.basedir = project

        d = BEP032Data(self.sub_id, self.ses_id)
        d.basedir = project

        self.bep032tools_data = d
        prefix = f'sub-{self.sub_id}_ses-{self.ses_id}'
        self.test_data_files = [sources / (prefix + '_ephy.nix'),
                                sources / (prefix + '_ephy.nwb')]
        self.test_mdata_files = [sources / 'dataset_description.json',
                                 sources / (prefix + '_probes.tsv'),
                                 sources / (prefix + '_contacts.json')]

        for f in self.test_mdata_files + self.test_data_files:
            f.touch()

        # create fake ascii dataset
        sample_data = np.random.uniform(size=(200, 3))
        self.ascii_data_filename = sources / "test_ascii_data.txt"
        np.savetxt(str(self.ascii_data_filename), sample_data, delimiter='\t')

    def test_get_data_folder(self):
        df = self.bep032tools_data.get_data_folder()
        self.assertTrue(df)

        df_abs = self.bep032tools_data.get_data_folder('absolute')
        df_local = self.bep032tools_data.get_data_folder('local')

        self.assertTrue(df_local)
        self.assertTrue(str(df_abs).endswith(str(df_local)))

    def test_generate_structure(self):
        self.bep032tools_data.generate_directory_structure()
        df = self.bep032tools_data.get_data_folder()
        self.assertTrue(df.exists())

    def test_data_files(self):
        self.bep032tools_data.generate_directory_structure()
        self.bep032tools_data.register_data_sources(*self.test_data_files)
        self.bep032tools_data.organize_data_files()

        session_folder = self.bep032tools_data.get_data_folder()
        self.assertTrue(session_folder.exists())
        data_files = list(session_folder.glob('*.nix'))
        data_files += list(session_folder.glob('*.nwb'))
        self.assertEqual(len(self.test_data_files), len(data_files))
        for data_file in data_files:
            self.assertTrue(data_file.name.find("_ephys"))

    @parameterized.expand([('nix'),('nwb')])
    def test_data_file_conversion(self, format):
        self.bep032tools_data.generate_directory_structure()
        self.bep032tools_data.register_data_sources(self.ascii_data_filename)

        # testing conversion to nix
        self.bep032tools_data.organize_data_files(autoconvert=format)

        observed_files = list(self.bep032tools_data.get_data_folder().glob(f'*.{format}'))
        self.assertTrue(len(observed_files) == 1)

        # check file content
        import neo
        if format == 'nix':
            ioclass = neo.NixIOFr
        else:
            ioclass = neo.NWBIO
        io = ioclass(str(observed_files[0]))
        block = io.read_block()

        expected_data = np.loadtxt(self.ascii_data_filename)
        anasigs = block.segments[0].analogsignals
        self.assertEqual(len(anasigs), expected_data.shape[-1])
        # compare data of first channel
        np.testing.assert_array_almost_equal(anasigs[0].magnitude, expected_data[:, 0:1])
        # compare first samples across channels
        for channel_idx, channel in enumerate(anasigs):
            self.assertEqual(channel[0].magnitude, expected_data[0, channel_idx])
        os.remove(observed_files[0])

    def test_data_file_conversion_multi_split(self):
        self.bep032tools_data.generate_directory_structure()

        format = 'nix'
        # testing conversion to nix
        self.bep032tools_data.register_data_sources(*[self.ascii_data_filename]*3)
        self.bep032tools_data.organize_data_files(autoconvert=format)

        observed_files = list(self.bep032tools_data.get_data_folder().glob(f'*.{format}'))
        self.assertTrue(len(observed_files) == 3)
        for observed_file in observed_files:
            os.remove(observed_file)

    # This test currently fails due to https://github.com/NeuralEnsemble/python-neo/issues/1198'
    # def test_data_file_conversion_source_folder(self):
    #     self.bep032tools_data.generate_directory_structure()
    #
    #     format = 'nix'
    #
    #     # download example source folder
    #     import requests
    #     URL = 'https://gin.g-node.org/NeuralEnsemble/ephy_testing_data/raw/' \
    #           '5dbd759ca6048ac89695c35a679c78c79f618d74/neuralynx/Cheetah_v6.4.1dev/' \
    #           'original_data/CSC1_truncated.ncs'
    #     neuralynx_folder = self.test_dir / "sources" / "neuralynx_recording_session"
    #     neuralynx_folder.mkdir()
    #     with open(neuralynx_folder / "CSC1_truncated.ncs", "wb") as f:
    #         f.write(requests.get(URL).content)
    #
    #     # testing conversion to nix
    #     self.bep032tools_data.register_data_sources(neuralynx_folder)
    #     self.bep032tools_data.organize_data_files(autoconvert=format)
    #
    #     observed_files = list(self.bep032tools_data.get_data_folder().glob(f'*.{format}'))
    #     self.assertTrue(len(observed_files) == 1)
    #     for observed_file in observed_files:
    #         os.remove(observed_file)

    def test_data_files_complex(self):
        self.bep032tools_data.generate_directory_structure()
        nix_files = [self.test_data_files[0]] * 3
        runs = ['run1', 'run2']
        tasks = ['task1', 'task2']
        for run in runs:
            for task in tasks:
                self.bep032tools_data.register_data_sources(*nix_files, run=run, task=task)

        self.bep032tools_data.organize_data_files()

        session_folder = self.bep032tools_data.get_data_folder()
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
        self.bep032tools_data.generate_directory_structure()
        nix_files = [self.test_data_files[0]]
        run = 'run1'
        task = 'task1'

        self.bep032tools_data.register_data_sources(*nix_files, run=run, task=task)
        # register more data files in a second step
        self.bep032tools_data.register_data_sources(*nix_files, run=run, task=task)

        self.bep032tools_data.organize_data_files()

        session_folder = self.bep032tools_data.get_data_folder()
        self.assertTrue(session_folder.exists())
        data_files = list(session_folder.glob('*.nix'))
        self.assertEqual(len(data_files), 2)

        for data_file in data_files:
            self.assertTrue(data_file.name.find(f"_task-{task}_run-{run}_split-"))

    def test_implemented_error_raised(self):
        path = ""
        with self.assertRaises(NotImplementedError):
            self.bep032tools_data.generate_metadata_file_sessions(path)
        with self.assertRaises(NotImplementedError):
            self.bep032tools_data.generate_metadata_file_tasks(path)
        with self.assertRaises(NotImplementedError):
            self.bep032tools_data.generate_metadata_file_dataset_description(path)
        with self.assertRaises(NotImplementedError):
            self.bep032tools_data.generate_metadata_file_participants(path)
        with self.assertRaises(NotImplementedError):
            self.bep032tools_data.generate_metadata_file_probes(path)
        with self.assertRaises(NotImplementedError):
            self.bep032tools_data.generate_metadata_file_channels(path)
        with self.assertRaises(NotImplementedError):
            self.bep032tools_data.generate_metadata_file_contacts(path)
        with self.assertRaises(NotImplementedError):
            self.bep032tools_data.generate_all_metadata_files()

    def tearDown(self):
        initialize_test_directory(clean=True)


class Test_BEP032Data_ice(unittest.TestCase):
    '''
    Test class for a typical intra-cellular ephys (ice) data set.
    In particular, ses_id is not defined, and there is no session-level directory in the BIDS hierarchy
    '''
    def setUp(self):
        test_dir = Path(initialize_test_directory(clean=True))
        self.sub_id = 'sub5'
        self.tasks = None
        self.runs = None

        sources = test_dir / 'sources'
        sources.mkdir()
        project = test_dir / 'project-A'
        project.mkdir()
        self.basedir = project

        d = BEP032Data(self.sub_id)
        d.basedir = project

        self.bep032tools_data = d
        prefix = f'sub-{self.sub_id}'
        self.test_data_files = [sources / (prefix + '_ephy.nix'),
                                sources / (prefix + '_ephy.nwb')]
        self.test_mdata_files = [sources / 'dataset_description.json',
                                 sources / (prefix + '_probes.tsv'),
                                 sources / (prefix + '_contacts.json')]

        for f in self.test_mdata_files + self.test_data_files:
            f.touch()

        # create fake ascii dataset
        sample_data = np.random.uniform(size=(200, 3))
        self.ascii_data_filename = sources / "test_ascii_data.txt"
        np.savetxt(str(self.ascii_data_filename), sample_data, delimiter='\t')

    def test_get_data_folder(self):
        df = self.bep032tools_data.get_data_folder()
        self.assertTrue(df)

        df_abs = self.bep032tools_data.get_data_folder('absolute')
        df_local = self.bep032tools_data.get_data_folder('local')

        self.assertTrue(df_local)
        self.assertTrue(str(df_abs).endswith(str(df_local)))

    def test_generate_structure(self):
        self.bep032tools_data.generate_directory_structure()
        df = self.bep032tools_data.get_data_folder()
        self.assertTrue(df.exists())

    def test_data_files(self):
        self.bep032tools_data.generate_directory_structure()
        self.bep032tools_data.register_data_sources(*self.test_data_files)
        self.bep032tools_data.organize_data_files()

        session_folder = self.bep032tools_data.get_data_folder()
        self.assertTrue(session_folder.exists())
        data_files = list(session_folder.glob('*.nix'))
        data_files += list(session_folder.glob('*.nwb'))
        self.assertEqual(len(self.test_data_files), len(data_files))
        for data_file in data_files:
            self.assertTrue(data_file.name.find("_ephys"))

    @parameterized.expand([('nix'),('nwb')])
    def test_data_file_conversion(self, format):
        self.bep032tools_data.generate_directory_structure()
        self.bep032tools_data.register_data_sources(self.ascii_data_filename)

        # testing conversion to nix
        self.bep032tools_data.organize_data_files(autoconvert=format)

        observed_files = list(self.bep032tools_data.get_data_folder().glob(f'*.{format}'))
        self.assertTrue(len(observed_files) == 1)

        # check file content
        import neo
        if format == 'nix':
            ioclass = neo.NixIOFr
        else:
            ioclass = neo.NWBIO
        io = ioclass(str(observed_files[0]))
        block = io.read_block()

        expected_data = np.loadtxt(self.ascii_data_filename)
        anasigs = block.segments[0].analogsignals
        self.assertEqual(len(anasigs), expected_data.shape[-1])
        # compare data of first channel
        np.testing.assert_array_almost_equal(anasigs[0].magnitude, expected_data[:, 0:1])
        # compare first samples across channels
        for channel_idx, channel in enumerate(anasigs):
            self.assertEqual(channel[0].magnitude, expected_data[0, channel_idx])
        os.remove(observed_files[0])

    def test_data_files_complex(self):
        self.bep032tools_data.generate_directory_structure()
        nix_files = [self.test_data_files[0]] * 3
        runs = ['run1', 'run2']
        tasks = ['task1', 'task2']
        for run in runs:
            for task in tasks:
                self.bep032tools_data.register_data_sources(*nix_files,
                                                            run=run, task=task)

        self.bep032tools_data.organize_data_files()

        session_folder = self.bep032tools_data.get_data_folder()
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
        self.bep032tools_data.generate_directory_structure()
        nix_files = [self.test_data_files[0]]
        run = 'run1'
        task = 'task1'

        self.bep032tools_data.register_data_sources(*nix_files, run=run, task=task)
        # register more data files in a second step
        self.bep032tools_data.register_data_sources(*nix_files, run=run, task=task)

        self.bep032tools_data.organize_data_files()

        session_folder = self.bep032tools_data.get_data_folder()
        self.assertTrue(session_folder.exists())
        data_files = list(session_folder.glob('*.nix'))
        self.assertEqual(len(data_files), 2)

        for data_file in data_files:
            self.assertTrue(data_file.name.find(f"_task-{task}_run-{run}_split-"))

    def test_implemented_error_raised(self):
        path = ""
        with self.assertRaises(NotImplementedError):
            self.bep032tools_data.generate_metadata_file_sessions(path)
        with self.assertRaises(NotImplementedError):
            self.bep032tools_data.generate_metadata_file_tasks(path)
        with self.assertRaises(NotImplementedError):
            self.bep032tools_data.generate_metadata_file_dataset_description(path)
        with self.assertRaises(NotImplementedError):
            self.bep032tools_data.generate_metadata_file_participants(path)
        with self.assertRaises(NotImplementedError):
            self.bep032tools_data.generate_metadata_file_probes(path)
        with self.assertRaises(NotImplementedError):
            self.bep032tools_data.generate_metadata_file_channels(path)
        with self.assertRaises(NotImplementedError):
            self.bep032tools_data.generate_metadata_file_contacts(path)
        with self.assertRaises(NotImplementedError):
            self.bep032tools_data.generate_all_metadata_files()

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
        BEP032Data.generate_bids_dataset(self.csv_file, test_directory)
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


class Test_FolderGeneration(unittest.TestCase):

    def setUp(self):
        test_dir = Path(initialize_test_directory(clean=True))
        self.test_dir = test_dir / 'generateTest'  # this folder will not exist yet
        csv_filename = generate_simple_csv_file()
        self.csv_file = csv_filename

    def test_generate_folder(self):
        """
        Check that generation also works on non existing folders.
        """
        test_generate = False
        BEP032Data.generate_bids_dataset(self.csv_file, self.test_dir)
        if os.path.isdir(self.test_dir):
            test_generate = True
        self.assertTrue(test_generate)

    def test_no_duplicate_folder_generated(self):
        """
        Checks that there are no duplicates when generating folders.
        """
        BEP032Data.generate_bids_dataset(self.csv_file, self.test_dir)
        generation = False
        root_name = self.test_dir.name
        if not (self.test_dir / root_name).exists():
            generation = True
        self.assertTrue(generation)


if __name__ == '__main__':
    unittest.main()
