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
    outpout_dir   :path to save  bids dataset
    """
    builder_creatfile = CreatFile(outpout_dir)
    builder_creatfile.build()


def check_subdir(outpout_dir, sub_id):
    """
    check if a subdirectory exists
    Parameters
    ----------
    outpout_dir : path to save bid dataset
    sub_id : subdirectory id

    Returns
    -------
    bolean : True if subdirectory exists, else False
    """
    sub_id = "sub-" + sub_id
    sub_dir = os.path.join(outpout_dir, sub_id)
    if not os.path.exists(sub_dir):
        return True
    else:
        return False


def generate_subdir(outpout_dir, sub_id):
    """
    generate a subdirectory if it doesn't exists'
    Parameters
    ----------
    outpout_dir path:path to save bid dataset
    sub_id : subdirectory id

    Returns
    -------
    sub_dir ; absolute path of subdirectory
    """
    sub_id = "sub-" + sub_id
    sub_dir = os.path.join(outpout_dir, sub_id)
    if not os.path.exists(sub_dir):
        os.makedirs(sub_dir)
    return sub_dir


def check_datatype_has_session(datatype):
    """
    check if BIDS datatype has a session attribute
    Parameters
    ----------
    datatype: BIDS datatype

    Returns
    -------
    Boolean : True if BIDS datatype has a session attribute, else False
    """
    return True


def generate_session_dir(sub_dir, session_id):
    """
    generate a session directory
    Parameters
    ----------
    sub_dir:path of subdirectory
    session_id:session id

    Returns
    -------
    session_dir:absolute path of session directory
    """
    session_id = "ses-" + session_id
    session_dir = os.path.join(sub_dir, session_id)
    if not os.path.exists(session_dir):
        os.makedirs(session_dir)
    return session_dir


def generate_datatype_dir(current_dir, datatype):
    """
    generate a datatype directory
    Parameters
    ----------
    current_dir:absolute path of current
    directory it can be subdirectory if Datatype has no session attribute or session directory if
    Datatype has a session attribute datatype

    Returns
    -------
    the absolute path of datatype directory
    """
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
    """

     Writes headers to TSV files in the BIDS top-level directory based on JSON template files.

    Parameters
    ----------
    output_dir: str
        Path to the directory where the BIDS top-level TSV files are located.

    Returns
    -------
    None
        This function does not return any value. It updates the TSV files in place by adding headers
        based on the corresponding JSON template files found in the 'template_agnostic_file' directory.

    """
    tsv_json_files_list = [f for f in os.listdir(output_dir) if
                           f.endswith(".tsv")]

    tsv_json_files_list = [f for f in tsv_json_files_list if
                           os.path.isfile(os.path.join(output_dir, f))]

    agnostic_template_dir = "template_agnotic_file"

    list_template_files = os.listdir(agnostic_template_dir)
    list_template_files = [f for f in list_template_files if
                           os.path.isfile(os.path.join(agnostic_template_dir, f)) and f.endswith(
                               ".json")]

    for template_name in list_template_files:
        template_base_name, template_ext = os.path.splitext(template_name)

        template_path = os.path.join(agnostic_template_dir, template_name)
        with open(template_path, 'r') as template_file:
            template_content = json.load(template_file)

            if template_content:
                for file_name in tsv_json_files_list:
                    if file_name.startswith(template_base_name):
                        writeheader(template_content, file_name, output_dir)


def writeheader(template_content, file_name, output_dir):
    """
    Extract headers from a template file and write them to a corresponding TSV file.

    Parameters
    ----------
    template_content : dict
        The JSON data from the template file.
    file_name : str
        Name of the corresponding TSV file for this template.
    output_dir : str
        Path where the corresponding TSV file is located.

    Returns
    -------
    None
        The TSV file is updated with the corresponding header.
    """
    file_path = os.path.join(output_dir, file_name)

    # Extract header from template content
    header = '\t'.join(template_content.keys()) + '\n'

    # Open the file for reading and writing
    with open(file_path, 'r+') as f:
        # Read the existing content of the file
        existing_content = f.read()

        # Move the cursor to the beginning of the file
        f.seek(0, 0)

        # Write the new header and then the existing content
        f.write(header + existing_content)


def bids_dataset_processed(output_dir, experiment):
    """
    Creates all necessary directories for each experiment (each row in the metadata file).

    Parameters
    ----------
    output_dir : str
        Path to the base directory where BIDS data should be saved.
    experiment : Experiment
        An object from the Experiment class representing a row of the metadata file.

    Returns
    -------
    tuple A tuple containing the final directory path created for the experiment
    and a list of experiments already processed.

    Description
    -----------
    This function processes an experiment by creating the necessary directories based on its attributes.
    It creates a subject directory, and if the data type requires a session directory, it creates that as well.
    Finally, it creates a data type directory within the session or subject directory as needed.

    Example
    -------
    If an experiment has the following attributes:
        - Subject ID: '01'
        - Data type: 'func'
        - Session Number: '01'

    The following directory structure will be created:
        output_dir/sub-01/ses-01/func/
    """
    list_experiments_already_processed = []
    current_dir = output_dir

    # Retrieve attributes from the experiment object
    subject_id = experiment.get_attribute("Subject ID")
    data_type = experiment.get_attribute("Data type")
    session_number = experiment.get_attribute("Session Number")

    # Create the subject directory
    current_dir = generate_subdir(current_dir, subject_id)

    # If the data type requires a session directory, create it
    if check_datatype_has_session(data_type):
        current_dir = generate_session_dir(current_dir, session_number)

    # Create the data type directory
    current_dir = generate_datatype_dir(current_dir, data_type)

    # Append the processed experiment to the list
    list_experiments_already_processed.append(experiment)

    return current_dir, list_experiments_already_processed


def add_new_experiment_to_tsv(file_path, experiment):
    """
    Adds a new experiment (a new row from the metadata CSV file) to the TSV file.

    Parameters
    ----------
    file_path : str
        The path to the TSV file to which the new row (experiment) will be added.
    experiment : Experiment
        An object from the Experiment class representing a row of the metadata file.

    Returns
    -------
    None
        The function modifies the TSV file in place by adding a new row.
    """
    # Convert the experiment object to a dictionary
    exp_dict = experiment.to_dict()

    # Read the existing header from the file if it exists
    if os.path.isfile(file_path):
        with open(file_path, 'r') as f:
            # Read the first line to get the header
            header_line = f.readline()
            # Split the header line into field names
            existing_fieldnames = header_line.strip().split('\t')
    else:
        # If the file doesn't exist, initialize an empty list of field names
        existing_fieldnames = []

    # Open the file in append mode
    with open(file_path, 'a', newline='') as f:
        # If the file is new and empty, initialize with all keys from exp_dict
        if not existing_fieldnames:
            print("its have a problem with this file {}".format(file_path))
            pass
            existing_fieldnames = exp_dict.keys()
            writer = csv.DictWriter(f, delimiter='\t', fieldnames=existing_fieldnames)
            writer.writeheader()
        else:
            # Filter the experiment dictionary to include only existing fields
            filtered_exp_dict = {key: exp_dict.get(key, '') for key in existing_fieldnames}
            writer = csv.DictWriter(f, delimiter='\t', fieldnames=existing_fieldnames)

        # Write the new row (experiment)
        writer.writerow(filtered_exp_dict if existing_fieldnames else exp_dict)


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


import os
import csv


def fill_metadata_files(output_dir, experiment):
    """
    Fill an experiment's metadata in a file for each experiment in the metadata file.

    Parameters
    ----------
    output_dir : str
        Path to the directory containing the TSV files.
    experiment : Experiment
        An object from the Experiment class representing a row of the metadata file.

    Returns
    -------
    None
        The function modifies TSV files in place by adding new rows or updating existing ones.
    """
    tsv_json_files_list = [f for f in os.listdir(output_dir) if f.endswith(".tsv")]

    for file_name in tsv_json_files_list:
        file_path = os.path.join(output_dir, file_name)
        its_new_experience = True

        if file_name.endswith('.tsv'):
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f, delimiter='\t')
                lines = list(reader)

                # Nettoyer les en-têtes et les lignes pour supprimer les espaces inutiles
                if lines:
                    lines_updated = [
                        {key.strip(): (value.strip() if value else '') for key, value in
                         row.items()}
                        for row in lines
                    ]

                if lines_updated:
                    headers = [header.strip() for header in lines_updated[0].keys()]
                    print(f"Headers: {headers}")

                for line_number, row in enumerate(lines_updated):
                    row = {key.strip(): value.strip() for key, value in row.items()}

                    if 'Subject ID' not in row:
                        print(f"Missing 'Subject ID' in row: {row}")
                        continue

                    exp = Experiment(**row)

                    if experiment.get_attribute("Subject ID") == row['Subject ID']:
                        if exp == experiment:
                            its_new_experience = False
                            break
                        else:
                            print("There are modifications in this experiment")
                            input_user = input(
                                "Press 1 to continue without changes or 2 to update the experiment: ")
                            if input_user == '1':
                                break
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


import json


def write_static_files(template_path, file_path):
    """
    Fills a static file with default values based on a JSON template.

    Parameters
    ----------
    template_path : str
        The path to the JSON template file. This file should contain default values for various keys.
    file_path : str
        The path to the output file where the default values will be written.

    Returns
    -------
    None
    """
    # Read the JSON content from the template file
    with open(template_path, 'r') as template_file:
        template_content = json.load(template_file)

    # Extract default values for each key from the template
    primary_key = {key: template_content[key]["Default value"] for key in template_content.keys()}

    # Write the default values to the output file in JSON format
    with open(file_path, 'w') as static_file:
        json.dump(primary_key, static_file, indent=4)

    print(
        f"Written static content from {template_path} to {file_path} with primary key: {primary_key}")


def fill_static_files(output_dir):
    """
    Processes static files in the specified directory. For each file that does not have a .json or .tsv extension,
    checks for a corresponding template file and fills the static file with default values from the template.

    Parameters
    ----------
    output_dir : str
        The path to the directory where static files are located.

    Returns
    -------
    None
    """
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
