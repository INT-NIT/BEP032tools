from pathlib import Path
import os
from pandas import read_csv
import elab_bridge
import json
from elab_bridge import server_interface
from BidsEmptyRepositoryGenerator import Generator
from writing_agnosticfile import *
import argparse


def main(config_file_path, output_dir_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    csv_file = os.path.join(output_dir_path, 'elab_data.csv')

    jsonformat = elab_bridge.server_interface.extended_download(csv_file,
                                                                config_file_path, ["TEST_EEG"],
                                                                format='csv')
    df = read_csv(csv_file)
    print(df['sex'][0])
    print(df['id'][0])
    generator = Generator(output_dir_path, df['id'][0], df['session_id'][0], "micr")

    additional_kwargs = {
        "Name": "My Dataset",
        "BIDSVersion": "1.3.1",
        "HEDVersion": "7.0",
        "age": str(df['age'][0]),
        "sex": str(df['sex'][0]),
        "participant_id": str(df['id'][0])
    }
    print(additional_kwargs)
    fill_agnostic_file(output_dir_path, **additional_kwargs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to process configuration and output paths")
    parser.add_argument('config_path', type=str,
                        help='Path to the configuration file (JSON format)')
    parser.add_argument('output_path', type=str, help='Path to the output folder')

    args = parser.parse_args()

    main(args.config_path, args.output_path)
