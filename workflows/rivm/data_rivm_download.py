
"""Download RIVM daily stats"""

import pandas as pd
import urllib.request, json 
from datetime import date
from pathlib import Path
import itertools
import datetime
import numpy as np

# global variables
RIVM_DATA_BASE_CORONA_URL = "https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_cumulatief.json"
DATE = datetime.date.today()

def verify_dataset():
    pass


def download_rivm_data():

    verify_dataset()

    with urllib.request.urlopen(RIVM_DATA_BASE_CORONA_URL) as url:
        data = json.loads(url.read().decode())
        
    # Sum all municipalities to get total sum
    total = 0
    hospital = 0
    over = 0
    print("Loading data...")
    for i in range(len(data)):
        if f'{DATE}' in data[i]['Date_of_report']:
            total = total + data[i]['Total_reported']
            hospital = hospital + data[i]['Hospital_admission']
            over = over + data[i]['Deceased']

    
    # Create new dataframe
    mydata = {'Datum':  [f'{DATE}', f'{DATE}', f'{DATE}'],
        'Type': ['Totaal', 'Ziekenhuisopname', 'Overleden'],
        'Aantal': [total, hospital, over],
        }
    df = pd.DataFrame(mydata)
    
    # Add new data to datafile data-folder
    df_reported = pd.read_csv(Path("data", "rivm_NL_covid19_national.csv"))
    df_reported['Aantal'] = df_reported["Aantal"].astype(pd.Int64Dtype())

    
    if f'{DATE}' not in str(df_reported['Datum']):
        df_reported = df_reported.append(df, ignore_index = True)
        df_reported = df_reported.reset_index(drop=True)

        export_path = Path("data", "rivm_NL_covid19_national.csv")
        print("Downloading...")
        print(f"Export {export_path}")
        df_reported.to_csv(export_path, index=False)
    else: 
        print('RIVM file is already up to date')
    
   
if __name__ == '__main__':

    download_rivm_data()
