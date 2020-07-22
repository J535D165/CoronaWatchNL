import pandas as pd
from datetime import date
from pathlib import Path

DATA_FOLDER = Path("data-dashboard")
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

    df_total = pd.read_csv(Path("data-dashboard/data-contagious/data-contagious_estimates", "RIVM_NL_contagious_estimate.csv"))

    if df['Datum'][0] in list(df_total['Datum']):
        next
    else:
        df_total = df_total.append(df, ignore_index=True)
        df_total = df_total.sort_values(by=['Datum', 'Type'])
        df_total = df_total.reset_index(drop=True)

    Path(DATA_FOLDER, "data-contagious/data-contagious_estimates").mkdir(exist_ok=True)

    dates = sorted(df_total["Datum"].unique())

    for data_date in dates:

        export_date(df_total, "data-contagious/data-contagious_estimates", "RIVM_NL_contagious_estimate", data_date, str(data_date).replace("-", ""))

    export_date(df_total, "data-contagious/data-contagious_estimates", "RIVM_NL_contagious_estimate", data_date=None, label=None)

    export_date(df_total, "data-contagious/data-contagious_estimates", "RIVM_NL_contagious_estimate", data_date=dates[-1], label="latest")

def main_infectcounts():
    data = pd.read_json(URL)

    selection = data['infectious_people_count']['list']
    type = ['Geschat aantal besmettelijke mensen'] * len(selection)

    df = pd.DataFrame(selection.keys(), columns=['Datum'])
    df['Type'] = type
    df['Aantal'] = selection.values()
    df['Aantal'] = df["Aantal"].astype(pd.Int64Dtype())

    for i in range(len(df)):
        df.iloc[i, 0] = f'{date.fromtimestamp(int(df.iloc[i, 0]))}'

    df_total = pd.read_csv(Path("data-dashboard/data-contagious/data-contagious_count", "RIVM_NL_contagious_count.csv"))
    if df['Datum'][0] in list(df_total['Datum']):
        next
    else:
        df_total = df_total.append(df, ignore_index=True)
        df_total = df_total.sort_values(by=['Datum', 'Type'])
        df_total = df_total.reset_index(drop=True)

    Path(DATA_FOLDER, "data-contagious/data-contagious_count").mkdir(exist_ok=True)

    dates = sorted(df_total["Datum"].unique())

    for data_date in dates:

        export_date(df_total, "data-contagious/data-contagious_count", "RIVM_NL_contagious_count", data_date, str(data_date).replace("-", ""))

    export_date(df_total, "data-contagious/data-contagious_count", "RIVM_NL_contagious_count", data_date=None, label=None)

    export_date(df_total, "data-contagious/data-contagious_count", "RIVM_NL_contagious_count", data_date=dates[-1], label="latest")

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

    df['Aantal'] = df["Aantal"].astype(pd.Int64Dtype())
    df['AantalCumulatief'] = df["AantalCumulatief"].astype(pd.Int64Dtype())

    Path(DATA_FOLDER, "data-nursery/data-nursery_residents").mkdir(exist_ok=True)

    export_date(df, "data-nursery/data-nursery_residents", "RIVM_NL_nursery_residents", data_date=None, label=None)

def main_nurseryhomes():
    data = pd.read_json(URL)

    selection = data['total_newly_reported_locations']['list']
    selection2 = data['total_reported_locations']['list']
    type = ['Besmette verpleeghuizen'] * len(selection)

    df = pd.DataFrame(selection.keys(), columns=['Datum'])
    df['Type'] = type

    df['NieuwAantal'] = selection.values()
    df['Aantal'] = selection2.values()

    for i in range(len(df)):
        df.iloc[i, 0] = f'{date.fromtimestamp(int(df.iloc[i, 0]))}'

    df['Aantal'] = df["Aantal"].astype(pd.Int64Dtype())
    df['NieuwAantal'] = df["NieuwAantal"].astype(pd.Int64Dtype())

    Path(DATA_FOLDER, "data-nursery/data-nursery_homes").mkdir(exist_ok=True)

    export_date(df, "data-nursery/data-nursery_homes", "RIVM_NL_nursery_counts", data_date=None, label=None)

def main_national():
    data = pd.read_json(URL)

    selection = data['infected_people_total']['list']
    type = ['Totaal'] * len(selection)

    df = pd.DataFrame(selection.keys(), columns=['Datum'])
    df['Type'] = type
    df['Aantal'] = selection.values()
    df['AantalCumulatief'] = df['Aantal'].transform(pd.Series.cumsum)
    df.iloc[0,2] = 191

    selection2 = data['intake_hospital_ma']['list']
    type = ['Ziekenhuisopname'] * len(selection2)

    df2 = pd.DataFrame(selection2.keys(), columns=['Datum'])
    df2['Type'] = type
    df2['Aantal'] = selection2.values()

    value = [43, 109, 94]
    for i in range(0,3):
        df2.iloc[i,2] = value[i]

    for i in range(3,len(df2)):
        df2.iloc[i,2] = round((df2.iloc[i,2] * 3) - df2.iloc[i-1,2] - df2.iloc[i-2,2])

    df2['AantalCumulatief'] = 205
    df2.iloc[1:, 3] = (df2.iloc[1:, 2].transform(pd.Series.cumsum)) + 205

    df = df.append(df2)
    df = df.sort_values(by=['Datum', 'Type'], ascending=[True, True])
    df = df.reset_index(drop = True)

    for i in range(len(df)):
        df.iloc[i, 0] = f'{date.fromtimestamp(int(df.iloc[i, 0]))}'

    df['Aantal'] = df["Aantal"].astype(pd.Int64Dtype())
    df['AantalCumulatief'] = df["AantalCumulatief"].astype(pd.Int64Dtype())

    Path(DATA_FOLDER, "data-cases").mkdir(exist_ok=True)

    dates = sorted(df["Datum"].unique())

    for data_date in dates:

        export_date(df, "data-cases", "RIVM_NL_national_dashboard", data_date, str(data_date).replace("-", ""))

    export_date(df, "data-cases", "RIVM_NL_national_dashboard", data_date=dates[-1], label="latest")

    export_date(df, "data-cases", "RIVM_NL_national_dashboard", data_date=None, label=None)

def main_suspects():
    data = pd.read_json(URL)

    selection = data['verdenkingen_huisartsen']['list']
    type = ['Verdachte patienten'] * len(selection)

    df = pd.DataFrame(selection.keys(), columns=['Datum'])
    df['Type'] = type
    df['Aantal'] = selection.values()

    for i in range(len(df)):
        df.iloc[i, 0] = f'{date.fromtimestamp(int(df.iloc[i, 0]))}'

    Path(DATA_FOLDER, "data-suspects").mkdir(exist_ok=True)

    export_date(df, "data-suspects", "RIVM_NL_suspects", data_date=None, label=None)

def main_riool():
    data = pd.read_json(URL)
    selection = data['rioolwater_metingen']['list']

    df = pd.DataFrame(selection.keys(), columns=['Datum'])
    df['Type'] = "Virusdeeltjes per ml rioolwater"
    df['Aantal'] = selection.values()

    for i in range(len(df)):
        df.iloc[i, 0] = f'{date.fromtimestamp(int(df.iloc[i, 0]))}'

    df = df.sort_values(by=['Datum', 'Type'], ascending=[True, False])
    df = df.reset_index(drop = True)

    Path(DATA_FOLDER, "data-sewage").mkdir(exist_ok=True)

    export_date(df, "data-sewage", "RIVM_NL_sewage_counts", data_date=None, label=None)

def main_descriptive():
    data = pd.read_json(URL)

    selection = data['intake_share_age_groups']['list']
    datum = data['intake_share_age_groups']['lastupdate']
    datum = [f'{date.fromtimestamp(datum)}'] * len(selection)

    df = pd.DataFrame()
    df['Datum'] = datum
    df['LeeftijdGroep'] = selection.keys()
    df['Aantal'] = selection.values()
    df['Aantal'] = df["Aantal"].astype(pd.Int64Dtype())

    df_total = pd.read_csv(Path("data-dashboard/data-descriptive", "RIVM_NL_age_distribution.csv"))

    if df['Datum'][0] in list(df_total['Datum']):
        next
    else:
        df_total = df_total.append(df, ignore_index=True)
        df_total = df_total.sort_values(by=['Datum', 'LeeftijdGroep'])
        df_total = df_total.reset_index(drop=True)

    dates = sorted(df_total["Datum"].unique())

    Path(DATA_FOLDER, "data-descriptive").mkdir(exist_ok=True)

    for data_date in dates:
        export_date(df_total, "data-descriptive", "RIVM_NL_age_distribution", data_date, str(data_date).replace("-", ""))

    export_date(df_total, "data-descriptive", "RIVM_NL_age_distribution", data_date=None, label=None)

    export_date(df_total, "data-descriptive", "RIVM_NL_age_distribution", data_date=dates[-1], label="latest")

if __name__ == '__main__':
    DATA_FOLDER.mkdir(exist_ok=True)

    main_rep()

    main_infectious()

    main_infectcounts()

    main_nursery()

    main_nurseryhomes()

    main_riool()

    main_national()

    main_suspects()

    main_descriptive()
