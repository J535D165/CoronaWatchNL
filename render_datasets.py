"""Merge RIVM daily stats"""

from pathlib import Path
import re
import datetime

import pandas
import numpy


def daily_data(data):

    result = data.groupby('Datum')[['Aantal']].sum()

    # manual edits
    result.loc['2020-03-02', 'Aantal'] = 18

    result['Aantal'] = result['Aantal'].astype(numpy.int64)
    print(result.sort_index())
    return result.sort_index()


def wide_data(data):

    key_cols = [col for col in list(data) if col != 'Aantal']

    df = data.\
        set_index(key_cols)['Aantal'].\
        fillna(0).\
        astype(int).\
        unstack('Datum', fill_value=0).\
        sort_values('Gemeentecode').\
        reset_index()

    # add municipality
    df_mun = pandas.read_csv(
        Path("ext", "Gemeenten_alfabetisch_2019.csv"), sep=";"
    )[["Gemeentenaam", "Gemeentecode", "Provincienaam"]].\
        merge(df, how="left").\
        sort_values("Gemeentecode")

    df_mun.iloc[:, 3:] = df_mun.iloc[:, 3:].fillna(0).astype(int)
    return df_mun

if __name__ == '__main__':

    df = pandas.read_csv(Path("data", "rivm_corona_in_nl.csv"))
    daily_data(df).to_csv(Path("data", "rivm_corona_in_nl_daily.csv"))

    df_wide = wide_data(df).to_csv(
        Path("data", "rivm_corona_in_nl_table.csv"),
        index=False
    )
