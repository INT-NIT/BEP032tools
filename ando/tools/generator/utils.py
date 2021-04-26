from os import path
import pandas as pd
import os


def save_tsv(dataframe, path_to_save):
    if path.exists(path_to_save):
        df = pd.read_csv(os.path.join(path_to_save), sep='\t')
        output = df.append(dataframe, sort=True)
        output.to_csv(path_to_save, sep="\t", index=False)

    else:
        dataframe.to_csv(path_to_save, sep="\t", index=False)
