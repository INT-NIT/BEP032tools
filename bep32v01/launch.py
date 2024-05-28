from pathlib import Path
import os
from pandas import read_csv
import elab_bridge
import json
from elab_bridge import server_interface
from BidsEmptyRepositoryGenerator import Generator
from diglab_utils.test_utils import (test_directory, initialize_test_dir)
import argparse

project_dir = test_directory / 'test files_elab' / 'TestProject'
SERVER_CONFIG_YAML = ('elab_bridge/tests/'
                      'testfiles_elab/TestProject/project'
                      '.json')
chemin_fichier_yaml = os.path.join(elab_bridge.__path__[0], SERVER_CONFIG_YAML)
chemin_fichier_yaml = "tests/testfiles_elab/TestProject/project/server_config.yml"

# Construire le chemin absolu vers le fichier YAML
chemin_absolu_fichier_yaml = os.path.join(elab_bridge.__path__[0], chemin_fichier_yaml)


def main(config_path, output_path):
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Utiliser le chemin du fichier de configuration passé en argument
    json_path = config_path
    print(json_path)

    # Utiliser le chemin de sortie passé en argument
    output = output_path
    print(output)

    csv_file = os.path.join(output, 'fichier.csv')

    jsonformat = elab_bridge.server_interface.download_experiment(csv_file,
                                                                  json_path, 247, format='csv')
    df = read_csv(csv_file)
    print(df)
    generator = Generator(output, df['id'][0], df['session_id'][0], "micr")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to process configuration and output paths")
    parser.add_argument('config_path', type=str,
                        help='Path to the configuration file (JSON format)')
    parser.add_argument('output_path', type=str, help='Path to the output folder')

    args = parser.parse_args()

    main(args.config_path, args.output_path)
