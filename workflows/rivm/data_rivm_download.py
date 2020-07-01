
"""Download RIVM daily stats"""

from pathlib import Path
import pandas as pd
import datetime

# global variables
URL = "https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_cumulatief.json"
DATE = datetime.date.today()


def verify_dataset():
    pass


def download_rivm_data():
    verify_dataset()
        
    print("Connecting...")    
    data = pd.read_json(URL)
    
    TIME = datetime.datetime.combine(DATE, datetime.time(10, 0))

    if f'{TIME}'in list(data["Date_of_report"]):
        df = data[data["Date_of_report"] == f'{TIME}'].sum()
        
        df = pd.DataFrame({'Datum':  [f'{DATE}']*3,
        'Type': ['Totaal', 'Ziekenhuisopname', 'Overleden'],
        'Aantal': [df['Total_reported'], df['Hospital_admission'], df['Deceased']],
        })
        
        df_reported = pd.read_csv(Path("data", "rivm_NL_covid19_national.csv"))
        df_reported['Aantal'] = df_reported["Aantal"].astype(pd.Int64Dtype())
    
        if f'{DATE}' not in str(df_reported['Datum']):
            df_reported = df_reported.append(df, ignore_index = True)
            df_reported = df_reported.reset_index(drop=True)
    
            export_path = Path("data", "rivm_NL_covid19_national.csv")
            print(f"Export {export_path}")
            df_reported.to_csv(export_path, index=False)
        else: 
            print('RIVM file is already up to date')
    else:
        print(f"Data for {DATE} not (yet) available")
   
    
if __name__ == '__main__':

    download_rivm_data()
