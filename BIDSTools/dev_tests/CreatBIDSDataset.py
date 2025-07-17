""" CreatBIDSDataset.py

This script demonstrates how to load metadata from an elab source and generate a BIDS-compliant dataset.
It takes as input the path to a configuration file and an output directory, processes metadata from a CSV file, and creates a BIDS repository structure with example experiments.

Main Features:
- Downloads and processes metadata from elab via CSV.
- Creates a BIDS repository and test directory structure.
- Serves as a practical example of BIDSTools package usage.

Typical Usage:
    python CreatBIDSDataset.py --config <config_file_path> --output <output_dir_path>

Dependencies:
- pandas
- elab_bridge
- BIDSTools submodules

See the BIDSTools documentation for more advanced usage and customization.
"""

from pathlib import Path
import os
from pandas import read_csv
import elab_bridge
import json
from elab_bridge import server_interface
from BIDSTools.BidsEmptyRepositoryGenerator import Generator
from BIDSTools.WriteModalityAgnosticBIDSMetadataFiles import *
import argparse


def main(config_file_path, output_dir_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    csv_file = os.path.join(output_dir_path, '../elab_data.csv')

    jsonformat = elab_bridge.server_interface.extended_download(csv_file,
                                                                config_file_path,
                                                                ["FF"],
                                                                format='csv')



    with open("/BIDSTools/dev_tests/ffffff.json", 'w', encoding='utf-8') as f:
        json.dump(jsonformat, f, indent=4)
    df = read_csv(csv_file)


    print(df)



if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to process configuration and output paths")
    parser.add_argument('config_path', type=str,
                        help='Path to the configuration file (JSON format)')
    parser.add_argument('output_path', type=str, help='Path to the output folder')

    args = parser.parse_args()

    main(args.config_path, args.output_path)
