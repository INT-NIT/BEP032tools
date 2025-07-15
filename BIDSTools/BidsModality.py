"""
BidsModality.py

This module provides functionality to load and manage all modalities defined by the BIDS (Brain Imaging Data Structure) standard.
It enables retrieval of modality values based on their names, using a YAML schema as the source of truth for available modalities.

Main Features:
- Loads BIDS modalities from a YAML configuration file.
- Provides access to modality names and details.
- Facilitates lookup of modality information by name.

Typical Usage:
    modality = Modality()
    available_modalities = modality.modalities
    details = modality.modality_details
Example:
    modality = Modality()
    print("Available Modalities:", modality.modalities)
    print("Modality Details:", modality.modality_details)


See the BIDS specification for more details on modality definitions.
"""

import yaml
import os

from BIDSTools.resource_paths import MODALITIES_YAML
class Modality:
    def __init__(self, relative_path=None):
        """
        Initialize a Modality object with a path to a YAML file containing modalities.

        Args:
            relative_path (str, optional): Path to the YAML file containing modalities.
                If not provided, uses the default path in the resources directory.
        """
        if relative_path is None:
            # Get the directory where the current script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Construct the absolute path to modalities.yaml
            relative_path = os.path.join(script_dir, MODALITIES_YAML)
        
        self.relative_path = relative_path
        self.modalities = []
        self.modality_details = {}

        with open(relative_path, "r") as file:
            modalities_yaml = yaml.safe_load(file)
            if modalities_yaml:
               self.modalities = [p['display_name'].upper() for p in modalities_yaml.values()]

               self.modality_details = {p['display_name'].upper(): k for k, p in modalities_yaml.items()}

def main():
    """
    Main function to demonstrate the usage of the Modality class.
    """
    modality = Modality()


if __name__ == "__main__":
    main()
