
"""Download RIVM daily stats"""

from pathlib import Path
import re

import requests
from lxml import html
import lxml.html
import pandas as pd
from datetime import datetime

# global variables
RIVM_DATA_BASE_CORONA_URL = "https://www.rivm.nl/coronavirus-covid-19/actueel"


def verify_dataset():
    pass


def download_rivm_data():

    verify_dataset()

    # download data
    doc = requests.get(RIVM_DATA_BASE_CORONA_URL)
    root = lxml.html.fromstring(doc.content)
    
    # obtain date
    DATE = str(re.search(r'Actuele cijfers COVID-19: (\d+) [a-zA-Z]+ (\d+)', doc.content.decode()))
    DATE = DATE.split(": ")[1]
    DATE = DATE.split("'>")[0]
    
    Maand = {'januari':1, 'februari':2, 'maart':3, 'april':4, 'mei':5, 'juni':6, 'juli':7, 'augustus':8, 'september':9, 'oktober':10, 'november':11, 'december':12} 
    maand = ''.join(re.findall('[a-zA-Z]+', DATE))

    DATE = DATE.replace(maand, str(Maand[maand]))
    DATE = datetime.strptime(DATE, '%d %m %Y')
    DATE = DATE.strftime("%Y-%m-%d")
    
    # obtain table data
    root.xpath('//tr/td//text()')
    for tbl in root.xpath('//table'):
        elements = tbl.xpath('.//tr/td//text()')
    data = str(elements)
    data = re.findall('(\d+\.\d{1,3})', data)
    
    # create new dataframe
    types = ['Totaal', 'Ziekenhuisopname', 'Overleden']
    df = pd.DataFrame()
    for i in range(3):
        aantal = data[i].replace(".", "")
        new = {'Datum': DATE, 'Type': types[i], 'Aantal': aantal}
        df = df.append(new, ignore_index = True)

    df = df[[
        "Datum",
        "Type",
        "Aantal"
    ]]
    
    # Add new data to datafile data-folder
    df_reported = pd.read_csv(Path("data", "rivm_NL_covid19_national.csv"))
    df_reported['Aantal'] = df_reported["Aantal"].astype(pd.Int64Dtype())

    
    if DATE not in str(df_reported['Datum']):
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
