import json
import os

from bids import BIDSLayout

from pathlib import Path


def create_dir(output_path):
    if not Path(output_path).exists():
        os.makedirs(output_path)


def create_dir_for_file(file: str):
    output_path = os.path.dirname(os.path.abspath(file))
    create_dir(output_path)


def get_bidsname_config(config_file="") -> dict:
    """
    See the Path construction demo in the pybids tuto
    https://github.com/bids-standard/pybids/blob/master/examples/pybids_tutorial.ipynb
    """
    default = "config_bidsname.json"
    return get_config(config_file, default)


def get_pybids_config(config_file="") -> dict:
    """
    Pybids configs are stored in the layout module
    https://github.com/bids-standard/pybids/tree/master/bids/layout/config

    But they don't cover the ``ephys`` so we are using modified config, that
    should cover both ephys and microscopy.

    TODO the "default_path_patterns" of that config has not been extended for
    ephys or microscopy yet
    """
    default = "config_pybids.json"
    return get_config(config_file, default)


def get_config(config_file="", default="") -> dict:

    if config_file == "" or not Path(config_file).exists():
        my_path = os.path.dirname(os.path.abspath(__file__))
        config_file = os.path.join(my_path, default)

    if config_file == "" or not Path(config_file).exists():
        return
    with open(config_file, "r") as ff:
        return json.load(ff)


def init_layout(target_dir: str, pybids_config_file=""):

    create_dir(target_dir)

    if pybids_config_file == "":
        pybids_config_file = get_pybids_config()
    layout = BIDSLayout(target_dir, validate=False, config=pybids_config_file)

    return layout


def get_ephys_filename(layout, entities: dict, bidsname_config=""):

    bids_name_config = get_bidsname_config(bidsname_config)
    output_file = layout.build_path(
        entities, bids_name_config["ephys_file"], validate=False
    )

    return output_file


# TODO function to generate scans and sessoins TSV filenames
