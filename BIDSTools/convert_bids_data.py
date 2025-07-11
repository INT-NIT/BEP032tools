"""
This module provides the `ConvertBIDSData` class, which is an abstract base class, and the `ConvertedfSData` class, which is a subclass of `ConvertBIDSData`.
ConvertedfSData is used to convert EDF data to BIDS format.
"""
import os
import shutil
from abc import ABC, abstractmethod
from eye2bids.edf2bids import edf2bids
import tempfile


class ConvertBIDSData(ABC):
    def __init__(self, raw_data):
        self.raw_data = raw_data

    @abstractmethod
    def convert_bids_data(self):
        """Convert BIDS data. Must be overridden in subclasses."""
        pass


class ConvertedfSData(ConvertBIDSData):
    def __init__(self, raw_data, metadata, path_to_store_convertfile):
        super().__init__(raw_data)

        # Validate the raw data file extension
        basename, extension = os.path.splitext(raw_data)
        if extension.lower() != '.edf':
            raise ValueError("Check the raw data file extension; it must be '.edf'")

        self.raw_data = raw_data

        # Validate the metadata file extension
        basename, extension = os.path.splitext(metadata)
        if extension.lower() != '.yml':
            raise ValueError("Check the metadata file extension; it must be '.yml'")

        self.metadata = metadata
        self.path_to_store_convertfile = path_to_store_convertfile

    def convert_bids_data(self):
        # Call the conversion function
        # add a tmp dir to store the converted file
        with tempfile.TemporaryDirectory() as tmpdirname:
            edf2bids(self.raw_data, self.metadata, tmpdirname)
            for file in os.listdir(tmpdirname):
                shutil.move(os.path.join(tmpdirname, file),
                            os.path.join(self.path_to_store_convertfile, file))


if __name__ == "__main__":
    # Define your parameters
    raw_data = "/path/to/your/file.edf"  # Path to the raw EDF data file
    metadata = "/path/to/your/metadata.yml"  # Path to the metadata YAML file
    output_dir = "/path/to/store/converted/file"  # Directory to store converted files

    # Instantiate the converter for EDF data
    edf_converter = ConvertedfSData(raw_data, metadata, output_dir)
    edf_converter.convert_bids_data()
