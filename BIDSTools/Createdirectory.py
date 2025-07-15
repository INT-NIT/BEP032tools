"""
Createdirectory.py

This module defines the Createdirectory class, which automates the creation of directory layouts compliant with the BIDS (Brain Imaging Data Structure) directory structure.

Main Features:
- Generates a BIDS-compliant directory tree for neuroimaging datasets.
- Supports customization of subject ID, session ID, and modality.
- Integrates with other BIDSTools components for file and entity management.

Typical Usage:
    creator = Createdirectory(output_path, sub_id=1, session_id=1, modality="micr")
    creator.create_directories()
    Example of outuput:
    sub-1
    └─ ses-1
        └─ micr



Refer to the BIDS specification for directory organization guidelines.
"""
import json
import os
from BIDSTools.BidsFilestructure import FileStructure
from BIDSTools.BidsDirectoryStructure import DirectoryStructure
from BIDSTools.BidsEntity import Entity
from BIDSTools.BidsDatatype import DataTypes
from pathlib import Path


class Createdirectory:
    def __init__(self, output_path, sub_id=1, session_id=1, modality="micr"):
        """
        Initialize a Createdirectory object with output path, subject ID, session ID, and modality.

        Args:
            output_path (str): The path where directories will be created.
            sub_id (int): Subject ID.
            session_id (int): Session ID.
            modality (str): Modality name.
        """
        self.session_path = None
        self.output_path = output_path
        self.dir_name = []
        self.filestructure = FileStructure()
        self.filestructure.get_detail()
        self.directorystructure = DirectoryStructure()
        self.entity = Entity()
        self.dataType = DataTypes()
        self.sub_id = sub_id
        self.session_id = session_id
        self.modality = modality
        sub_directory = []

    def layout_folder(self):
        """
        Create directory layout based on BIDS directory structure.
        """
        top_level_dir = self.directorystructure.get_top_level_directory()
        entity_dir = self.directorystructure.get_entity_directory()
        value_dir = self.directorystructure.get_value_directory()
        all_dir = self.directorystructure.get_all_directory()
        for dir in all_dir:

            path = ""
            if dir in top_level_dir:
                if dir in entity_dir:
                    path = self.entity.get_entity_name(dir) + f'-{str(self.sub_id)}'

                elif dir in value_dir:
                    path = self.dataType.get_data_type_value(dir)

                else:
                    path = dir

                self.dir_name.append(path)

    def build(self):
        """
        Build the directory structure.
        """
        for dir in self.dir_name:
            first_level_dir = os.path.join(self.output_path, dir)
            if not os.path.exists(first_level_dir):
                os.makedirs(first_level_dir)

        # subdirectory session
        subject_dir = os.path.join(self.output_path, f'sub-{self.sub_id}')
        session_dir = os.path.join(subject_dir, f'ses-{self.session_id}')
        if not os.path.exists(session_dir):
            os.makedirs(session_dir)
        # subdirectory_modality
        modality_dir = os.path.join(session_dir, self.modality)
        if not os.path.exists(modality_dir):
            os.makedirs(modality_dir)


def main():
    """
    Main function to create directory layout.
    """
    output_path = "Essaie"  # Change this to your desired output path
    creator = Createdirectory(output_path)
    creator.layout_folder()
    creator.build()


if __name__ == "__main__":
    main()
