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
    return result.sort_index()

if __name__ == '__main__':

    df = pandas.read_csv(Path("data", "rivm_corona_in_nl.csv"))

    daily_data(df).to_csv(Path("data", "rivm_corona_in_nl_daily.csv"))
