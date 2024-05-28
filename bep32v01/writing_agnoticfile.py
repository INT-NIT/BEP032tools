import csv
import json
import os
import warnings

import yaml

from bep32v01.agnostic_file_template import data_description_json_template, Citation_template, \
    Sample_template
from bep32v01.agnostic_file_template import participant_json_template

# Assign the data description template
data_description_template = data_description_json_template

data_participants_template = participant_json_template
# Path to the file containing the BIDS version
bidversion_path = 'ressources/schema/BIDS_VERSION'
bid_version_path = os.path.join('ressources/schema', 'BIDS_VERSION')

bid_version = "1.0.0"


# Initialize the bid_version variable by reading the content of the file


def extract_primary_key(template):
    """
    Extracts the primary keys from the provided template and includes the BIDS version.

    :param template: The template containing the data description.
    :return: A dictionary with primary keys and their requirement levels.
    """
    # Extract the primary keys and their requirement levels from the template

    primary_keys = {key: template[key]["Requirement Level"] for key in template.keys()}

    return primary_keys


def get_agnostic_file_arguments(template):
    """
    Extracts arguments from the template to be used for creating an agnostic file.

    :param template: The template containing the data description.
    :return: A dictionary with argument keys and default values.
    """
    return {key: None for key in template.keys()}


def write_agnostic_files(path_to_save, template, **kwargs):
    """
    Writes an agnostic file using the template and additional keyword arguments.

    :param path_to_save: The path where the file will be saved.
    :param template: The template containing the data description.
    :param kwargs: Additional keyword arguments to override template values.
    :return: A dictionary with the updated primary keys.
    """
    # Extract the primary keys from the template
    primary_keys = extract_primary_key(template)
    # Define the requirement levels
    Level1 = "REQUIRED"
    Level2 = "RECOMMENDED"
    Level3 = "OPTIONAL"

    # Override the primary keys with values provided in kwargs
    for key, value in kwargs.items():
        if key in primary_keys:
            primary_keys[key] = value

    # Check and warn about missing required, recommended, and optional fields
    for key, value in primary_keys.items():
        value_details = value.split()
        if Level1 in value_details:
            warnings.warn(f"Lack of required field for {key}")
        if Level2 in value_details:
            warnings.warn(f"Lack of recommended field for {key}")
        if Level3 in value_details:
            warnings.warn(f"Lack of optional field for {key}")

    # Save the primary keys to a file in JSON or TSV format
    if path_to_save.endswith('.json'):
        with open(path_to_save, 'w') as f:
            json.dump(primary_keys, f, indent=4)
    elif path_to_save.endswith('.tsv'):
        with open(path_to_save, 'w') as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(primary_keys.keys())
            writer.writerow(primary_keys.values())
    elif path_to_save.endswith('.cff'):
        with open(path_to_save, 'w') as f:
            yaml.dump(primary_keys, f, default_flow_style=False)
            print(path_to_save)
            print(primary_keys)
    elif path_to_save.endswith('.txt'):
        with open(path_to_save, 'w') as f:
            for key, value in primary_keys.items():
                f.write(f"{key}: {value}\n")
    return primary_keys


def complete_agnostic_file(output_dir, **kwargs):
    global files_list
    try:
        files_list = os.listdir(output_dir)
        files_list = [f for f in files_list if os.path.isfile(os.path.join(output_dir, f))]

    except Exception as e:
        print(f"None file found: {e}")
    for file_name in files_list:
        template = None
        if file_name == "participants.json" or file_name == "participants.tsv":
            template = data_participants_template
        elif file_name == "dataset_description.json" or file_name == "dataset_description.tsv":
            template = data_description_template
        elif file_name == "CITATION.cff":
            template = Citation_template

        elif file_name.startswith("samples"):
            template = Sample_template
        else:
            # there we will be able to add the Readme template after

            continue
        if template is not None:
            write_agnostic_files(os.path.join(output_dir, file_name), template, **kwargs)
            print(f"Wrote {file_name}")


if __name__ == "__main__":
    pass
