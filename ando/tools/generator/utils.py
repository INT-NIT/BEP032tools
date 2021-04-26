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

def save_json(dict, path_to_save):
    if path.exists(path_to_save):
        with open(path_to_save) as json_file:
            data_existing = json.load(json_file)
            for key_exist in data_existing.keys():
                for new_key in dict.keys():
                    if type(data_existing[key_exist]) == str and data_existing[key_exist] == dict[new_key]:
                        print('Error')
                    # todo : check other possibility
    else:
        with open(path_to_save, 'w') as outfile:
            json.dump(dict, outfile)
