import copy
import json
import os
from pathlib import Path

import pandas as pd


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
    path_to_save = path_to_save.with_suffix('.tsv')

    # Check if path exist and if the file is empty
    if Path(path_to_save).exists() and os.path.getsize(path_to_save) > 1:
        existing_df = pd.read_csv(path_to_save, sep='\t', index_col=0)
        merged_dfs = merge_dfs_by_index(existing_df, dataframe)
        merged_dfs.to_csv(path_to_save, sep="\t", index=True)

    else:
        dataframe.to_csv(path_to_save, sep="\t", index=True)


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
    path_to_save = path_to_save.with_suffix('.json')

    if Path(path_to_save).exists():
        with open(path_to_save, 'r') as json_file:
            data_existing = json.load(json_file)
            new_dict = merge_dict(data_existing, data_dict)
        with open(path_to_save, 'w+') as json_file:
            json.dump(new_dict, json_file)
    else:
        with open(path_to_save, 'w') as json_file:
            json.dump(data_dict, json_file)


def merge_dict(original_data, new_data):
    """
    Merge two dictionaries.
   
    Merge the content of a `new` dictionary into another, `original` dictionary.
    A new dictionary with the merged content is created. Values are preserved
    and a ValueError is raised if incompatible content is encountered.
    Overlapping lists are extended and nested dictionaries are merged
    recursively.

    Parameters
    ----------
    original_data : dict
        data to merge in the already existing json file
    new_data : dict
        the already existing json file convert to dict

    Raises
    ----------
    ValueError
        if the data type of the value is neither iterable or basic dtype

    """
    # deep copying input dictionary to not overwrite existing values in-place
    result = copy.deepcopy(original_data)
    for key in new_data.keys():
        if key not in original_data:
            # new entry that does not exist -> just added it
            result[key] = new_data[key]
        else:
            # if the values are simple and identical then no action required
            if not hasattr(original_data[key], '__iter__') \
                    and new_data[key] == original_data[key]:
                continue
            # contradicting values can not be merged
            elif not hasattr(original_data[key], '__iter__') \
                    and new_data[key] != original_data[key]:
                raise ValueError(f"Error different values for the same key "
                                 f"{key}: {new_data[key]} {original_data[key]}")
            # compare strings explicitly
            if isinstance(original_data[key], str):
                if original_data[key] == new_data[key]:
                    continue
                else:
                    raise ValueError(f"Error different values for the same key "
                                     f"{key}: {new_data[key]} "
                                     f"{original_data[key]}")
            # merge lists by concatenation of values
            if type(original_data[key]) == list:
                result[key].extend(new_data[key])
            # merge dictionaries recursively
            elif type(original_data[key]) == dict:
                result[key] = merge_dict(result[key], new_data[key])
            else:
                raise ValueError(f"Can not merge unexpected data type: "
                                 f"{type(original_data[key])}")

    return result


def merge_dfs_by_index(df1, df2):
    """
    Merge two pandas dataframe index-by-index.

    The dataframes have to share the same index name. Shared indexes will be
    merged without data loss. In case of conflicting entries a ValueError is 
    raised. The merge operation is symmetric and does not depend on the
    order of df1 and df2.

    Parameters
    ----------
    df1: dataframe
        Pandas dataframe to be extended
    df2: dataframe
        Pandas dataframe with used for extension
        
    Returns
    -------
    dataframe:
        The merged dataframe

    Raises
    ----------
    ValueError
        in case of incompatible index names or values
    """
    if df1.index.name != df2.index.name:
        raise ValueError('Dataframes have incompatible indexes: '
                         f'{df1.index.name} != {df2.index.name}.')

    # check for contradicting values by comparing A+B with B+A
    left_combine = df1.combine_first(df2)
    right_combine = df2.combine_first(df1)

    if not left_combine.equals(right_combine):
        raise ValueError('Dataframes have incompatible values: '
                         f'{left_combine.compare(right_combine)}')

    return right_combine

