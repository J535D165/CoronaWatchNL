import re
import datetime
from pathlib import Path

import pandas as pd

DATA_FOLDER = Path("data-misc/data-underlying")

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


def parse_onderliggende_a():

    df = pd.read_csv(Path("data-misc/data-underlying/data-underlying_statistics", "RIVM_NL_deceased_under70_statistics.csv"))

    Path(DATA_FOLDER, "data-underlying_statistics").mkdir(exist_ok=True)

    dates = sorted(df["Datum"].unique())

    # export by date
    for data_date in dates:

        export_date(df, "data-underlying_statistics", "RIVM_NL_deceased_under70_statistics", data_date, str(data_date).replace("-", ""))

    # export latest
    export_date(df, "data-underlying_statistics", "RIVM_NL_deceased_under70_statistics", data_date=dates[-1], label="latest")


    # export all
    export_date(df, "data-underlying_statistics", "RIVM_NL_deceased_under70_statistics", data_date=None, label=None)


def parse_onderliggende_b():

    df = pd.read_csv(Path("data-misc/data-underlying/data-underlying_conditions", "RIVM_NL_deceased_under70_conditions.csv"))

    Path(DATA_FOLDER, "data-underlying_conditions").mkdir(exist_ok=True)

    dates = sorted(df["Datum"].unique())

    # export by date
    for data_date in dates:

        export_date(df, "data-underlying_conditions", "RIVM_NL_deceased_under70_conditions", data_date, str(data_date).replace("-", ""))

    # export latest
    export_date(df, "data-underlying_conditions", "RIVM_NL_deceased_under70_conditions", data_date=dates[-1], label="latest")


    # export all
    export_date(df, "data-underlying_conditions", "RIVM_NL_deceased_under70_conditions", data_date=None, label=None)


if __name__ == '__main__':

    parse_onderliggende_a()

    parse_onderliggende_b()
