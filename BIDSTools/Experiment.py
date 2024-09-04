import csv as csv
import json


class Experiment:
    def __init__(self, **kwargs):
        cleaned_kwargs = {key.strip(): value for key, value in kwargs.items()}
        self.__dict__.update(cleaned_kwargs)

    def get_attribute(self, name):
        if name in self.__dict__:
            return self.__dict__[name]
        else:
            raise AttributeError(f"'Experiment' object has no attribute '{name}'")

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

