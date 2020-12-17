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
            "experiments_name,subjects_names,years,months,days,sessions_numbers,comments\n" \
            "neo,enya,2020,12,01,001,protocol-v1\n" \
            "neo,enya,2020,12,01,002,protocol-v2\n" \
            "neo,enya,2020,02,01,003,protocol-v1\n" \
            "neo,zamba,2020,12,12,001,vsdi\n" \
            "neo,zamba,2020,2,3,010,vsdi\n" \
            "aerial,zimba,2020,12,06,001,ephys-acute\n" \
            "aerial,zimba,2020,12,01,010,ephys-chronic"
        f.writelines(csv_lines)

    return file_path

