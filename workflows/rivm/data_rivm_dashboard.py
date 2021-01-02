from datetime import date
from pathlib import Path

import numpy as np
import pandas as pd

import requests


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


def _get_data(key, mapping, date_key):

    r = requests.get(URL)
    data = r.json()[key]["values"]
    df = pd.DataFrame(data)

    df["Datum"] = pd.to_datetime(df[date_key], unit='s').dt.date
    df.rename(mapping, axis=1, inplace=True)

    df_selection = ["Datum"] + list(mapping.values())

    df = df[df_selection] \
        .set_index("Datum") \
        .dropna(how="all") \
        .fillna(-1) \
        .stack() \
        .replace(-1, np.nan) \
        .to_frame() \
        .reset_index()

    df.columns = ["Datum", "Type", "Waarde"]

    return df


def main_rep():

    df = _get_data(
        "reproduction_index",
        {
            "reproduction_index_low": "Minimum",
            "reproduction_index_high": "Maximum",
            "reproduction_index_avg": "Reproductie index",
        },
        "date_of_report_unix"
    )

    Path(DATA_FOLDER, "data-reproduction").mkdir(exist_ok=True)

    export_date(
        df,
        "data-reproduction",
        "RIVM_NL_reproduction_index",
        data_date=None,
        label=None)


def main_infectious():

    df_normalized = _get_data(
        "infectious_people_count_normalized",
        {
            "infectious_low_normalized": "Minimum",
            "infectious_high_normalized": "Maximum",
            "infectious_avg_normalized": "Geschat aantal besmettelijke mensen",
        },
        "date_of_report_unix"
    )

    df = _get_data(
        "infectious_people_count",
        {
            "infectious_low": "Minimum",
            "infectious_high": "Maximum",
            "infectious_avg": "Geschat aantal besmettelijke mensen",
        },
        "date_of_report_unix"
    )
    df["Waarde"] = df["Waarde"].astype(pd.Int64Dtype())

    Path(DATA_FOLDER,
         "data-contagious/data-contagious_estimates").mkdir(exist_ok=True)

    export_date(
        df_normalized,
        "data-contagious",
        "RIVM_NL_contagious_estimate_normalized",
        data_date=None,
        label=None)

    export_date(
        df,
        "data-contagious",
        "RIVM_NL_contagious_estimate",
        data_date=None,
        label=None)


def main_nursery():


    df_pos = _get_data(
        "nursing_home",
        {
            "newly_infected_people": "Positief geteste bewoners",
        },
        "date_of_report_unix"
    )

    df_deceased = _get_data(
        "nursing_home",
        {
            "newly_infected_people": "Overleden besmette bewoners",
        },
        "date_of_report_unix"
    )

    df = df_pos.append(df_deceased) \
        .rename({"Waarde": "Aantal"}, axis=1) \
        .sort_values(by=['Datum', 'Type'], ascending=[True, False])

    df['AantalCumulatief'] = df.groupby('Type')['Aantal'].transform(
        pd.Series.cumsum)

    df['Aantal'] = df["Aantal"].astype(pd.Int64Dtype())
    df['AantalCumulatief'] = df["AantalCumulatief"].astype(pd.Int64Dtype())

    Path(DATA_FOLDER,
         "data-nursery/data-nursery_residents").mkdir(exist_ok=True)

    export_date(
        df,
        "data-nursery/data-nursery_residents",
        "RIVM_NL_nursery_residents",
        data_date=None,
        label=None)


def main_nurseryhomes():

    df_new = _get_data(
        "nursing_home",
        {
            "newly_infected_locations": "Besmette verpleeghuizen",
        },
        "date_of_report_unix"
    ).rename({"Waarde": "NieuwAantal"}, axis=1)

    df_total = _get_data(
        "nursing_home",
        {
            "infected_locations_total": "Besmette verpleeghuizen",
        },
        "date_of_report_unix"
    ).rename({"Waarde": "Aantal"}, axis=1)

    df = df_total.merge(df_new, on=["Datum", "Type"])

    Path(DATA_FOLDER, "data-nursery/data-nursery_homes").mkdir(exist_ok=True)

    export_date(
        df,
        "data-nursery/data-nursery_homes",
        "RIVM_NL_nursery_counts",
        data_date=None,
        label=None)


def main_national():

    df_total = _get_data(
        "infected_people_total",
        {
            "infected_daily_total": "Totaal",
        },
        "date_of_report_unix"
    ).rename({"Waarde": "Aantal"}, axis=1)
    df_total['AantalCumulatief'] = df_total['Aantal'].transform(pd.Series.cumsum)

    df_ma = _get_data(
        "intake_hospital_ma",
        {
            "moving_average_hospital": "Ziekenhuisopname",
        },
        "date_of_report_unix"
    ).rename({"Waarde": "Aantal"}, axis=1)
    df_ma['AantalCumulatief'] = df_ma['Aantal'].transform(pd.Series.cumsum)

    df = df_total.append(df_ma)

    df['Aantal'] = df["Aantal"].astype(pd.Int64Dtype())
    df['AantalCumulatief'] = df["AantalCumulatief"].astype(pd.Int64Dtype())

    df = df.sort_values(by=['Datum', 'Type'], ascending=[True, True])
    df = df.reset_index(drop=True)

    Path(DATA_FOLDER, "data-cases").mkdir(exist_ok=True)

    dates = sorted(df["Datum"].unique())

    for data_date in dates:

        export_date(df, "data-cases", "RIVM_NL_national_dashboard", data_date,
                    str(data_date).replace("-", ""))

    export_date(
        df,
        "data-cases",
        "RIVM_NL_national_dashboard",
        data_date=dates[-1],
        label="latest")

    export_date(
        df,
        "data-cases",
        "RIVM_NL_national_dashboard",
        data_date=None,
        label=None)


def main_suspects():

    df = _get_data(
        "verdenkingen_huisartsen",
        {
            "incidentie": "Verdachte patienten",
        },
        "week_unix"
    ).rename({"Waarde": "Aantal"}, axis=1)

    Path(DATA_FOLDER, "data-suspects").mkdir(exist_ok=True)

    export_date(
        df, "data-suspects", "RIVM_NL_suspects", data_date=None, label=None)


def main_riool():

    df_ml = _get_data(
        "sewer",
        {
            "average": "Virusdeeltjes per ml rioolwater",
        },
        "week_unix"
    ).rename({"Waarde": "Aantal"}, axis=1)

    df_installations = _get_data(
        "sewer",
        {
            "total_installation_count": "Installaties",
        },
        "week_unix"
    ).rename({"Waarde": "Installaties"}, axis=1).drop("Type", axis=1)

    df = df_ml.merge(df_installations, on=["Datum"])

    Path(DATA_FOLDER, "data-sewage").mkdir(exist_ok=True)

    export_date(
        df, "data-sewage", "RIVM_NL_sewage_counts", data_date=None, label=None)


def main_descriptive():

    r = requests.get(URL)
    data = r.json()["intake_share_age_groups"]["values"]
    df = pd.DataFrame(data)
    df["Datum"] = pd.to_datetime(df["date_of_report_unix"], unit='s').dt.date

    df.rename({
        "agegroup": "LeeftijdGroep",
        "infected_per_agegroup_increase": "Aantal"
    }, axis=1, inplace=True)

    df = df[["Datum", "LeeftijdGroep", "Aantal"]]

    data = pd.read_json(URL)

    df_total = pd.read_csv(
        Path("data-dashboard/data-descriptive",
             "RIVM_NL_age_distribution.csv"),
        parse_dates=["Datum"])
    df_total["Datum"] = df_total["Datum"].dt.date

    if df['Datum'][0] in list(df_total['Datum']):
        next
    else:
        df_total = df_total.append(df, ignore_index=True)
        df_total = df_total.sort_values(by=['Datum', 'LeeftijdGroep'])
        df_total = df_total.reset_index(drop=True)

    dates = sorted(df_total["Datum"].unique())

    Path(DATA_FOLDER, "data-descriptive").mkdir(exist_ok=True)

    for data_date in dates:
        export_date(df_total, "data-descriptive", "RIVM_NL_age_distribution",
                    data_date,
                    str(data_date).replace("-", ""))

    export_date(
        df_total,
        "data-descriptive",
        "RIVM_NL_age_distribution",
        data_date=None,
        label=None)

    export_date(
        df_total,
        "data-descriptive",
        "RIVM_NL_age_distribution",
        data_date=dates[-1],
        label="latest")


if __name__ == '__main__':
    DATA_FOLDER.mkdir(exist_ok=True)

    funs = [
        main_rep,
        main_infectious,
        main_nursery,
        main_nurseryhomes,
        # main_riool,
        # main_national,
        main_suspects,
        main_descriptive,
    ]

    for f in funs:
        try:
            f()
        except KeyError as err:
            print("key no longer available", err)
