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
    else:
        with open(path_to_save, 'w') as outfile:
            json.dump(new_dict, outfile)


def mergejson(new_data,data_existing):
        # todo : comment
        for new_key in new_data.keys():
            if new_key not in data_existing :
                data_existing[new_key] = new_data[new_key]
            else:
                if not hasattr(data_existing[new_key], '__iter__') and new_data[new_key] == data_existing[new_key]:
                    pass
                elif not hasattr(data_existing[new_key], '__iter__') and new_data[new_key] != data_existing[new_key]:
                    print(f"Error different values for the same key {new_key} : {new_data[new_key]} {data_existing[new_key]}")
                if type(data_existing[new_key]) == list :
                    data_existing[new_key].extend(new_data[new_key])
                elif type(data_existing[new_key]) == dict :
                    mergejson(new_data[new_key],data_existing[new_key])

