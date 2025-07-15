"""
BidsEmptyRepositoryGenerator.py

This module generates an empty BIDS (Brain Imaging Data Structure) repository structure.
It creates the required directory and file layout for initializing new BIDS-compliant datasets.

Main Features:
- Automates creation of empty BIDS directory and file structures.
- Supports customization of subject, session, and modality.
- Integrates with BIDSTools components for directory and file management.

Typical Usage:
    from BIDSTools.BidsEmptyRepositoryGenerator import Generator
    generator = Generator(output="/path/to/output", sub_id=1, session_id=1, modality="micr")

Refer to the BIDS specification for repository initialization guidelines.
"""
import sys
from BIDSTools.Createfile import CreatFile
from BIDSTools.Createdirectory import Createdirectory


class Generator:
    def __init__(self, output, sub_id=1, session_id=1, modality=None):
        """
        Initialize a Generator object.

        Args:
            output (str): The output folder path.
            sub_id (int): Subject ID.
            session_id (int): Session ID.
            modality (str, optional): The modality name.
        """
        self.output = output
        self.modality = modality.strip() if modality else None
        if self.modality:
            self.directory_builder = Createdirectory(output, sub_id, session_id, self.modality)
            self.file_builder = CreatFile(output)
            self.generate()
        else:
            print("No modality provided. Please specify a modality.")

    def generate(self):
        """Generate files and directories."""
        self.directory_builder.build()
        self.file_builder.build()


if __name__ == "__main__":
    pass
