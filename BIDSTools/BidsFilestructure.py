"""
BidsFilestructure.py

This module loads and manages file structures defined by the BIDS (Brain Imaging Data Structure) standard.
It provides utilities to retrieve, inspect, and validate BIDS file structures from YAML schemas.

Main Features:
- Loads all BIDS file structure rules from YAML configuration files.
- Provides access to file names, directory levels, and file details.
- Facilitates validation and inspection of file structures for BIDS compliance.

Typical Usage:
    from BIDSTools.BidsFilestructure import FileStructure
    fs = FileStructure()
    print(fs.all_files)

Refer to the BIDS specification for file structure guidelines.
"""

import yaml

import os
from BIDSTools.resource_paths import CORE_FILES_YAML, DIRECTORIES_YAML, FILES_YAML, TABLES_YAML

class FileStructure:
    def __init__(self, relative_path=CORE_FILES_YAML):
        """
        Initialize a FileStructure object with a relative path to a YAML file.

        Args:
            relative_path (str): The relative path to the YAML file containing file structure rules.
        """
        self.relative_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), relative_path)

        self.all_files = []
        self.top_level_files = []
        self.top_level_directory = []
        self.top_level_file_details = {}
        self.top_level_directory_detail = {}
        self.get_detail()

    def get_all_files(self):
        """
        Retrieve all file names from the YAML file containing file structure rules.
        """

        with open(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                               FILES_YAML), 'r') as file:

            file_rules = yaml.safe_load(file)
            if file_rules:
                for key in file_rules:
                    self.all_files.append(key)
                    if file_rules.get(key).get("file_type") == "regular":
                        self.top_level_files.append(key)
                    else:
                        self.top_level_directory.append(key)

    def get_all_files_detail(self, relative_path):
        """
        Retrieve details for all files and directories from a specified YAML file.

        Args:
            relative_path (str): The relative path to the YAML
            file containing file structure details.
        """
        with open(relative_path, 'r') as file:
            file_rules = yaml.safe_load(file)
            if file_rules:
                for key, value in file_rules.items():
                    if key in self.top_level_files:
                        self.top_level_file_details[key] = value
                    else:
                        self.top_level_directory_detail[key] = value

    def get_detail(self):
        """
        Retrieve file structure details and store them in class attributes.
        """
        self.get_all_files()
        self.get_all_files_detail(self.relative_path)
        self.get_all_files_detail(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                               TABLES_YAML))
        return self

    def get_detail_for_file(self, file_name):
        """
        Retrieve details for a specific file.

        Args:
            file_name (str): The name of the file.

        Returns:
            dict: Details of the file.
        """
        return self.top_level_file_details.get(file_name)

    def get_detail_for_directory(self, directory_name):
        """
        Retrieve details for a specific directory.

        Args:
            directory_name (str): The name of the directory.

        Returns:
            dict: Details of the directory.
        """
        return self.top_level_directory_detail.get(directory_name)

    # Attributes Getters
    def get_relative_path(self):
        """
        Get the relative path to the YAML file containing file structure rules.

        Returns:
            str: The relative path.
        """
        return self.relative_path

    def get_all_files_list(self):
        """
        Get the list of all files.

        Returns:
            list: List of all file names.
        """
        return self.all_files

    def get_top_level_files_list(self):
        """
        Get the list of top-level files.

        Returns:
            list: List of top-level file names.
        """
        return self.top_level_files

    def get_top_level_directory_list(self):
        """
        Get the list of top-level directories.

        Returns:
            list: List of top-level directory names.
        """
        return self.top_level_directory

    def get_top_level_file_details(self):
        """
        Get details of top-level files.

        Returns:
            dict: Dictionary containing details of top-level files.
        """
        return self.top_level_file_details

    def get_top_level_directory_details(self):
        """
        Get details of top-level directories.

        Returns:
            dict: Dictionary containing details of top-level directories.
        """
        return self.top_level_directory_detail


def main():
    """
    Main function to demonstrate the usage of the FileStructure class.
    """
    file_structure = FileStructure()
    file_structure.get_detail()
    print(file_structure.all_files)


if __name__ == "__main__":
    main()
