import csv
import json
import os
from Experiment import Experiment
import numpy as np
from Createfile import CreatFile
import template_agnotic_file


def generate_top_level_file(outpout_dir):
    """"
    Generate a top-level bid dataset structure file

    Parameters
    input   :path to save  bids dataset
    """
    builder_creatfile = CreatFile(outpout_dir)
    builder_creatfile.build()


def get_sub_id(current_exp):
    return current_exp.id


def check_subdir(outpout_dir, sub_id):
    sub_id = "sub-" + sub_id
    sub_dir = os.path.join(outpout_dir, sub_id)
    if not os.path.exists(sub_dir):
        return True
    else:
        return False


def generate_subdir(outpout_dir, sub_id):
    sub_id = "sub-" + sub_id
    sub_dir = os.path.join(outpout_dir, sub_id)
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)
    return sub_dir


def check_datatype_has_session(datatype):
    return True


def generate_session_dir(sub_dir, session_id):
    session_id = "ses-" + session_id
    session_dir = os.path.join(sub_dir, session_id)
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)
    return session_dir


def generate_datatype_dir(current_dir, datatype):
    datatype_dir = os.path.join(current_dir, datatype)
    if not os.path.exists(datatype_dir):
        os.makedirs(datatype_dir)
    return datatype_dir


def get_bids_filename(current_exp, raw_data_link):
    return raw_data_link
    pass


def get_data_metadata_link(current_exp, data_storage_path):
    raw_data_link = current_exp.get_data_link()

    standardized_data_link = get_bids_filename(current_exp, raw_data_link)


def covert_data_edf_to_msg(edf_data):
    pass


def already_exists_subject(current_exp):
    return true


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


def writeheader_tsv_json_files(output_dir):
    tsv_json_files_list = [f for f in os.listdir(output_dir) if
                           f.endswith(".json") or f.endswith(".tsv")]

    tsv_json_files_list = [f for f in tsv_json_files_list if
                           os.path.isfile(os.path.join(output_dir, f))]

    agnostic_template_dir = "template_agnotic_file"

    list_template_files = os.listdir(agnostic_template_dir)
    list_template_files = [f for f in list_template_files if
                           os.path.isfile(os.path.join(agnostic_template_dir, f)) and f.endswith(
                               ".json")]
    print(list_template_files)

    for template_name in list_template_files:
        template_base_name, template_ext = os.path.splitext(template_name)

        template_path = os.path.join(agnostic_template_dir, template_name)
        with open(template_path, 'r') as template_file:
            template_content = json.load(template_file)

            if template_content:
                for file_name in tsv_json_files_list:
                    if file_name.startswith(template_base_name):
                        writeheader(template_content, file_name, output_dir)


import os


def writeheader(template_content, file_name, output_dir):
    file_path = os.path.join(output_dir, file_name)

    # Extract header from template content
    header = '\t'.join(template_content.keys()) + '\n'

    # Open the file for reading and writing
    with open(file_path, 'r+') as f:
        # Read the existing content of the file
        existing_content = f.read()

        # Move the cursor to the beginning of the file
        f.seek(0, 0)

        # Write the new header
        f.write(header)


def bids_dataset_processed(output_dir, experiment):
    list_experiments_already_processed = []
    current_dir = output_dir

    subject_id = experiment.get_attribute("Subject ID")
    data_type = experiment.get_attribute("Data type")
    session_number = experiment.get_attribute("Session Number")

    current_dir = generate_subdir(current_dir, subject_id)
    if check_datatype_has_session(data_type):
        current_dir = generate_session_dir(current_dir, session_number)
    current_dir = generate_datatype_dir(current_dir, data_type)

    list_experiments_already_processed.append(experiment)
    return current_dir, list_experiments_already_processed


def add_new_experiment_to_tsv(file_path, experiment):
    # Convert experiment object to dictionary
    exp_dict = experiment.to_dict()

    # Read the existing header from the file if it exists
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            # Read the first line to get the header
            header_line = f.readline()
            # Split header line into fieldnames
            existing_fieldnames = header_line.strip().split('\t')
    else:
        existing_fieldnames = []

    # Filter the experiment dictionary to only include existing fields
    filtered_exp_dict = {key: exp_dict.get(key, '') for key in existing_fieldnames}

    # Open the file in append mode
    with open(file_path, 'a', newline='') as f:
        # Create a CSV DictWriter object with the existing fieldnames
        writer = csv.DictWriter(f, delimiter='\t', fieldnames=existing_fieldnames)

        # Write the header only if the file did not previously exist
        if not existing_fieldnames:
            with open(file_path, 'w', newline='') as f_write:
                writer = csv.DictWriter(f_write, delimiter='\t', fieldnames=existing_fieldnames)
                writer.writeheader()

        # Write the new row (experiment)
        writer.writerow(filtered_exp_dict)


def add_new_experiment_to_json(file_path, experiment):
    try:
        with open(file_path, 'r') as f:
            existing_data = json.load(f)  # Load existing JSON data
    except FileNotFoundError:
        existing_data = []  # Start with an empty list if file does not exist

    # Convert the experiment to a dictionary and then to a JSON string
    exp_dict = experiment.to_dict()
    exp_json_string = json.dumps(exp_dict, sort_keys=True)

    # Convert existing data to JSON strings for comparison
    existing_json_strings = {json.dumps(item, sort_keys=True) for item in existing_data}

    # Check if the experiment JSON string already exists in existing data
    if exp_json_string not in existing_json_strings:
        existing_data.append(exp_dict)  # Add new experiment to existing data
        with open(file_path, 'w') as f:
            json.dump(existing_data, f, indent=4)  # Write updated data back to JSON file


def fill_metadata_files(output_dir, experiment):
    tsv_json_files_list = [f for f in os.listdir(output_dir) if
                           f.endswith(".json") or f.endswith(".tsv")]

    for file_name in tsv_json_files_list:
        file_path = os.path.join(output_dir, file_name)
        its_new_experience = True

        if file_name.endswith('.tsv'):
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f, delimiter='\t')
                lines = list(reader)

                # Nettoyer les en-têtes et les lignes pour supprimer les espaces inutiles
                if lines:
                    lines_updated = [{key.strip(): (value.strip() if value else '')for key, value in row.items()} for
                                     row
                                     in lines]

                if lines_updated:
                    # Extraire les en-têtes après nettoyage
                    headers = [header.strip() for header in lines_updated[0].keys()]
                    print(f"Headers: {headers}")

                for line_number, row in enumerate(lines_updated):

                    row = {key.strip(): value.strip() for key, value in row.items()}

                    if 'Subject ID' not in row:
                        print(f"Missing 'Subject ID' in row: {row}")
                        continue  # Passer à la ligne suivante si 'Subject ID' est manquant

                    exp = Experiment(**row)
                    print(
                        f"Comparing Subject ID {row['Subject ID']} with {experiment.get_attribute('Subject ID')}")

                    if experiment.get_attribute("Subject ID") == row['Subject ID']:
                        if exp == experiment:
                            its_new_experience = False
                            break  # Pas besoin de vérifier les autres lignes si l'expérience est trouvée
                        else:
                            print("There are modifications in this experiment")
                            input_user = input(
                                "Press 1 to continue without changes or 2 to update the experiment: ")
                            if input_user == '1':
                                continue  # Passer à l'itération suivante sans mise à jour
                            else:
                                update_file(experiment, line_number, file_path, lines_updated,
                                            headers)
                            its_new_experience = False
                            break

            if its_new_experience:
                add_new_experiment_to_tsv(file_path, experiment)


def update_file(experiment, line_number, file_path, lines, headers):
    # Filter the experiment dictionary to keep only the fields in the header
    exp_dict = experiment.to_dict()
    filtered_exp_dict = {key: exp_dict.get(key, '') for key in headers}
    print(filtered_exp_dict, " found in ", file_path)
    lines[line_number] = filtered_exp_dict
    print(lines, "je suis lines")
    # Write back the file with updated content
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, delimiter='\t', fieldnames=headers)
        writer.writeheader()
        writer.writerows(lines)


def write_static_files(template_path, file_path):
    # Read the JSON content from the template file
    with open(template_path, 'r') as template_file:
        template_content = json.load(template_file)

    primary_key = {key: template_content[key]["Default value"] for key in template_content.keys()}
    # primary_key = edite_value(primary_key,**kwrg)
    print(primary_key)

    # Write the template content to the output file in JSON format
    with open(file_path, 'w') as static_file:
        json.dump(primary_key, static_file, indent=4)

    print(
        f"Written static content from {template_path} to {file_path} with primary key: {primary_key}")


def fill_static_files(output_dir):
    agnostic_template_dir = "template_agnotic_file"
    list_template_files = os.listdir(agnostic_template_dir)

    all_files = os.listdir(output_dir)
    tsv_json_files_list = [f for f in all_files if f.endswith('.json') or f.endswith('.tsv')]

    for file_name in all_files:
        if file_name in tsv_json_files_list:
            continue
        file_path = os.path.join(output_dir, file_name)
        base_name, ext = os.path.splitext(file_name)
        base_name_json = base_name + '.json'

        if base_name_json in list_template_files:
            template_path = os.path.join(agnostic_template_dir, base_name_json)
            write_static_files(template_path, file_path)


def main():
    outpout = "/home/INT/idrissou.f/Bureau/diglab"
    generate_top_level_file(outpout)
    path = "/home/INT/idrissou.f/Bureau/diglab/newone1.csv"
    writeheader_tsv_json_files(outpout)
    fill_static_files(outpout)
    with open(path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            print(row)
            experiment = Experiment(**row)
            bids_dataset_processed(outpout, experiment)
            fill_metadata_files(outpout, experiment)


if __name__ == '__main__':
    main()
