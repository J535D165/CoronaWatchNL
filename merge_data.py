"""Merge RIVM daily stats"""

from pathlib import Path
import re
import datetime
from io import StringIO

import pandas


DATE_MAP = {
    "maart": 3,
    "april": 4,
    "mei": 5,
}


def list_files():

    return [p for p in Path('raw_data').iterdir() if p.is_file()]


def parse_format_v3(file, n_missing=None):

    date_parts = re.findall(r'(\d{1,2})-(.*?)-(\d{4})', str(file))[0]

    # find date
    date = datetime.date(
        int(date_parts[2]),
        int(date_parts[1]),
        int(date_parts[0])
    )

    df = pandas.read_csv(file, sep=";")

    # find the number of missing locations
    missing = re.findall(
        r'Bij (\d+) personen is de woonplaats niet van bekend',
        df.iat[0, 1]
    )
    try:
        n_missing = int(missing[0])
    except Exception:
        pass

    try:
        df['id'] = df['Gemnr'].astype(int)
        del df['Gemnr']
    except Exception:
        pass

    # remove junk rows
    df = df[df['id'] >= 0].copy()

    # append row with missing numbers
    df = df.append({
        "Gemeente": None,
        "id": -1,
        "Aantal": n_missing},
        ignore_index=True)

    # print(df.tail())

    # add column with date
    df['Datum'] = date

    return df


def parse_format_v4(file, n_missing=None):

    date_parts = re.findall(r'(\d{1,2})-(.*?)-(\d{4})', str(file))[0]

    # find date
    date = datetime.date(
        int(date_parts[2]),
        int(date_parts[1]),
        int(date_parts[0])
    )

    df = pandas.read_csv(file, sep=";")

    # find the number of missing locations
    missing = re.findall(
        r'Bij (\d+) personen is de woonplaats niet van bekend',
        df.iat[0, 1]
    )
    try:
        n_missing = int(missing[0])
    except Exception:
        pass

    try:
        df['id'] = df['Gemnr'].astype(int)
        del df['Gemnr']
    except Exception:
        pass

    # remove junk rows
    df = df[df['id'] >= 0].copy()

    df["Aantal"] = df["Zkh opname"]

    # append row with missing numbers
    df = df.append({
        "Gemeente": None,
        "id": -1,
        "Aantal": n_missing},
        ignore_index=True)

    # print(df.tail())

    # add column with date
    df['Datum'] = date

    df = df[["Datum", "Gemeente", "id", "Aantal"]]

    print(df)

    return df


def merge_df_days(df_dict):

    result = pandas.concat(
        df_dict.values(),
        axis=0,
        sort=False
    ).dropna(axis=0, subset=["Aantal"])

    result['Aantal'] = result['Aantal'].astype(int)

    return result


if __name__ == '__main__':

    df_frames = {
        "raw_data/peildatum-31-03-2020-14-00.csv": None,
        "raw_data/peildatum-08-04-2020-13-55.csv": parse_format_v4("raw_data/peildatum-08-04-2020-13-55.csv"),
    }

    # files not in the list above
    for file in Path('raw_data').glob('peildatum*.csv'):
        if str(file) not in df_frames.keys():
            print(f"Parse file {file}")
            df_frames[str(file)] = parse_format_v3(file)

    result = merge_df_days(df_frames)

    # add municipality to data
    df_mun = pandas.read_csv(
        Path("ext", "Gemeenten_alfabetisch_2019.csv"), sep=";"
    )[["Gemeentecode", "Gemeentenaam", "Provincienaam"]]

    result = result.\
        merge(df_mun, left_on="id", right_on="Gemeentecode", how="left").\
        drop(["id"], axis=1)
    result = result[
        ["Datum", "Gemeentenaam", "Gemeentecode", "Provincienaam", "Aantal"]
    ].sort_values(["Datum", "Gemeentecode"]). \
        fillna({"Gemeentecode": -1})

    result["Gemeentecode"] = result["Gemeentecode"].astype(int)

    result = result[result["Aantal"] != 0]

    print(result.tail())
    result.to_csv(Path("data", "rivm_NL_covid19_hosp_municipality.csv"), index=False)
