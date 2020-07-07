from pathlib import Path
import itertools

import pandas as pd
import numpy as np

from utils import convert_to_int

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

DATA_FOLDER = Path("data-geo")

VARIABLES = [
    "Totaal",
    "Ziekenhuisopname",
    "Overleden"
]


def get_municipalities(return_missing=True):

    # add municipality to data
    list_mun = pd.read_csv(
        Path("ext", "Gemeenten_alfabetisch_2019.csv"), sep=";"
    )["Gemeentecode"].tolist()

    if return_missing:
        # append -1 for the missing values
        list_mun.append(-1)

    return list_mun


def get_timeline():

    df = pd.read_csv(Path("data", "rivm_NL_covid19_national.csv"))
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


def main_national():

    df_reported = pd.read_csv(Path("data", "rivm_NL_covid19_national.csv"))
    # df_reported["DatumType"] = "Gemeld in laatste 24 uur"
    # df_reported["Waarde"] = "Cumulatief"
    df_reported["AantalCumulatief"] = df_reported["Aantal"]
    # df_reported['Opmerking'] = np.nan
    df_reported["Aantal"] = df_reported \
        .groupby('Type', sort=True)['AantalCumulatief'] \
        .transform(pd.Series.diff)


    #df_reported.loc[df_reported["Datum"] == "2020-02-27", "Aantal"] = \
        #df_reported.loc[df_reported["Datum"] == "2020-02-27", "AantalCumulatief"]

    df_reported['Aantal'] = df_reported["Aantal"].astype(pd.Int64Dtype())
    df_reported['AantalCumulatief'] = df_reported["AantalCumulatief"].astype(pd.Int64Dtype())

    # format the columns
    df_reported = df_reported[[
        "Datum",
        "Type",
        "Aantal",
        "AantalCumulatief",
        # "Opmerking"
    ]]

    Path(DATA_FOLDER, "data-national").mkdir(exist_ok=True)

    dates = sorted(df_reported["Datum"].unique())

    # export by date
    for data_date in dates:

        export_date(df_reported, "data-national", "RIVM_NL_national", data_date, str(data_date).replace("-", ""))

    # export latest
    export_date(df_reported, "data-national", "RIVM_NL_national", data_date=dates[-1], label="latest")


    # export all
    export_date(df_reported, "data-national", "RIVM_NL_national", data_date=None, label=None)


def _main_municipality():

    df_national = pd.read_csv(Path("data", "rivm_NL_covid19_national.csv"))

    df_fata = pd.read_csv(Path("data", "rivm_NL_covid19_fatalities_municipality.csv"))
    df_fata["Type"] = "Overleden"
    df_hosp = pd.read_csv(Path("data", "rivm_NL_covid19_hosp_municipality.csv"))
    df_hosp["Type"] = "Ziekenhuisopname"
    df_total = pd.read_csv(Path("data", "rivm_NL_covid19_total_municipality.csv"))
    df_total["Type"] = "Totaal"

    df = df_fata.append(df_hosp).append(df_total)

    df["AantalCumulatief"] = df["Aantal"]
    # df['Opmerking'] = np.nan
    df["Aantal"] = df \
        .groupby(['Gemeentecode', 'Type'], sort=True)['AantalCumulatief'] \
        .transform(pd.Series.diff)

    #df.loc[df["Datum"] == "2020-02-27", "Aantal"] = \
      #  df.loc[df["Datum"] == "2020-02-27", "AantalCumulatief"]

    df = df[[
        "Datum",
        "Gemeentecode",
        "Type",
        "Aantal",
        "AantalCumulatief",
        # "Opmerking"
    ]]

    combinations = itertools.product(
        get_timeline(),
        get_municipalities(),
        VARIABLES
    )
    df_base = pd.DataFrame(combinations, columns=["Datum", "Gemeentecode", "Type"])

    # add the municipality variables
    df_mun = pd.read_csv(
        Path("ext", "Gemeenten_alfabetisch_2019.csv"), sep=";"
    )[["Gemeentecode", "Gemeentenaam", "Provincienaam", "Provinciecode"]]

    df_base = df_base.\
        merge(df_mun, on="Gemeentecode", how="left"). \
        fillna({"Provinciecode": -1})

    # add the data to the dataframe
    df_extended = df_base.\
        merge(df, on=["Datum", "Gemeentecode", "Type"], how="left")

    # convert types
    for col in ["Provinciecode", "Aantal", "AantalCumulatief"]:
        df_extended[col] = df_extended[col].astype(pd.Int64Dtype())

    return df_extended


def main_municipality():

    df_extended = _main_municipality()

    Path(DATA_FOLDER, "data-municipal").mkdir(exist_ok=True)
    dates = sorted(df_extended["Datum"].unique())

    # format the columns
    df_extended = df_extended[[
        "Datum",
        "Gemeentecode",
        "Gemeentenaam",
        "Provincienaam",
        "Provinciecode",
        "Type",
        "Aantal",
        "AantalCumulatief",
        # "Opmerking"
    ]].sort_values(
        ["Datum", "Gemeentecode"])

    # export by date
    for data_date in dates:

        export_date(
            df_extended,
            "data-municipal",
            "RIVM_NL_municipal",
            data_date,
            str(data_date).replace("-", "")
        )

    # export latest
    export_date(df_extended, "data-municipal", "RIVM_NL_municipal", data_date=dates[-1], label="latest")


    # export all
    export_date(df_extended, "data-municipal", "RIVM_NL_municipal", data_date=None, label=None)


def main_province():

    df_extended = _main_municipality()

    df_extended = df_extended \
        .fillna({"Gemeentenaam":"",  "Provincienaam":""}) \
        .groupby(["Datum", "Provincienaam", "Provinciecode", "Type"])["Aantal", "AantalCumulatief"] \
        .apply(lambda x: x.sum(min_count=1)) \
        .reset_index()
    # df_extended['Opmerking'] = np.nan

    df_extended.loc[df_extended["Provinciecode"] == -1, ["Provincienaam"]] = np.nan

    df_extended = convert_to_int(df_extended, ["Aantal", "AantalCumulatief", "Provinciecode"])

    # format the columns
    df_extended = df_extended[[
        "Datum",
        "Provincienaam",
        "Provinciecode",
        "Type",
        "Aantal",
        "AantalCumulatief",
        # "Opmerking"
    ]].sort_values(
        ["Datum", "Provinciecode"])

    Path(DATA_FOLDER, "data-provincial").mkdir(exist_ok=True)
    dates = sorted(df_extended["Datum"].unique())

    # export by date
    for data_date in dates:

        export_date(
            df_extended,
            "data-provincial",
            "RIVM_NL_provincial",
            data_date,
            str(data_date).replace("-", "")
        )

    # export latest
    export_date(df_extended, "data-provincial", "RIVM_NL_provincial", data_date=dates[-1], label="latest")


    # export all
    export_date(df_extended, "data-provincial", "RIVM_NL_provincial", data_date=None, label=None)



if __name__ == '__main__':

    DATA_FOLDER.mkdir(exist_ok=True)

    main_national()

    main_municipality()

    main_province()
