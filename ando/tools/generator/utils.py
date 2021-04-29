import copy
from pathlib import Path
import pandas as pd
import json


def save_tsv(dataframe, path_to_save):
    """
    Append or create a tsv file corresponding of dataframe data
    Parameters
    ----------
    dataframe: dataframe
        dataframe to save in a TSV format
    path_to_save: str
        path to save the TSV file

    """
    if Path(path_to_save).exists():
        df = pd.read_csv(path_to_save, sep='\t')
        output = df.append(dataframe, sort=True)
        output.to_csv(path_to_save, sep="\t", index=False)

    else:
        dataframe.to_csv(path_to_save, sep="\t", index=False)


def save_json(data_dict, path_to_save):
    """
    Append or create a json file corresponding of dict data

    Parameters
    ----------
    data_dict: dict
        dict to save in a json format

    path_to_save: str
        path to save the JSON file

    """
    if Path(path_to_save).exists():
        with open(path_to_save,'r+') as json_file:
            data_existing = json.load(json_file)
            new_dict = merge_dict(data_existing, data_dict)
            json.dump(new_dict, json_file)
    else:
        with open(path_to_save, 'w') as json_file:
            json.dump(data_dict, json_file)


def merge_dict(original_data, new_data):
    """
    Merge two dictionaries.
   
   Merge the content of a `new` dictionary into another, `original` dictionary. A new 
   dictionary with the merged content is created. Values are preserved and a ValueError is
   raised if incompatible content is encountered. Overlapping lists are extended and nested
   dictionaries are merged recursively.

    Parameters
    ----------
    original_data : dict
        data to merge in the already existing json file
    new_data : dict
        the already existing json file convert to dict

    """
    # deep copying input dictionary to not overwrite existing values in-place
    result = copy.deepcopy(new_data)
    for key in original_data.keys():
        if key not in new_data:
            # new entry that does not exist -> just added it
            result[key] = original_data[key]
        else:
            # if the values have a simple data type and are identical then nothing needs to be done
            if not hasattr(new_data[key], '__iter__') and original_data[key] == new_data[key]:
                pass
            # contradicting values can not be merged
            elif not hasattr(new_data[key], '__iter__') and original_data[key] != new_data[key]:
                raise ValueError(f"Error different values for the same key {key} : {original_data[key]} {new_data[key]}")
            # merge lists by concatenation of values
            if type(new_data[key]) == list:
                result[key].extend(original_data[key])
            # merge dictionaries recursively
            elif type(new_data[key]) == dict:
                merge_dict(original_data[key], result[key])
            else:
                raise ValueError("Can not merge unexpected data type: {type(data_existing)}")

    return result
