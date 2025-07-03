from pathlib import Path
import os
from pandas import read_csv
import elab_bridge
import json
from elab_bridge import server_interface
from BIDSTools.BidsEmptyRepositoryGenerator import Generator
from BIDSTools.WritingModalityAgnosticsFiles import *
import argparse


def main(config_file_path, output_dir_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    csv_file = os.path.join(output_dir_path, 'elab_data.csv')

    jsonformat = elab_bridge.server_interface.extended_download(csv_file,
                                                                config_file_path,
                                                                ["FF"],
                                                                format='csv')

    print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
    print(jsonformat)
    print("kkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkkk")
    print(type(jsonformat))

    with open("/home/INT/idrissou.f/PycharmProjects/BEP032tools/BIDSTools/ffffff.json", 'w', encoding='utf-8') as f:
        json.dump(jsonformat, f, indent=4)
    df = read_csv(csv_file)


    print(df)

    """for i in range(len(df)):
        generator = Generator(output_dir_path, df['id'][i], df['session_id'][i], "micr")
        additional_kwargs = {
            "Name": "My Dataset",
            "BIDSVersion": "1.3.1",
            "HEDVersion": "7.0",
            "age": str(df['age'][i]),
            "sex": str(df['sex'][i]),
            "participant_id": str(df['id'][i])
        }
        fill_agnostic_file(output_dir_path, **additional_kwargs)
        print(additional_kwargs)"""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to process configuration and output paths")
    parser.add_argument('config_path', type=str,
                        help='Path to the configuration file (JSON format)')
    parser.add_argument('output_path', type=str, help='Path to the output folder')

    args = parser.parse_args()

    main(args.config_path, args.output_path)
