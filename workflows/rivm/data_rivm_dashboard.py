import pandas as pd
from datetime import date
from pathlib import Path

DATA_FOLDER = Path("data-misc")
URL = "https://coronadashboard.rijksoverheid.nl/json/NL.json"

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
    data = pd.read_json(URL)

    df = pd.DataFrame()
    meas = ['list', 'min', 'max']
    types = ['Reproductie index', 'Minimum', 'Maximum']

    for i in range(len(meas)):
        selection = data['reproduction_index'][meas[i]]
        type = [types[i]] * len(selection)

        df2 = pd.DataFrame(selection.keys(), columns = ['Datum'])
        df2['Type'] = type
        df2['Waarde'] = [round(elem, 2) for elem in selection.values()]

        df = df.append(df2, ignore_index = True)

    for i in range(len(df)):
        df.iloc[i,0] = f'{date.fromtimestamp(int(df.iloc[i,0]))}'

    dates = list(df['Datum'][df['Type'] == 'Reproductie index'])
    for i in set(df['Datum']):
        if i not in dates:
            df = df.append({'Datum':i, 'Type':'Reproductie index', 'Waarde':''}, ignore_index = True)

    df = df.sort_values(by=['Datum', 'Type'], ascending=[True, False])
    df = df.reset_index(drop = True)

    Path(DATA_FOLDER, "data-reproduction").mkdir(exist_ok=True)

    export_date(df, "data-reproduction", "RIVM_NL_reproduction_index", data_date=None, label=None)

def main_infectious():
    data = pd.read_json(URL)

    df = pd.DataFrame()
    meas = ['list', 'min', 'max']
    types = ['Geschat aantal besmettelijke mensen', 'Minimum aantal besmettelijke mensen', 'Maximum aantal besmettelijke mensen']

    for i in range(len(meas)):
        selection = data['infectious_people_count_normalized'][meas[i]]
        type = [types[i]] * len(selection)

        df2 = pd.DataFrame(selection.keys(), columns = ['Datum'])
        df2['Type'] = type
        df2['Waarde'] = selection.values()

        df = df.append(df2, ignore_index = True)

    for i in range(len(df)):
        df.iloc[i,0] = f'{date.fromtimestamp(int(df.iloc[i,0]))}'

    df = df.sort_values(by=['Datum', 'Type'])
    df = df.reset_index(drop = True)

    df_total = pd.read_csv(Path("data-misc/data-contagious", "RIVM_NL_contagious_estimate.csv"))

    if df['Datum'][0] in list(df_total['Datum']):
        next
    else:
        df_total = df_total.append(df, ignore_index=True)
        df_total = df_total.sort_values(by=['Datum', 'Type'])
        df_total = df_total.reset_index(drop=True)

    Path(DATA_FOLDER, "data-contagious").mkdir(exist_ok=True)

    export_date(df_total, "data-contagious", "RIVM_NL_contagious_estimate", data_date=None, label=None)

    export_date(df, "data-contagious", "RIVM_NL_contagious_estimate", data_date=None, label="latest")

def main_nursery():
    data = pd.read_json(URL)

    df = pd.DataFrame()
    meas = ['infected_people_nursery_count_daily', 'deceased_people_nursery_count_daily']
    types = ['Positief geteste bewoners', 'Overleden besmette bewoners']

    for i in range(len(meas)):
        selection = data[meas[i]]['list']
        type = [types[i]] * len(selection)

        df2 = pd.DataFrame(selection.keys(), columns=['Datum'])
        df2['Type'] = type
        df2['Aantal'] = selection.values()

        df = df.append(df2, ignore_index=True)

    for i in range(len(df)):
        df.iloc[i, 0] = f'{date.fromtimestamp(int(df.iloc[i, 0]))}'

    df = df.sort_values(by=['Datum', 'Type'], ascending=[True, False])
    df = df.reset_index(drop = True)
    df['AantalCumulatief'] = df.groupby('Type')['Aantal'].transform(pd.Series.cumsum)

    Path(DATA_FOLDER, "data-nursery").mkdir(exist_ok=True)

    export_date(df, "data-nursery", "RIVM_NL_nursery_counts", data_date=None, label=None)

if __name__ == '__main__':
    DATA_FOLDER.mkdir(exist_ok=True)

    main_rep()

    main_infectious()

    main_nursery()

