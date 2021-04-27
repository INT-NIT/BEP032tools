from os import path
import pandas as pd
import os
import json

def save_tsv(dataframe, path_to_save):
    if path.exists(path_to_save):
        df = pd.read_csv(os.path.join(path_to_save), sep='\t')
        output = df.append(dataframe, sort=True)
        output.to_csv(path_to_save, sep="\t", index=False)

    else:
        dataframe.to_csv(path_to_save, sep="\t", index=False)

def save_json(new_dict, path_to_save):
    if path.exists(path_to_save):
        with open(path_to_save) as json_file:
            data_existing = json.load(json_file)
            mergejson(data_existing,new_dict)
                    # todo : check other possibility
    else:
        with open(path_to_save, 'w') as outfile:
            json.dump(dict, outfile)


def mergejson(data_existing,new_data):
    for key_exist in list(data_existing.keys()):
        for new_key in new_data.keys():
            if type(data_existing[key_exist]) == str and key_exist == new_key and data_existing[key_exist] == new_data[new_key]:
                print('error')
            if type(data_existing[key_exist]) == str and key_exist != new_key:
                data_to_append = {new_key: new_data[new_key]}
                data_existing.update(data_to_append)
            if type(data_existing[key_exist]) == list and key_exist == new_key:
                data_existing[key_exist].extend(new_data[new_key])
            if type(data_existing[key_exist]) == dict and key_exist == new_key :
                mergejson(data_existing[key_exist],new_data[new_key])


