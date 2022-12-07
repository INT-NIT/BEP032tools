import os
import tempfile
import shutil
import pathlib
test_directory = pathlib.Path(tempfile.gettempdir()) / 'bep032tools_testfiles'


def initialize_test_directory(clean=True):
    """
    Create main test folder if required

    Parameters
    ----------
    clean: (bool)
        Remove test folder first in case it exists.

    Returns
    -------
    test_directory: (str)
        path of the test directory
    """
    if clean and os.path.exists(test_directory):
        shutil.rmtree(test_directory)

    if not os.path.exists(test_directory):
        os.mkdir(test_directory)
    packaged_testfolder = pathlib.Path(__file__).parent / 'test_files'
    shutil.copytree(packaged_testfolder, test_directory / 'test_files')

    return test_directory



def generate_example_csv_file(mode='simple'):
    """
    Create csv file containing parameters for the creation of multiple BEP032 structures

    Returns
    -------
    file_path: (str)
        path of the generated file
    """
    file_path = os.path.join(test_directory, 'example.csv')
    if mode == 'simple':
        with open(file_path, 'w+') as f:
            csv_lines = \
                "sub_id,ses_id\n" \
                "enya,20200101\n" \
                "enya,20200101\n" \
                "enya,20200101\n" \
                "zamba,20200102\n" \
                "zamba,20200102\n" \
                "zimba,20200103\n" \
                "zimba,20200104"
            f.writelines(csv_lines)

    elif mode == 'full':
        with open(file_path, 'w+') as f:
            csv_lines = \
                "sub_id,ses_id,data_source,run,task\n" \
                "mouse-A,2000-01-01,my_data_file_0.nix,1,running\n" \
                "mouse-A,2000-01-01,my_data_file_1.nix,2,running\n" \
                "mouse-B,2000-01-01,my_data_file_2.nix,0,rest\n" \
                "mouse-B,2000-01-01,my_data_file_3.nix,,walk\n"
            f.writelines(csv_lines)

        for i in range(4):
            pathlib.Path(f'my_data_file_{i}.nix').touch()

    else:
        raise ValueError(f'unknown mode {mode}')

    return file_path
