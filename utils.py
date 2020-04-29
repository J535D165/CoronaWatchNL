from pathlib import Path

import pandas as pd


def get_municipalities(return_missing=True):

    # add municipality to data
    list_mun = pd.read_csv(
        Path("ext", "Gemeenten_alfabetisch_2019.csv"), sep=";"
    )["Gemeentecode"].tolist()

    if return_missing:
        # append -1 for the missing values
        list_mun.append(-1)

    return list_mun


def convert_to_int(df, cols):

    df_ = df.copy()

    for col in cols:
        df_[col] = df_[col].astype(pd.Int64Dtype())

    return df_
