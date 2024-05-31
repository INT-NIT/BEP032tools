import csv
import json
import os
import warnings
import yaml

bid_version_path = os.path.join('ressources/schema', 'BIDS_VERSION')


def extract_primary_key(template):
    """
    Extracts the primary keys from the provided template and includes the BIDS version.

    Args:
        template (dict): The template containing the data description.

    Returns:
        dict: A dictionary with primary keys and their requirement levels.
    """
    primary_keys = {key: template[key]["Default value"] for key in template.keys()
                    if template[key]["Requirement Level"] == "REQUIRED"}
    return primary_keys


def write_agnostic_files(path_to_save, template, **kwargs):
    """
    Writes an agnostic file using the template and additional keyword arguments.

    Args:
        path_to_save (str): The path where the file will be saved.
        template (dict): The template containing the data description.
        **kwargs: Additional keyword arguments to override template values.

    Returns:
        dict: A dictionary with the updated primary keys.
    """
    primary_keys = extract_primary_key(template)

    for key, value in kwargs.items():
        if key in primary_keys:
            primary_keys[key] = value

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


def fill_agnostic_file(output_dir, **kwargs):
    """
    Fills agnostic files in the specified output directory with provided data.

    Args:
        output_dir (str): The directory where the agnostic files will be filled.
        **kwargs: Additional keyword arguments.

    Returns:
        None
    """
    agnostic_template_dir = "template_agnotic_file"
    try:
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

        agnostic_files_list = os.listdir(output_dir)
        agnostic_files_list = [f for f in agnostic_files_list if
                               os.path.isfile(os.path.join(output_dir, f))]
        agnostic_files_template = os.listdir(agnostic_template_dir)
    except Exception as e:
        print(f"Error: {e}")
        return

    for agnostic_template_name in agnostic_files_template:
        if agnostic_template_name in agnostic_files_list:
            template = json.load(open(os.path.join(agnostic_template_dir, agnostic_template_name)))

            if template is not None:
                for file_path in agnostic_files_list:
                    if file_path.startswith(os.path.splitext(agnostic_template_name)[0]):
                        write_agnostic_files(os.path.join(output_dir, file_path),
                                             template, **kwargs)
                        print(f"Wrote {file_path}")


if __name__ == "__main__":
    output_directory = "Essaie"
    additional_kwargs = {
        "Name": "My Dataset",
        "BIDSVersion": "1.3.0",
        "HEDVersion": "7.0",

    }
    fill_agnostic_file(output_directory, **additional_kwargs)
