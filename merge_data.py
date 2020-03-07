"""Merge RIVM daily stats"""

from pathlib import Path
import re
import datetime

import pandas


def list_files():

    return [p for p in Path('raw_data').iterdir() if p.is_file()]


def merge_data(files):

    # make a selection of files per day
    include_files = {}
    for file in files:
        date = re.findall(r'\d{8}', str(file))
        if len(date) >= 1:
            include_files[date[0]] = file

    # load all the files
    df_files = []
    for date, file in include_files.items():
        df = pandas.read_csv(file, sep=";", decimal=",")

        try:
            df['id'] = df['id'].astype(int)
        except Exception:
            pass

        df['Datum'] = datetime.date(
            int(date[4:8]),
            int(date[2:4]),
            int(date[0:2])
        )

        df_files.append(df)

    # merge the files
    result = pandas.concat(df_files, axis=0)

    # correct columns
    result['Aantal'] = result['Aantal'].astype(pandas.Int64Dtype())

    return result

if __name__ == '__main__':

    files = list_files()
    result = merge_data(files)
    result.to_csv(Path("data", "rivm_corona_in_nl.csv"), index=False)
