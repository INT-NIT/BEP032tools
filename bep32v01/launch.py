from pathlib import Path

from pandas import read_csv

import elab_bridge
import json
from elab_bridge import server_interface
from BidsEmptyRepositoryGenerator import Generator
import os
from elab_bridge import *
from diglab_utils.test_utils import (test_directory, initialize_test_dir)

project_dir = test_directory / 'test files_elab' / 'TestProject'
SERVER_CONFIG_YAML = ('elab_bridge/tests/'
                      'testfiles_elab/TestProject/project'
                      '.json')
chemin_fichier_yaml = os.path.join(elab_bridge.__path__[0], SERVER_CONFIG_YAML)
chemin_fichier_yaml = "tests/testfiles_elab/TestProject/project/server_config.yml"

# Construire le chemin absolu vers le fichier YAML
chemin_absolu_fichier_yaml = os.path.join(elab_bridge.__path__[0], chemin_fichier_yaml)

h = "/home/INT/idrissou.f/PycharmProjects/BEP032tools/elabConf.json"


def main():
    output = input(
        "Enter the output folder path:  :"
        " ex :/home/INT/idrissou.f/PycharmProjects/BEP032tools/bep32v01/Essaie")

    csv_file = os.path.join(output, 'fichier.csv')

    jsonformat = elab_bridge.server_interface.download_experiment(csv_file,
                                                                  h, 247, format='csv')
    df = read_csv(csv_file)

    generator = Generator(output, df['id'][0], df['session_id'][0], "micr")


if __name__ == "__main__":
    main()
