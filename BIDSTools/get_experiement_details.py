"""
Module for processing experiment details from JSON format to CSV.

This module provides functionality to extract and transform experiment data
from a specific JSON structure into a tabular CSV format, making it easier
to analyze and work with the data in spreadsheet applications or data analysis tools.
"""

import json
import os
from typing import Dict, List, Any
import pandas as pd


def get_experiement_details(experiement_json_file: str,
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

    Example:
        >>> get_experiement_details("experiment_data.json", "output.csv")
    """
    with open(experiement_json_file, 'r') as f:
        experiement_details = json.load(f)

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
    It processes a specific JSON file and saves the output to a CSV file.
    """
    try:
        input_file = "/home/INT/idrissou.f/PycharmProjects/BEP032tools/BIDSTools/ffffff.json"
        output_file = "output.csv"

        print(f"Processing experiment data from: {input_file}")
        get_experiement_details(input_file, output_file)
        print(f"Successfully saved processed data to: {output_file}")

    except Exception as e:
        print(f"An error occurred: {str(e)}")
        raise


if __name__ == "__main__":
    main()