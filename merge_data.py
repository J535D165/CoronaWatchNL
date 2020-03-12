"""Merge RIVM daily stats"""

from pathlib import Path
import re
import datetime

import pandas


def list_files():

    return [p for p in Path('raw_data').iterdir() if p.is_file()]


def parse_old_format(file):

    date = re.findall(r'\d{8}', str(file))[0]

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

    return df


def parse_new_format(file):

    date = re.findall(r'(\d{2})-maart', str(file))[0]

    df = pandas.read_csv(file, sep=";")

    try:
        df['id'] = df['Gemnr'].astype(int)
        del df['Gemnr']
    except Exception:
        pass

    df['Datum'] = datetime.date(
        2020,
        3,
        int(date[0:2])
    )

    return df[df['id'] >= 0]

if __name__ == '__main__':

    df_frames = [
        parse_old_format("raw_data/reconstruct_corona_27022020.csv"),
        parse_old_format("raw_data/reconstruct_corona_28022020.csv"),
        parse_old_format("raw_data/reconstruct_corona_29022020.csv"),
        parse_old_format("raw_data/reconstruct_corona_01032020.csv"),
        parse_old_format("raw_data/klik_corona03032020.csv"),
        parse_old_format("raw_data/klik_corona04032020.csv"),
        parse_old_format("raw_data/klik_corona05032020.csv"),
        # parse_old_format("raw_data/klik_corona06032020.csv"),
        parse_old_format("raw_data/klik_corona06032020_rec_0.csv"),
        parse_old_format("raw_data/klik_corona07032020.csv"),
        parse_old_format("raw_data/klik_corona08032020_rectificatie.csv"),
        # parse_old_format("raw_data/klik_corona08032020_v2.csv"),
        # parse_old_format("raw_data/klik_corona08032020_v2_0.csv"),
        # parse_old_format("raw_data/klik_corona09032020_0.csv"),
        parse_old_format("raw_data/klik_corona09032020_1.csv"),
        parse_old_format("raw_data/klik_corona10032020_2.csv"),
        # parse_old_format("raw_data/klik_corona11032020.csv"),
        parse_old_format("raw_data/klik_corona11032020rectificatie.csv"),
    ]

    files = [p for p in Path('raw_data').iterdir()
             if p.is_file() and p.stem.startswith("peildatum")]
    print(files)

    result = pandas.concat(
        [parse_new_format(f) for f in files] + df_frames,
        axis=0,
        sort=False
    ).sort_values(["Datum", "id"])
    del result["Indicator"]

    result['Aantal'] = result['Aantal'].astype(pandas.Int64Dtype())

    print(result.tail())

    result.to_csv(Path("data", "rivm_corona_in_nl.csv"), index=False)
