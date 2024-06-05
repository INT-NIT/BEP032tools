from pathlib import Path
import os
from pandas import read_csv
import elab_bridge
import json
from elab_bridge import server_interface
from BidsEmptyRepositoryGenerator import Generator

import argparse


def main(config_file_path, output_dir_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    csv_file = os.path.join(output_dir_path, 'fichier.csv')

    jsonformat = elab_bridge.server_interface.download_experiment(csv_file,
                                                                  config_file_path, 247,
                                                                  format='csv')
    df = read_csv(csv_file)

    generator = Generator(output_dir_path, df['id'][0], df['session_id'][0], "micr")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to process configuration and output paths")
    parser.add_argument('config_path', type=str,
                        help='Path to the configuration file (JSON format)')
    parser.add_argument('output_path', type=str, help='Path to the output folder')

    args = parser.parse_args()

    main(args.config_path, args.output_path)
