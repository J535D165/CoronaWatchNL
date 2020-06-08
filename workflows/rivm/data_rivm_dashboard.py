import pandas as pd
import urllib.request, json 
from datetime import date
from pathlib import Path
import itertools
import datetime
import numpy as np

#from utils import convert_to_int

DATA_FOLDER = Path("data-misc")

def get_timeline():

    df = pd.read_csv(Path("data-misc/data-reproduction", "RIVM_NL_reproduction_index.csv"))
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
    
    
def main_rep():    
    # Read json 
    with urllib.request.urlopen("https://coronadashboard.rijksoverheid.nl/json/NL.json") as url:
        data = json.loads(url.read().decode())
    
    data = data['reproduction_index']
    data_min = data['min']
    data_max = data['max']
    data_rep = data['list']

    
    dates = []
    for i in data_min:
        datum = f'{date.fromtimestamp(int(i))}'
        dates.append(datum)
        
    df = pd.DataFrame()
    df['Datum'] = dates
    
    # Select reproduction values per date
    rep = []
    for i in data_rep:
        aantal = data_rep[i]
        rep.append(aantal)
    
    df['Type'] = 'Reproductie index'
    df['Waarde'] = pd.Series(rep)
    
    # Select minimum values per date
    df2 = pd.DataFrame()
    mini = []
    for i in data_min:
        aantal = data_min[i]
        mini.append(aantal)
    df2['Datum'] = dates
    df2['Type'] ='Minimum'
    df2['Waarde'] = mini
    
    # Select maximum values per date
    df3 = pd.DataFrame()
    maxi = []
    for i in data_max:
        aantal = data_max[i]
        maxi.append(aantal)
    df3['Datum'] = dates
    df3['Type'] ='Maximum'
    df3['Waarde'] = maxi
    
    df = df.append(df2).append(df3)
    df = df.sort_values(by = ['Datum', 'Type'], ascending=[True, False])
    df = df.reset_index(drop = True)
        
    Path(DATA_FOLDER, "data-reproduction").mkdir(exist_ok=True)

    dates = sorted(df["Datum"].unique())

    # export by date
    # for data_date in dates:

        #export_date(df, "data-reproduction", "RIVM_NL_reproduction_index", data_date, str(data_date).replace("-", ""))

    # export latest
    # export_date(df, "data-reproduction", "RIVM_NL_reproduction_index", data_date=dates[-1], label="latest")

    # export all
    export_date(df, "data-reproduction", "RIVM_NL_reproduction_index", data_date=None, label=None)

def main_test():    
    # Read json 
    with urllib.request.urlopen("https://coronadashboard.rijksoverheid.nl/json/NL.json") as url:
        data = json.loads(url.read().decode())
        
    # Only save data related to infected people
    data = data['infected_people_total']
    data = data['list']
    
    # create dataframe
    dates = []
    values = []
    for i in data:
        datum = f'{date.fromtimestamp(int(i))}'
        dates.append(datum)
        aantal = data[i]
        values.append(aantal)
        
    df = pd.DataFrame()
    df['Datum'] = dates
    df['AantalCumulatief'] = values
    df["Aantal"] = df \
    ['AantalCumulatief'] \
    .transform(pd.Series.diff)
    
    df.loc[df["Datum"] == sorted(df["Datum"].unique())[0], "Aantal"] = \
    df.loc[df["Datum"] == sorted(df["Datum"].unique())[0], "AantalCumulatief"]

    
    df['Aantal'] = df["Aantal"].astype(pd.Int64Dtype())
    
    df = df[[
        "Datum",
        "Aantal",
        "AantalCumulatief"
    ]]
    
    return(df)

    # Path(DATA_FOLDER, "data-test").mkdir(exist_ok=True)

    # dates = sorted(df["Datum"].unique())

    # export by date
    # for data_date in dates:

        #export_date(df, "data-test", "RIVM_NL_tested", data_date, str(data_date).replace("-", ""))

    # export latest
    # export_date(df, "data-test", "RIVM_NL_tested", data_date=dates[-1], label="latest")

    # export all
    # export_date(df, "data-test", "RIVM_NL_tested", data_date=None, label=None)

def main_infectious():    
    # Read json 
    with urllib.request.urlopen("https://coronadashboard.rijksoverheid.nl/json/NL.json") as url:
        data = json.loads(url.read().decode())
        
    # Only save data related to infected people
    data = data['infectious_people_count_normalized']
    data_count = data['list']
    data_min = data['min']
    data_max = data['max']
    
    # create dataframe
    dates = []
    values = []
    for i in data_count:
        datum = f'{date.fromtimestamp(int(i))}'
        dates.append(datum)
        
        aantal = data_count[i]
        mini = data_min[i]
        maxi = data_max[i]
        
        values.append(aantal)
        values.append(mini)
        values.append(maxi)
        
    df = pd.DataFrame()
    df['Datum'] = dates*3
    df['Type'] = ['Geschat aantal besmettelijke mensen', 'Minimum aantal besmettelijke mensen', 'Maximum aantal besmettelijke mensen']
    df['Waarde'] = values
    
    df_total = pd.read_csv(Path("data-misc/data-contagious", "RIVM_NL_contagious_estimate.csv"))

    if df['Datum'].isin(dates).any():
        next
    else:
        df_total = df_total.append(df, ignore_index = True)
        
    Path(DATA_FOLDER, "data-contagious").mkdir(exist_ok=True)
    export_date(df_total, "data-contagious", "RIVM_NL_contagious_estimate", data_date=None, label=None)

    export_date(df, "data-contagious", "RIVM_NL_contagious_estimate", data_date=None, label="latest")


if __name__ == '__main__':

    DATA_FOLDER.mkdir(exist_ok=True)

    main_rep()
    
    main_test()
    
    main_infectious()
     
