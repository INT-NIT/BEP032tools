from os import path
import pandas as pd
import os
import json


def save_tsv(dataframe, path_to_save):
    """

    Parameters
    ----------
    dataframe: dataframe
        dataframe to save in a TSV format
    path_to_save: str
        path to save the TSV file

    Returns
    -------

    """
    if path.exists(path_to_save):
        df = pd.read_csv(path_to_save, sep='\t')
        output = df.append(dataframe, sort=True)
        output.to_csv(path_to_save, sep="\t", index=False)
    else:
        dataframe.to_csv(path_to_save, sep="\t", index=False)


def save_json(new_dict, path_to_save):
    """

    Parameters
    ----------
    new_dict: dict
        dict to save in a json format

    path_to_save

    Returns
    -------

    """
    if path.exists(path_to_save):
        with open(path_to_save) as json_file:
            data_existing = json.load(json_file)
            mergejson(data_existing, new_dict)
    else:
        with open(path_to_save, 'w') as outfile:
            json.dump(new_dict, outfile)


def mergejson(new_data, data_existing):
    """

    Parameters
    ----------
    new_data : dict
        data to merge in the already existing json file
    data_existing : dict
        the already existing json file convert to dict

    Returns
    -------

    """
    for new_key in new_data.keys():
        if new_key not in data_existing:
            # new entry that does not exist -> just added it
            data_existing[new_key] = new_data[new_key]
        else:
            # if the key are the same but not iterable just pass
            if not hasattr(data_existing[new_key], '__iter__') and new_data[new_key] == data_existing[new_key]:
                pass
            # contradicting values can not be merged
            elif not hasattr(data_existing[new_key], '__iter__') and new_data[new_key] != data_existing[new_key]:
                print(f"Error different values for the same key {new_key} : {new_data[new_key]} {data_existing[new_key]}")
            # merge lists by concatenation of values
            if type(data_existing[new_key]) == list:
                data_existing[new_key].extend(new_data[new_key])
            # merge dictionaries recursively
            elif type(data_existing[new_key]) == dict:
                mergejson(new_data[new_key], data_existing[new_key])
