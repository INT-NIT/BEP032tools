"""
BidsDatatype.py

This module loads and manages data types defined by the BIDS (Brain Imaging Data Structure) standard.
It provides utilities to retrieve data type values from a YAML schema and facilitates working with BIDS-compliant datasets.

Main Features:
- Loads all BIDS data types from a YAML configuration file.
- Provides access to data type names and values.
- Facilitates lookup of data type values by name.

Typical Usage:
    from BIDSTools.BidsDatatype import DataTypes
    datatypes = DataTypes()
    value = datatypes.get_data_type_value("anat")

Refer to the BIDS specification for more details on data type definitions.
"""
import yaml
from BIDSTools.resource_paths import DATATYPES_YAML
from BIDSTools.helper import load_yaml_file



class DataTypes:
    def __init__(self):
        """
        Initialize a DataTypes object and load data types from a YAML file.
        """
        self.data_types = load_yaml_file(DATATYPES_YAML)

    def get_data_type_value(self, data_type_name):
        """
        Get the value of a specific data type.

        Args:
            data_type_name (str): The name of the data type to retrieve.

        Returns:
            str: The value of the data type, or None if the data type does not exist.
        """
        return self.data_types.get(data_type_name, {}).get("value")

    def get_data_type_list(self):
        """
                Retrieve a list of all data type names.

                Returns:
                    list: A list of strings, each representing a data type name.
        """
        return list(self.data_types.keys())


def main():
    """
    Main function to demonstrate the usage of the DataTypes class.
    """
    data_types = DataTypes()
    data_type_name = "anat"
    data_type = data_types.get_data_type_value(data_type_name)
    print(data_types.get_data_type_list())


if __name__ == "__main__":
    main()
