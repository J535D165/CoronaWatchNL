import re
from pathlib import Path
from datetime import date

import pandas as pd

START_DATE = date(2020, 2, 27)

DATA_FP = {
    "Totaal": Path("raw_data", "website_charts", "bij-de-ggd-gemelde-patiënten-{date}.csv"),
    "Ziekenhuisopname": Path("raw_data", "website_charts", "in-ziekenhuis-opgenomen-patiënten-{date}.csv"),
    "Overleden": Path("raw_data", "website_charts", "overledenen-per-dag-{date}.csv")
}


def merge_data(date, type_data):

    data_totaal_fp = str(DATA_FP[type_data]).format(date=date)
    if type_data == "Totaal" and date > "2020-10-20":
        data_totaal_fp = Path("raw_data", "website_charts", "ggd-meldingen-positief-geteste-personen-per-dag-{date}.csv".format(date=date))

    df_totaal = pd.read_csv(data_totaal_fp, sep=";")

    if df_totaal.iloc[0, 0] not in ["2020-02-27", "27-feb", "27 feb"]:
        raise ValueError("Start date not feb 27, {}".format(df_totaal.iloc[0, 0]))

    df_totaal["Datum"] = pd.date_range(START_DATE, periods=len(df_totaal))
    df_totaal["Type"] = type_data

    try:
        df_totaal["Aantal"] = df_totaal["nieuw"] + df_totaal["tot en met gisteren"]
    except Exception:
        df_totaal["Aantal"] = df_totaal["nieuw"] + df_totaal["t/m afgelopen week"]

    return df_totaal[["Datum", "Type", "Aantal"]]


if __name__ == '__main__':

    files = Path("raw_data", "website_charts").glob("overledenen-per-dag-*.csv")
    files = sorted([str(file) for file in files])

    for file in files:
        print(file)

        date_str = re.search(r"(\d{4}-\d{2}-\d{2})", str(file)).group(1)

        df_totaal = merge_data(date_str, "Totaal")
        df_ziekenhuis = merge_data(date_str, "Ziekenhuisopname")
        df_overleden = merge_data(date_str, "Overleden")

        # merge and sort data
        df = pd.concat([df_totaal, df_ziekenhuis, df_overleden], axis=0)
        df["Type_index"] = df["Type"].replace({"Totaal": 1, "Ziekenhuisopname": 2, "Overleden": 3})
        df.sort_values(["Datum", "Type_index"], inplace=True)
        del df["Type_index"]

        # check if file is latest
        if files[-1] == str(file):
            df.to_csv(
                Path("data", "rivm_NL_covid19_national_by_date", "rivm_NL_covid19_national_by_date_latest.csv".format(date_str)),
                index=False
            )

        df.to_csv(
            Path("data", "rivm_NL_covid19_national_by_date", "rivm_NL_covid19_national_by_date_{}.csv".format(date_str)),
            index=False
        )
