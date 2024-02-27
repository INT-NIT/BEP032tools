import os
import tempfile
import shutil
import pathlib


def initialize_test_directory(clean=True):
    """
    Creates the main test directory if necessary.

    Parameters
    ----------
    clean: (bool)
        Removes the test directory first if it exists.

    Returns
    -------
    test_directory: (str)
        Path of the test directory.
    """
    # Retrieve the system temporary directory
    temp_dir = tempfile.gettempdir()

    # Full path of the test directory
    test_directory = os.path.join(temp_dir, 'bep032_test_files')

    # Removes the existing directory if it exists and clean is True
    if clean and os.path.exists(test_directory):
        shutil.rmtree(test_directory)

    # Creates the test directory if it does not exist yet
    if not os.path.exists(test_directory):
        os.mkdir(test_directory)

    return pathlib.Path(test_directory)


# Example of usage:
if __name__ == "__main__":
    initialize_test_directory()
