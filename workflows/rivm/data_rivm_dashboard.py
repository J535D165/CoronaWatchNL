import pandas as pd
import urllib.request, json 
from datetime import date
from pathlib import Path
import itertools
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
        
    # Only save data related to reproduction index
    data = data['reproduction_index']
    
    # Select dates
    data_min = data['min']
    
    dates = []
    for i in data_min:
        datum = f'{date.fromtimestamp(int(i))}'
        dates.append(datum)
        
    df = pd.DataFrame()
    df['Datum'] = dates
    
    # Select reproduction values per date
    data_rep = data['list']
    
    rep = []
    for i in data_rep:
        aantal = data_rep[i]
        rep.append(aantal)
    
    df['ReproductieGetal'] = pd.Series(rep)
    
    # Select minimum values per date
    mini = []
    for i in data_min:
        aantal = data_min[i]
        mini.append(aantal)
    
    df['Minimum'] = mini
    
    # Select maximum values per date
    data_max = data['max']
    
    maxi = []
    for i in data_max:
        aantal = data_max[i]
        maxi.append(aantal)
        
    df['Maximum'] = maxi
    
    Path(DATA_FOLDER, "data-reproduction").mkdir(exist_ok=True)

    dates = sorted(df["Datum"].unique())

    # export by date
    for data_date in dates:

        export_date(df, "data-reproduction", "RIVM_NL_reproduction_index", data_date, str(data_date).replace("-", ""))

    # export latest
    export_date(df, "data-reproduction", "RIVM_NL_reproduction_index", data_date=dates[-1], label="latest")

    # export all
    export_date(df, "data-reproduction", "RIVM_NL_reproduction_index", data_date=None, label=None)


if __name__ == '__main__':

    DATA_FOLDER.mkdir(exist_ok=True)

    main_rep()
     
