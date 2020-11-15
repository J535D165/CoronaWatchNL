from pathlib import Path
import itertools

import pandas as pd
import numpy as np
import re
import datetime
#from utils import convert_to_int

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

DATA_FOLDER = Path("data-desc")

VARIABLES = [
    "Totaal",
    "Ziekenhuisopname",
    "Overleden"
]


def get_timeline():

    df = pd.read_csv(Path("data", "rivm_NL_covid19_sex.csv"))
    dates = sorted(df["Datum"].unique())

    return dates


def export_date(df, data_folder, prefix, data_date=None, label=None):

    if data_date:
        df_date = df.loc[df["Datum"] == data_date, :]
    else:
        df_date = df

    # export with data date
    if label is not None:
        export_path = Path(DATA_FOLDER, data_folder, f"{prefix}_{label}.csv")
    else:
        export_path = Path(DATA_FOLDER, data_folder, f"{prefix}.csv")

    print(f"Export {export_path}")
    df_date.to_csv(export_path, index=False)



def main_sex():

    df_reported = pd.read_csv(Path("data-desc", "data-sex", "RIVM_NL_sex.csv"))
    df_reported["Aantal"] = df_reported["Aantal"].astype(pd.Int64Dtype())

    dates = sorted(df_reported["Datum"].unique())

    # export by date
    for data_date in dates:

        export_date(df_reported, "data-sex", "RIVM_NL_sex", data_date, str(data_date).replace("-", ""))

    # export latest
    export_date(df_reported, "data-sex", "RIVM_NL_sex", data_date=dates[-1], label="latest")


def main_age():

    df_reported = pd.read_csv(Path("data-desc", "data-age", "RIVM_NL_age.csv"))
    df_reported["Aantal"] = df_reported["Aantal"].astype(pd.Int64Dtype())

    dates = sorted(df_reported["Datum"].unique())

    # export by date
    for data_date in dates:

        export_date(df_reported, "data-age", "RIVM_NL_age", data_date, str(data_date).replace("-", ""))

    # export latest
    export_date(df_reported, "data-age", "RIVM_NL_age", data_date=dates[-1], label="latest")


def main_age_sex():

    DATA_FOLDER_INPUT = Path("raw_data/website_charts")
    files = DATA_FOLDER_INPUT.glob('*leeftijd-en-geslacht-overledenen*')

    df = []
    for file in files:
        match = re.search('\d{4}-\d{2}-\d{2}', f'{file}')
        date = datetime.datetime.strptime(match.group(), '%Y-%m-%d').date()

        new = pd.read_csv(file, sep = ';')
        new['Datum'] = date

        genders = ['Vrouw', 'Man']

        for geslacht in genders:
            new_man = new[[
                "Datum",
                "Leeftijdsgroep",
                geslacht
            ]]

            new_man['Geslacht'] = geslacht
            new_man = new_man.rename(columns={geslacht:'AantalCumulatief', 'Leeftijdsgroep':'LeeftijdGroep'})

            df.append(new_man)


    df_reported = pd.concat(df, axis=0, ignore_index=True)
    df_reported = df_reported.sort_values(by = ['Datum', 'Geslacht', 'LeeftijdGroep'])

    df_reported["Aantal"] = df_reported \
    .groupby(['Geslacht', 'LeeftijdGroep'], sort=True)['AantalCumulatief'] \
    .transform(pd.Series.diff)

    df_reported.loc[df_reported["Datum"] == sorted(df_reported["Datum"].unique())[0], "Aantal"] = \
    df_reported.loc[df_reported["Datum"] == sorted(df_reported["Datum"].unique())[0], "AantalCumulatief"]

    df_reported['Aantal'] = df_reported["Aantal"].astype(pd.Int64Dtype())

    Path(DATA_FOLDER, "data-deceased").mkdir(exist_ok=True)

    df_reported = df_reported[[
        "Datum",
        "LeeftijdGroep",
        "Geslacht",
        "Aantal",
        "AantalCumulatief"
    ]]

    dates = sorted(df_reported["Datum"].unique())

    # export by date
    for data_date in dates:

        export_date(df_reported, "data-deceased", "RIVM_NL_deceased_age_sex", data_date, str(data_date).replace("-", ""))

    # export latest
    export_date(df_reported, "data-deceased", "RIVM_NL_deceased_age_sex", data_date=dates[-1], label="latest")

    # export all
    export_date(df_reported, "data-deceased", "RIVM_NL_deceased_age_sex", data_date=None, label=None)



if __name__ == '__main__':

    DATA_FOLDER.mkdir(exist_ok=True)

    main_sex()

    main_age()

    main_age_sex()


