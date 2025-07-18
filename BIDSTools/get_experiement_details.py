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

import elab_bridge

from elab_bridge import server_interface
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

    experiement_details = elab_bridge.server_interface.extended_download(
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
                print(f"Processing field: {k} = {v['value']}")
                fields_details[k] = v['value']

            # Extract modality information from group names
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
        tag = "FF"  # Tag to filter experiments
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
