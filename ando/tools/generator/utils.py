import copy
from pathlib import Path
import pandas as pd
import json


def save_tsv(dataframe, path_to_save):
    """

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

    Parameters
    ----------
    data_dict: dict
        dict to save in a json format

    path_to_save: str
        path to save the JSON file

    """
    if Path(path_to_save).exists():
        with open(path_to_save) as json_file:
            data_existing = json.load(json_file)
            merge_dict(data_existing, data_dict)
            #overwrite
    else:
        with open(path_to_save, 'w') as outfile:
            json.dump(data_dict, outfile)


def merge_dict(original_data, data_existing):
    """

    Parameters
    ----------
    original_data : dict
        data to merge in the already existing json file
    data_existing : dict
        the already existing json file convert to dict

    Returns
    -------

    """
    # deep copy
    result = copy.deepcopy(data_existing)
    for key in original_data.keys():
        if key not in data_existing:
            # new entry that does not exist -> just added it
            result[key] = original_data[key]
        else:
            # if the values have a simple data type and are identical then nothing needs to be done
            if not hasattr(data_existing[key], '__iter__') and original_data[key] == data_existing[key]:
                pass
            # contradicting values can not be merged
            elif not hasattr(data_existing[key], '__iter__') and original_data[key] != data_existing[key]:
                print(f"Error different values for the same key {key} : {original_data[key]} {data_existing[key]}")
            # merge lists by concatenation of values
            if type(data_existing[key]) == list:
                result[key].extend(original_data[key])
            # merge dictionaries recursively
            elif type(data_existing[key]) == dict:
                merge_dict(original_data[key], result[key])
            else:
                raise ValueError()

    return result
