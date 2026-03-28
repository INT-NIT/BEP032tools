"""
BidsDatasetBuilder.py

This module provides tools for processing, organizing, and converting neuroimaging datasets into the BIDS (Brain Imaging Data Structure) format.
It supports directory creation, file conversion, metadata handling, and integration with elab sources and the BIDSTools ecosystem.


Typical Usage:
    pytho nconfocal_microscopy_customs --config_file_path <config.json> --metada_file_path <metadata.csv> --output_dir <bids_output> --tag <experiment_tag>, --project_config_yml_path <project_config.yml>

Refer to the BIDS specification and BIDSTools documentation for further details.
"""

import argparse
import csv
import json
import logging
import os
import shutil
from BIDSTools.get_experiement_details import get_experiement_details
from BIDSTools.BidsModality import Modality
from BIDSTools.Createfile import CreatFile
from BIDSTools.ProjectConfig import ProjectConfig

from BIDSTools.constants_fields import *  # Import des constantes de mapping de champs

from BIDSTools.Experiment import Experiment

from BIDSTools.BIDS_PROJECT_CONFIG.BIDS_modality_custom import ModalityCustomBuilder

def generate_empty_top_level_bids_files(outpout_dir):
    """
    Generate a top-level bid dataset structure file

    Parameters
    ----------
    outpout_dir : str
        Path to save bids dataset
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
    sub_ids = "sub-" + sub_id
    sub_dir = os.path.join(outpout_dir, sub_ids)
    if not os.path.exists(sub_dir):
        return False
    else:
        return True


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
    if session_id is None:
        return sub_dir
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


def get_link(current_exp):
    try:

        link = current_exp.get_attribute(RAW_DATA_PATH)
    except AttributeError:
        logging.warning(
            f"RAW_DATA_PATH attribute not found in experiment {current_exp.get_attribute(SUBJECT_ID)}")
        link = " "
    return link


def get_data_metadata_link(current_exp, current_path):
    raw_data_link = get_link(current_exp)

    return raw_data_link


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


def initiate_top_level_bids_files_tsv(output_dir):
    """

     Writes headers to TSV files in the BIDS top-level directory based on JSON template files.

    Parameters
    ----------
    output_dir: str
        Path to the directory where the BIDS top-level TSV files are located.

    Returns ------- None This function does not return any value. It updates the TSV files in
    place by adding headers based on the corresponding JSON template files found in the
    'template_agnostic_file' directory.

    """
    tsv_json_files_list = [f for f in os.listdir(output_dir) if
                           f.endswith(".tsv")]

    tsv_json_files_list = [f for f in tsv_json_files_list if
                           os.path.isfile(os.path.join(output_dir, f))]

    script_dir = os.path.dirname(__file__)
    agnostic_template_dir = os.path.join(script_dir, 'template_agnostic_files')

    list_template_files = os.listdir(agnostic_template_dir)
    list_template_files = [f for f in list_template_files if
                           os.path.isfile(os.path.join(agnostic_template_dir, f)) and f.endswith(
                               "_tsv.json")]

    for template_name in list_template_files:
        template_base_name = template_name.removesuffix("_tsv.json")

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
        f.write(header)


def initiate_top_level_bids_files_json(output_dir):
    """

     Initiate json files with default values in the BIDS top-level directory based on JSON template files.

    Parameters
    ----------
    output_dir: str
        Path to the directory where the BIDS top-level TSV files are located.

    Returns
    ------- 
    None

    """
    json_files_list = [f for f in os.listdir(output_dir) if
                           f.endswith(".json")]

    json_files_list = [f for f in json_files_list if
                           os.path.isfile(os.path.join(output_dir, f))]

    script_dir = os.path.dirname(__file__)
    agnostic_template_dir = os.path.join(script_dir, 'template_agnostic_files')

    list_template_files = os.listdir(agnostic_template_dir)
    list_template_files = [f for f in list_template_files if
                           os.path.isfile(os.path.join(agnostic_template_dir, f)) and f.endswith(
                               "_json.json")]

    for template_name in list_template_files:
        template_base_name = template_name.removesuffix("_json.json")

        template_path = os.path.join(agnostic_template_dir, template_name)
        with open(template_path, 'r') as template_file:
            template_content = json.load(template_file)

            if template_content:
                for file_name in json_files_list:
                    if file_name.startswith(template_base_name):
                        #writeheader(template_content, file_name, output_dir)
                        file_path = os.path.join(output_dir, file_name)
                        write_static_files(template_path, file_path)


def construct_bids_folders(output_dir, experiment, project_config):
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
    This function processes an experiment by creating the necessary
    directories based on its attributes. It creates a subject directory if required , and if the
    data type requires a session directory, it creates that as well. Finally, it creates a data type
    directory within the session or subject directory as needed.

    Example
    -------
    If an experiment has the following attributes:
        - Subject ID: '01'
        - Data type: 'func' if single data type
        - Data type: 'func' , 'anat' , ..., if multiple data types
        - Session Number: '01'

    The following directory structure will be created:
        output_dir/sub-01/ses-01/func/
    """
    list_experiments_already_processed = []
    current_dir = output_dir

    # Retrieve attributes from the experiment object
    subject_id = experiment.get_attribute(SUBJECT_ID,)  # Use the SUBJECT_ID constant
    current_dir = generate_subdir(current_dir, subject_id)
    #data_type = experiment.get_attribute("Data type") # must be changed

    # check modality
    modality_list = project_config.get_project_modalities()



    # take the list of modalities
    modality_objects =  Modality()
    for modality in modality_list:
        if modality.upper() not in modality_objects.modalities:
            raise ValueError(f"Modality {modality} is not valid. Valid modalities are: {modality_objects.modalities}")



        for datatype_key  in modality_objects.modalities:
            if modality.upper() in datatype_key:
                data_type = modality_objects.modality_details[datatype_key]
                if project_config.is_session_required():
                    session_number = experiment.get_attribute(SESSION_ID)


                    current_dir = generate_session_dir(current_dir,
                                                       session_number)
                current_dir = generate_datatype_dir(current_dir, data_type)






    # creat a custom part
    custom_builder  = ModalityCustomBuilder(project_config, experiment, current_dir)
    custom_builder.build_customizations()

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
    """
    Adds a new experiment to a JSON file if it doesn't already exist.

    This function checks if an experiment, represented as a dictionary,
    is already present in the JSON file specified by `file_path`. If the
    experiment is not present, it is added to the JSON file. If the file
    does not exist, a new file is created.

    Parameters
    ----------
    file_path : str
        The path to the JSON file where the experiment data is stored.
    experiment : Experiment
        An object from the Experiment class containing the data of the experiment to be added.

    Returns
    -------
    None
        This function does not return any value. It modifies the JSON file by adding
        the new experiment if it doesn't already exist.

    Raises
    ------
    IOError
        If there is an issue opening or writing to the JSON file.

    Example
    -------
    Assume `experiment` is an instance of the Experiment class with relevant data.

    >>> add_new_experiment_to_json('experiments.json', experiment)
    This will add the experiment to 'experiments.json' if it's not already present.
    """
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
        lines_updated = {}
        if file_name.endswith('.tsv'):
            with open(file_path, 'r') as f:
                reader = csv.DictReader(f, delimiter='\t')
                lines = list(reader)
                print(f"Lines: {lines}")
                print(f"File: {file_name}, Path: {file_path}", file_path,)
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

                    if SUBJECT_ID not in row:
                        print(f"Missing '{SUBJECT_ID}' in row: {row}")
                        continue

                    exp = Experiment(**row)

                    if experiment.get_attribute(SUBJECT_ID) == row[SUBJECT_ID]:
                        if exp == experiment:
                            its_new_experience = False
                            break
                        else:
                            print("There are modifications in this experiment")
                            input_user = input(
                                "Press 1 to continue without changes or 2 to update the "
                                "experiment: ")
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

    lines[line_number] = filtered_exp_dict

    # Write back the file with updated content
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, delimiter='\t', fieldnames=headers)
        writer.writeheader()
        writer.writerows(lines)


def write_static_files(template_path, file_path):
    """
    Fills a static file with default values based on a JSON template.

    Parameters
    ----------
    template_path : str
        The path to the JSON template file. This file should contain default values for various
        keys.
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


def initiate_top_level_bids_files_other(output_dir):
    """
    Processes static files in the specified directory. For each file that does not have a .json or
     .tsv extension,
    checks for a corresponding template file and fills the static file with default values from
    the template.

    Parameters
    ----------
    output_dir : str
        The path to the directory where static files are located.

    Returns
    -------
    None
    """
    script_dir = os.path.dirname(__file__)

    agnostic_template_dir = os.path.join(script_dir, "template_agnostic_files")

    list_template_files = os.listdir(agnostic_template_dir)

    all_files = os.listdir(output_dir)
    tsv_json_files_list = [f for f in all_files if f.endswith('.json') or f.endswith('.tsv')]

    for file_name in all_files:
        if file_name in tsv_json_files_list:
            # skip json and tsv files to process only the others
            continue

        file_path = os.path.join(output_dir, file_name)
        base_name, ext = os.path.splitext(file_name)
        base_name_json = base_name + '.json'

        if base_name_json in list_template_files:
            template_path = os.path.join(agnostic_template_dir, base_name_json)
            write_static_files(template_path, file_path)



def simple_copy(source_path, destination_path):
    shutil.copytree(source_path, destination_path)








def main(config_file_path, metada_file_path, output_dir, tag, project_config_yml_path="confocal_microscopy.yml"):


    """
    Main entry point for the BIDS generation process.

    This function reads configuration parameters from a file, downloads experiment data from elab using the provided tag,
    and generates a BIDS-compliant dataset structure with example experiments and files.

    Parameters
    ----------
    config_file_path : str
        Path to a configuration file containing elab connection parameters.
    metada_file_path : str
        Path where to save the downloaded experiment metadata.
    output_dir : str
        Path to the directory where the BIDS dataset will be generated.
    tag : str
        Tag to filter experiments.
    project_config_yml_path : str
        Path to the project configuration file.
        eg: confocal_microscopy.yml

    Returns
    -------
    None
        The function modifies the file system by creating a BIDS dataset structure and writing files to it.
    """
    # Download experiment data from elab
    get_experiement_details(
        config_file_path,
        metada_file_path,
        tag,
        metada_file_path
    )
    # get project config
    project_config = ProjectConfig(project_config_yml_path)

   # Generate top-level file structure
    generate_empty_top_level_bids_files(output_dir)



    # Generate participant folder structure


    # Write header (first line) of tsv files
    initiate_top_level_bids_files_tsv(output_dir)
    # Temporary: fill json files (as static ones)
    initiate_top_level_bids_files_json(output_dir)
    # Fill static files
    initiate_top_level_bids_files_other(output_dir)

    # Fill metadata files

    with open(metada_file_path, mode='r', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # create an experiment(object)
            experiment = Experiment(**row)
            # creat a BIDS folder structure

            construct_bids_folders(output_dir, experiment, project_config)
            # convert edf to bids( formats) and store them in predefined folders

            # fill metadata in TSV files
            fill_metadata_files(output_dir, experiment)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("config_file_path", help="The path to the configuration file")
    parser.add_argument("metada_file_path", help="The path to the output directory")
    parser.add_argument("output_dir", help="The path to the output directory")
    parser.add_argument("tag", help="The tag to write the output to")
    parser.add_argument("project_config_yml_path", help="The path to the project configuration file")
    args = parser.parse_args()
    main(args.config_file_path, args.metada_file_path, args.output_dir, args.tag, args.project_config_yml_path)
