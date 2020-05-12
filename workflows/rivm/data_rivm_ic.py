from pathlib import Path
import itertools

import pandas as pd
import numpy as np

from utils import convert_to_int

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
    "newIntake",
    "intakeCount",
    "intakeCumulative",
    "survivedCumulative",
    "diedCumulative"
]

def main_nice():

    df_reported = pd.read_csv(Path("data", "nice_ic_by_day.csv"))
    df_reported['Type'] = 'NA'
    
    new = pd.DataFrame([])
    big = pd.DataFrame([])
    for i in VARIABLES:
        new = df_reported[['Datum', i, 'Type']]
        new = new.rename(columns={i: "Aantal"})
        new['Type'] = i
        big = big.append(new, ignore_index = True)
        
    big = big.sort_values('Datum', ascending=True)    

    big['Aantal'] = big["Aantal"].astype(pd.Int64Dtype())

    # format the columns
    big = big[[
        "Datum",
        "Type",
        "Aantal"
    ]]

    Path(DATA_FOLDER, "data-nice").mkdir(exist_ok=True)

    dates = sorted(big["Datum"].unique())

    # export by date
    for data_date in dates:
        export_date(big, "data-nice", "NICE_NL_IC", data_date, str(data_date).replace("-", ""))

    # export latest
    export_date(big, "data-nice", "NICE_NL_IC", data_date=dates[-1], label="latest")

    # export all
    export_date(big, "data-nice", "NICE_NL_IC", data_date=None, label=None)

# LCPS data
def main_lcps():

    df_reported = pd.read_csv(Path("data", "lcps_ic_country.csv"))    
    df_reported['Aantal'] = df_reported["Aantal"].astype(pd.Int64Dtype())

    dates = sorted(df_reported["Datum"].unique())

    for i in dates:
        data = {'Datum':  [i],
        'Land': ['Totaal'], 'Aantal':['NA']}
        new = pd.DataFrame(data, columns = ['Datum','Land','Aantal'])
        new['Aantal'] = sum(df_reported.loc[df_reported['Datum'] == i, 'Aantal'])
        df_reported = df_reported.append(new, ignore_index = True)

    df_reported = df_reported.sort_values('Datum', ascending=True)    
    df_reported['Aantal'] = df_reported["Aantal"].astype(pd.Int64Dtype())

    # format the columns
    df_reported = df_reported[[
        "Datum",
        "Land",
        "Aantal"
    ]]

    Path(DATA_FOLDER, "data-lcps").mkdir(exist_ok=True)

    # export by date
    for data_date in dates:
        export_date(df_reported, "data-lcps", "LCPS_NL_IC", data_date, str(data_date).replace("-", ""))

    # export latest
    export_date(df_reported, "data-lcps", "LCPS_NL_IC", data_date=dates[-1], label="latest")

    # export all
    export_date(df_reported, "data-lcps", "LCPS_NL_IC", data_date=None, label=None)
        
    
if __name__ == '__main__':

    DATA_FOLDER.mkdir(exist_ok=True)

    main_nice()
     
    main_lcps()


