import os
import tempfile
import shutil

test_directory = os.path.join(tempfile.gettempdir(), 'ando_testfiles')

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

    return test_directory



def generate_simple_csv_file():
    """
    Create csv file containing parameters for the creation of multiple AnDO structures

    Returns
    -------
    file_path: (str)
        path of the generated file
    """
    file_path = os.path.join(test_directory, 'example.csv')
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

    return file_path

