"""Merge RIVM daily stats"""

from pathlib import Path
import re
import datetime
from io import StringIO

import pandas


DATE_MAP = {
    "maart": 3,
    "april": 4,
    "juni": 5,
}


def list_files():

    return [p for p in Path('raw_data').iterdir() if p.is_file()]


def parse_format_v1(file, total=None):

    date = re.findall(r'\d{8}', str(file))[0]
    date = datetime.date(
        int(date[4:8]),
        int(date[2:4]),
        int(date[0:2])
    )

    df = pandas.read_csv(file, sep=";", decimal=",")

    try:
        df['id'] = df['id'].astype(int)
    except Exception:
        pass

    n_without_missing = df['Aantal'].sum()

    if total:

        n_missing = total - n_without_missing

        if n_missing > 0:
            df = df.append({
                "Gemeente": None,
                "id": -1,
                "Aantal": n_missing},
                ignore_index=True)

    df['Datum'] = date

    del df["Indicator"]

    return df


def parse_format_v2(file, n_missing=None):

    # find date
    date = datetime.date(
        2020,
        3,
        int(re.findall(r'(\d{2})-maart', str(file))[0][0:2])
    )

    # read file
    if file == "raw_data/peildatum-13-maart-14-00.csv":
        result_list = []
        with open(file, "r") as f:
            for line in f:
                extr_first = re.findall(r'(.*;.*;.*);.*', line)
                if extr_first:
                    result_list.append(extr_first[0])
                else:
                    result_list.append(line.rstrip())
        df = pandas.read_csv(StringIO("\n".join(result_list)), sep=";")
    else:
        df = pandas.read_csv(file, sep=";")

    try:
        df['id'] = df['Gemnr'].astype(int)
        del df['Gemnr']
    except Exception:
        pass

    # find the number of missing locations
    missing = re.findall(
        r'postcode ontbreekt bij (\d+) pt en (\d+) woont in buitenland', 
        df.iat[1, 0]
    )
    try:
        n_missing = int(missing[0][0])  # + int(missing[0][1]) ## Exclude 'buitenland'
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


def parse_format_v3(file, n_missing=None):

    date_parts = re.findall(r'(\d{1,2})-(.*?)-(\d{4})', str(file))[0]

    # find date
    date = datetime.date(
        int(date_parts[2]),
        DATE_MAP[date_parts[1]],
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
        "raw_data/reconstruct_corona_27022020.csv":
            parse_format_v1(
                "raw_data/reconstruct_corona_27022020.csv"),
        "raw_data/reconstruct_corona_28022020.csv":
            parse_format_v1(
                "raw_data/reconstruct_corona_28022020.csv"),
        "raw_data/reconstruct_corona_29022020.csv":
            parse_format_v1(
                "raw_data/reconstruct_corona_29022020.csv"),
        "raw_data/reconstruct_corona_01032020.csv":
            parse_format_v1(
                "raw_data/reconstruct_corona_01032020.csv", total=10),
        "raw_data/reconstruct_corona_02032020.csv":
            parse_format_v1(
                "raw_data/reconstruct_corona_02032020.csv", total=18),
        "raw_data/klik_corona03032020.csv":
            parse_format_v1(
                "raw_data/klik_corona03032020.csv", total=24),
        "raw_data/klik_corona04032020.csv":
            parse_format_v1(
                "raw_data/klik_corona04032020.csv", total=38),
        "raw_data/klik_corona05032020.csv":
            parse_format_v1(
                "raw_data/klik_corona05032020.csv", total=82),
        "raw_data/klik_corona06032020.csv": None,
        "raw_data/klik_corona06032020_rec_0.csv":
            parse_format_v1(
                "raw_data/klik_corona06032020_rec_0.csv", total=128),
        "raw_data/klik_corona07032020.csv":
            parse_format_v1(
                "raw_data/klik_corona07032020.csv", total=188),
        "raw_data/klik_corona08032020_rectificatie.csv":
            parse_format_v1(
                "raw_data/klik_corona08032020_rectificatie.csv", total=265),
        "raw_data/klik_corona08032020_v2.csv": None,
        "raw_data/klik_corona08032020_v2_0.csv": None,
        "raw_data/klik_corona09032020_0.csv": None,
        "raw_data/klik_corona09032020_1.csv":
            parse_format_v1(
                "raw_data/klik_corona09032020_1.csv", total=321),
        "raw_data/klik_corona10032020_2.csv":
            parse_format_v1(
                "raw_data/klik_corona10032020_2.csv", total=382),
        "raw_data/klik_corona11032020.csv": None,
        "raw_data/klik_corona11032020rectificatie.csv":
            parse_format_v1(
                "raw_data/klik_corona11032020rectificatie.csv", total=503),
        "raw_data/peildatum-12-maart-14-00.csv":
            parse_format_v2(
                "raw_data/peildatum-12-maart-14-00.csv"),
        "raw_data/peildatum-13-maart-14-00.csv":
            parse_format_v2(
                "raw_data/peildatum-13-maart-14-00.csv"),
        "raw_data/peildatum-14-maart-14-30.csv":
            parse_format_v2(
                "raw_data/peildatum-14-maart-14-30.csv"),
        "raw_data/peildatum-15-maart-14-00.csv":
            parse_format_v2(
                "raw_data/peildatum-15-maart-14-00.csv"),
        "raw_data/peildatum-16-maart-14-00.csv":
            parse_format_v2(
                "raw_data/peildatum-16-maart-14-00.csv"),
        "raw_data/peildatum-17-maart-14-00.csv":
            parse_format_v2(
                "raw_data/peildatum-17-maart-14-00.csv"),
        "raw_data/peildatum-18-maart-14-00.csv":
            parse_format_v2(
                "raw_data/peildatum-18-maart-14-00.csv"),
        "raw_data/peildatum-19-maart-14-00.csv":
            parse_format_v2(
                "raw_data/peildatum-19-maart-14-00.csv"),
        "raw_data/peildatum-20-maart-14-00.csv":
            parse_format_v2(
                "raw_data/peildatum-20-maart-14-00.csv", n_missing=112),
        "raw_data/peildatum-21-maart-14-00.csv":
            parse_format_v2(
                "raw_data/peildatum-21-maart-14-00.csv", n_missing=137),
        "raw_data/peildatum-22-maart-14-00.csv":
            parse_format_v2(
            "raw_data/peildatum-22-maart-14-00.csv", n_missing=155),  # wrong number in data file (55)
        "raw_data/peildatum-23-maart-14-30.csv":
            parse_format_v2(
                "raw_data/peildatum-23-maart-14-30.csv", n_missing=184),
        "raw_data/peildatum-24-maart-14-00.csv":
            parse_format_v2(
                "raw_data/peildatum-24-maart-14-00.csv", n_missing=200),
        "raw_data/peildatum-25-maart-14-00.csv":
            parse_format_v2(
                "raw_data/peildatum-25-maart-14-00.csv", n_missing=213),
        "raw_data/peildatum-26-maart-14-00.csv":
            parse_format_v2(
                "raw_data/peildatum-26-maart-14-00.csv", n_missing=237),
        "raw_data/peildatum-27-maart-14-00.csv":
            parse_format_v2(
                "raw_data/peildatum-27-maart-14-00.csv", n_missing=265),
        "raw_data/peildatum-28-maart-14-00.csv":
            parse_format_v2(
                "raw_data/peildatum-28-maart-14-00.csv", n_missing=279),
    }

    # files not in the list above
    for file in Path('raw_data').glob('peildatum*.csv'):
        if str(file) not in df_frames.keys():
            print(f"Parse file {file}")
            df_frames[str(file)] = parse_format_v3(file)

    result = merge_df_days(df_frames)

    # fix typos in peildatum 12 maart
    result.loc[result["Gemeente"] == "BeekDaelen", "Gemeente"] = \
        "Beekdaelen"
    result.loc[result["Gemeente"] == "Súdwest Fryslân", "Gemeente"] = \
        "Súdwest-Fryslân"

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
    result.to_csv(Path("data", "rivm_corona_in_nl.csv"), index=False)
