from pathlib import Path
import itertools

import pandas as pd
import numpy as np

pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

DATA_FOLDER = Path("data-ic")

def get_timeline():

    df = pd.read_csv(Path("data", "nice_ic_by_day.csv"))
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

# NICE data
VARIABLES = [
    "icCount",
    "new",
    "intakeCount",
    "intakeCumulative",
    "survivedCumulative",
    "diedCumulative",
    "dischargedTotal"
]

TYPE = [
    "Totaal ingezette IC's",
    "Toename opnamen (IC)",
    "Totaal opnamen (IC)",
    "Cumulatief opnamen (IC)",
    "Cumulatief ontslag (ziekenhuis)",
    "Cumulatief ontslag (overleden)",
    "Totaal ontslag (IC)",
    "Toename ontslag (ziekenhuis)",
    "Toename ontslag (overleden)",
]

def main_long_nice():

    df_reported = pd.read_csv(Path("data", "nice_ic_by_day.csv"))
    df_reported['new'] = df_reported['newIntake'] + df_reported['newSuspected']
    df_reported['Type'] = 'NA'

    big = pd.DataFrame([])
    for i in VARIABLES:
        new = df_reported[['Datum', i, 'Type']]
        new = new.rename(columns={i: "Aantal"})
        new['Type'] = TYPE[VARIABLES.index(i)]
        big = big.append(new, ignore_index = True)

    new = pd.DataFrame([])
    new = big.loc[big['Type'].isin(["Cumulatief ontslag (ziekenhuis)", "Cumulatief ontslag (overleden)"])]
    new["AantalCumulatief"] = new["Aantal"]
    new.loc[new["Type"] == "Cumulatief ontslag (ziekenhuis)", "Type"] = "Toename ontslag (ziekenhuis)"
    new.loc[new["Type"] == "Cumulatief ontslag (overleden)", "Type"] = "Toename ontslag (overleden)"
    new["Aantal"] = new \
        .groupby('Type', sort=True)['AantalCumulatief'] \
        .transform(pd.Series.diff)
    new.loc[new["Datum"] == "2020-02-27", "Aantal"] = \
        new.loc[new["Datum"] == "2020-02-27", "AantalCumulatief"]

    big = big.append(new, sort = False)
    big = big.sort_values('Datum', ascending=True)
    big = big.reset_index(drop=True)

    big['Aantal'] = big["Aantal"].astype(pd.Int64Dtype())

    # format the columns
    big = big[[
        "Datum",
        "Type",
        "Aantal"
    ]]

    Path(DATA_FOLDER, "data-nice").mkdir(exist_ok=True)

    # dates = sorted(big["Datum"].unique())

    # export by date
    # for data_date in dates:
       # export_date(big, "data-nice", "NICE_NL_IC", data_date, str(data_date).replace("-", ""))

    # export latest day
    # export_date(big, "data-nice", "NICE_NL_IC", data_date=dates[-1], label="latest")

    # export all (latest download)
    export_date(big, "data-nice", "NICE_IC_long", data_date=None, label="latest")

TYPES = [
    "IngezetteICs",
    "ToenameOpnamen",
    "TotaalOpnamen",
    "CumulatiefOpnamen",
    "CumulatiefOntslagZiekenhuis",
    "CumulatiefOntslagOverleden",
    "TotaalOntslagIC",
    "ToenameOntslagZiekenhuis",
    "ToenameOntslagOverleden",
]

def main_wide_nice():

    df_reported = pd.read_csv(Path("data", "nice_ic_by_day.csv"))
    df_reported['new'] = df_reported['newIntake'] + df_reported['newSuspected']
    df_reported.drop(['newIntake', 'newSuspected'], axis = 1, inplace = True)
    df_reported.rename(columns={
                       VARIABLES[0]: TYPES[0],
                       VARIABLES[1]: TYPES[1],
                       VARIABLES[2]: TYPES[2],
                       VARIABLES[3]: TYPES[3],
                       VARIABLES[4]: TYPES[4],
                       VARIABLES[5]: TYPES[5],
                       VARIABLES[6]: TYPES[6]}, inplace=True)

    df_reported["ToenameOntslagOverleden"] = df_reported["CumulatiefOntslagOverleden"]
    df_reported["ToenameOntslagOverleden"] = df_reported \
        ['CumulatiefOntslagOverleden'] \
        .transform(pd.Series.diff)
    df_reported['ToenameOntslagOverleden'] = df_reported["ToenameOntslagOverleden"].astype(pd.Int64Dtype())

    df_reported["ToenameOntslagZiekenhuis"] = df_reported["CumulatiefOntslagZiekenhuis"]
    df_reported["ToenameOntslagZiekenhuis"] = df_reported \
        ['CumulatiefOntslagZiekenhuis'] \
        .transform(pd.Series.diff)
    df_reported['ToenameOntslagZiekenhuis'] = df_reported["ToenameOntslagZiekenhuis"].astype(pd.Int64Dtype())


    # format the columns
    df_reported = df_reported[[
        "Datum",
        "IngezetteICs",
        "TotaalOpnamen",
        "ToenameOpnamen",
        "CumulatiefOpnamen",
        "ToenameOntslagZiekenhuis",
        "CumulatiefOntslagZiekenhuis",
        "ToenameOntslagOverleden",
        "CumulatiefOntslagOverleden",
        "TotaalOntslagIC"
    ]]

    Path(DATA_FOLDER, "data-nice").mkdir(exist_ok=True)

    # export all (latest download)
    export_date(df_reported, "data-nice", "NICE_IC_wide", data_date=None, label="latest")


if __name__ == '__main__':

    DATA_FOLDER.mkdir(exist_ok=True)

    main_long_nice()

    main_wide_nice()

 

