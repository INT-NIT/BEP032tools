"""
get_experiement_details.py

This module provides tools for extracting and processing experiment details from JSON to CSV format for BIDS (Brain Imaging Data Structure) workflows.
It enables transformation of experiment metadata for easier analysis and integration with BIDSTools pipelines.

Main Features:
- Processes experiment data from JSON files and saves as CSV.
- Extracts experiment fields and modality types for downstream use.
- Integrates with elab_bridge for data download and transformation.

Typical Usage:
    from BIDSTools.get_experiement_details import get_experiement_details
    get_experiement_details(config_file_path, metada_file_path, tag, output_csv_file)

Refer to the BIDSTools documentation for more details on experiment metadata extraction.
"""

import json
import os
from typing import Dict, List, Any
import pandas as pd
import elabapi_python

def extended_download(save_to, server_config_json, experiment_tags=None,
                      format='csv', experiment_axis='columns'):
    """
    Download experiments based on tags or a specific experiment by ID.
    Existing function that has been retrieved from "DigLabTools" repository, at "elab_bridge/server_interface.py"
    Parameters
    ----------
    save_to: str
        Path where to save the retrieved experiment data
    server_config_json: str
        Path to the json file containing the api_url and the api_token
    experiment_tags: list, optional
        List of tags of your experiments. Default is None.
    experiment_id: int, optional
        ID of the experiment you want to download. Default is None.
    format: str
        Format of the retrieved records. Options are 'csv' or 'json'. Default: 'csv'
    experiment_axis: str
        Option to control whether in the csv format experiments are arranged in columns or rows.
        Default: 'columns'

    Returns
    -------
    list
        List of the experiment(s) downloaded
    """

    api_client = get_elab_config(server_config_json)
    experiment_api = elabapi_python.ExperimentsApi(api_client)

    if experiment_tags:
        response = experiment_api.read_experiments_with_http_info(tags=experiment_tags)
        experiments = response[0]
        experiment_ids = [experiment.id for experiment in experiments]
    else:
        raise ValueError("Either experiment_tags or experiment_id must be provided.")

    downloaded_experiments = []
    combined_df = pd.DataFrame()

    for exp_id in experiment_ids:
        experiment_body, status_get, http_dict = (
            experiment_api.get_experiment_with_http_info(exp_id))

        if status_get != 200:
            raise ValueError('Could not download experiment. '
                             'Check your internet connection and permissions.')

        experiment_json = experiment_body.metadata
        metadata = json.loads(experiment_json)
        extra_fields = metadata.get("extra_fields", {})

        if format == 'json':
            with open(save_to, 'w') as f:
                json.dump(extra_fields, f)
        elif format == 'csv':
            if experiment_axis == 'columns':
                df = pd.DataFrame.from_dict(extra_fields, orient='columns')
                combined_df = pd.concat([combined_df, df.iloc[[1]]], ignore_index=True, sort=False)
            elif experiment_axis == 'rows':
                df = pd.DataFrame.from_dict(extra_fields, orient='index')
                df = df[['value']].transpose()
                combined_df = pd.concat([combined_df, df], ignore_index=True, sort=False)
            else:
                raise ValueError(f'Unknown experiment axis: {experiment_axis}. Valid arguments are '
                                 f'"columns" and "rows".')
        else:
            raise ValueError(f'Unknown format: {format}. Valid arguments are "json" and "csv".')

        downloaded_experiments.append(metadata)

    if format == 'csv':
        combined_df.to_csv(save_to, index=False)

    return downloaded_experiments


def get_elab_config(server_config_json):
    """
    Initialize an elab project based on the provided server configuration
    Existing function that has been retrieved from "DigLabTools" repository, at "elab_bridge/server_interface.py"
    Used to make extended_download works
    :param server_config_json: json file containing the api_token and api_url
    :return: elab api client
    """

    config = json.load(open(server_config_json, 'r'))
    configuration = elabapi_python.Configuration()

    if config['api_token'] in os.environ:
        api_token = os.environ[config['api_token']]
    else:
        api_token = config['api_token']

    configuration.api_key['api_token'] = api_token
    configuration.api_key_prefix['api_token'] = 'Authorization'

    configuration.host = config['api_url']
    configuration.debug = True
    configuration.verify_ssl = False

    api_client = elabapi_python.ApiClient(configuration)
    api_client.set_default_header(header_name='Authorization', header_value=api_token)

    return api_client


def get_experiement_details(config_file_path: str, metada_file_path: str, tag: str,
                            output_csv_file: str) -> None:
    """
    Process experiment data from a JSON file and save it as a CSV file.

    The function reads experiment data from a JSON file, extracts relevant information
    including experiment fields and modality types, and saves the processed data
    to a CSV file.

    Args:
        experiement_json_file (str): Path to the input JSON file containing experiment data.
        output_csv_file (str): Path where the output CSV file will be saved.

    Raises:
        FileNotFoundError: If the input JSON file does not exist.
        json.JSONDecodeError: If the input file contains invalid JSON.
        ValueError: If the required fields are missing in the JSON structure.


    """
    
    experiement_details = extended_download(
        metada_file_path,
        config_file_path,
        [tag],
        format='csv'
    )
    list_experiement_details = []
    for data in experiement_details:
        group_fields = []
        fields_details = {}
        if data.get('elabftw') and data['elabftw'].get(
                'extra_fields_groups') and data.get('extra_fields'):
            # Extract group names from extra_fields_groups
            for group in data['elabftw']['extra_fields_groups']:
                group_fields.append(group['name'])

            # Extract field values
            for k, v in data['extra_fields'].items():
              try:
                  print(f"Processing field: {k} = {v['value']}")
                  fields_details[k] = v['value']
              except KeyError:
                  print(f"field  missing 'value' for the key: {k}")
                  fields_details[k] = ""

            # Extract modalit
              # y information from group names
            modaity_list = []
            for group_name in group_fields:
                if group_name.startswith('MODALITY'):
                    modality = group_name.split('_')[-1]
                    modaity_list.append(modality)
            #fields_details['modality'] = modaity_list
            fields_details['modality'] = modaity_list




            list_experiement_details.append(fields_details)
        else:
            raise ValueError(
                "No 'elabftw' or 'extra_fields' found in the JSON file.")

    # Save the processed data to CSV
    df = pd.DataFrame(list_experiement_details)
    df.to_csv(output_csv_file, index=False)


def main() -> None:
    """
    Main function to demonstrate the usage of get_experiement_details.

    This function serves as an entry point for command-line execution.
    It downloads experiment data using elab_bridge and saves the output to a CSV file.
    """
    try:
        # Configuration parameters
        config_file = "/home/INT/idrissou.f/Bureau/diglab/elabConf.json"  # Path to your configuration file
        metadata_file = "metadata.csv" # Path where to save the downloaded metadata
        tag = "FF"
        #tag = "testt"  # Tag to filter experiments
        output_file = "output.csv"  # Output CSV file

        print(f"Downloading experiment data with tag: {tag}")
        get_experiement_details(
            config_file_path=config_file,
            metada_file_path=metadata_file,
            tag=tag,
            output_csv_file=output_file
        )
        print(f"Successfully saved processed data to: {output_file}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    main()
