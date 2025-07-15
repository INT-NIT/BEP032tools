"""
Experiment.py

This module defines the Experiment class for representing and managing experiment metadata in BIDS (Brain Imaging Data Structure) workflows.
Each experiment is typically initialized from a row in a metadata CSV file, with dynamic attributes for each metadata field.

Main Features:
- Dynamically creates attributes for each metadata field.
- Provides methods for attribute access, modification, and comparison.
- Integrates with BIDSTools for experiment-based data processing.

Typical Usage:
    from BIDSTools.Experiment import Experiment
    exp = Experiment(subject_id='01', session_id='01', modality='anat')
    print(exp.subject_id)

Refer to the BIDSTools documentation for more details on experiment management.
"""

import csv as csv
import json
import logging
"""
This class is designed to create an experiment.
Each experiment is represented by a line from a CSV file (which serves as our metadata file).
Each line has the following format: {key: value}, where {key} is a column name and {value} is the
corresponding column value.
For each experiment, a dynamic attribute is created for each {key} with its corresponding {value}.
"""


class Experiment:
    def __init__(self, **kwargs):
        cleaned_kwargs = {key.strip(): value for key, value in kwargs.items()}
        self.__dict__.update(cleaned_kwargs)

    def get_attribute(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
          logger = logging.getLogger(__name__)
          logger.warning(f"'Experiment' object has no attribute '{name}'")
          return None

    def set_attribute(self, name, value):
        self.__dict__[name] = value

    def __eq__(self, other):
        if isinstance(other, Experiment):
            other_dict = other.__dict__
            filtered_other_dict = {key: other_dict.get(key, '') for key in self.__dict__}

            return self.__dict__ == filtered_other_dict
        return False

    def __ne__(self, other):
        return not self.__eq__(other)

    def to_dict(self):
        return self.__dict__

    def to_json_string(self):
        return json.dumps(self.to_dict(), sort_keys=True)

    def display(self):
        print(self.to_dict())
