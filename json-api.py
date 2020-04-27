from pathlib import Path
import json

import pandas as pd


DATA_FOLDER = Path("data-json")


FP_NATIONAL = Path("data-geo", "data-national", "RIVM_NL_national.csv")
FP_NATIONAL_LATEST = Path("data-geo", "data-national", "RIVM_NL_national_latest.csv")

FP_PROVINCE = Path("data-geo", "data-provincial", "RIVM_NL_provincial.csv")
FP_PROVINCE_LATEST = Path("data-geo", "data-provincial", "RIVM_NL_provincial_latest.csv")

FP_MUNICIPALITY = Path("data-geo", "data-municipal", "RIVM_NL_municipal.csv")
FP_MUNICIPALITY_LATEST = Path("data-geo", "data-municipal", "RIVM_NL_municipal_latest.csv")


def convert_csv_to_json_national(fn, export_fn):

    df = pd.read_csv(fn)

    df_wide = df \
        .pivot_table(
            index=['Datum'],
            columns='Type',
            values=['Aantal', 'AantalCumulatief']
        )
    df_wide.columns = ["{}{}".format(v.lower(), k) for k,v in df_wide]
    df_wide.reset_index(inplace=True)

    # convert types
    for col in [
        "totaalAantal",
        "ziekenhuisopnameAantal",
        "overledenAantal",
        "totaalAantalCumulatief",
        "ziekenhuisopnameAantalCumulatief",
        "overledenAantalCumulatief"
    ]:
        df_wide[col] = df_wide[col].astype(pd.Int64Dtype())

    json_str = df_wide.to_json(
        orient="table",
        indent=2,
        index=False
    )

    json_dict = json.loads(json_str)
    del json_dict["schema"]["pandas_version"]
    json_dict["apiVersion"] = "0.1"

    Path(DATA_FOLDER, "data-national").mkdir(exist_ok=True, parents=True)

    with open(Path(DATA_FOLDER, "data-national", export_fn), "w") as f:
        json.dump(json_dict, f, indent=2)


def convert_csv_to_json_province(fn, export_fn):

    df = pd.read_csv(fn)

    df_wide = df \
        .pivot_table(
            index=['Datum', "Provincienaam", "Provinciecode"],
            columns='Type',
            values=['Aantal', 'AantalCumulatief']
        )
    df_wide.columns = ["{}{}".format(v.lower(), k) for k,v in df_wide]
    df_wide.reset_index(inplace=True)

    # convert types
    for col in [
        "Provinciecode",
        "totaalAantal",
        "ziekenhuisopnameAantal",
        "overledenAantal",
        "totaalAantalCumulatief",
        "ziekenhuisopnameAantalCumulatief",
        "overledenAantalCumulatief"
    ]:
        df_wide[col] = df_wide[col].astype(pd.Int64Dtype())

    json_str = df_wide.to_json(
        orient="table",
        indent=2,
        index=False
    )

    json_dict = json.loads(json_str)
    del json_dict["schema"]["pandas_version"]
    json_dict["apiVersion"] = "0.1"

    Path(DATA_FOLDER, "data-provincial").mkdir(exist_ok=True, parents=True)

    with open(Path(DATA_FOLDER, "data-provincial", export_fn), "w") as f:
        json.dump(json_dict, f, indent=2)



def convert_csv_to_json_municipality(fn, export_fn):

    df = pd.read_csv(fn)

    df_wide = df \
        .pivot_table(
            index=['Datum', "Provincienaam", "Provinciecode", "Gemeentenaam", "Gemeentecode"],
            columns='Type',
            values=['Aantal', 'AantalCumulatief']
        )
    df_wide.columns = ["{}{}".format(v.lower(), k) for k,v in df_wide]
    df_wide.reset_index(inplace=True)

    # convert types
    for col in [
        "Provinciecode",
        "Gemeentecode",
        "totaalAantal",
        "ziekenhuisopnameAantal",
        "overledenAantal",
        "totaalAantalCumulatief",
        "ziekenhuisopnameAantalCumulatief",
        "overledenAantalCumulatief"
    ]:
        df_wide[col] = df_wide[col].astype(pd.Int64Dtype())

    json_str = df_wide.to_json(
        orient="table",
        indent=2,
        index=False
    )

    json_dict = json.loads(json_str)
    del json_dict["schema"]["pandas_version"]
    json_dict["apiVersion"] = "0.1"

    Path(DATA_FOLDER, "data-municipal").mkdir(exist_ok=True, parents=True)

    with open(Path(DATA_FOLDER, "data-municipal", export_fn), "w") as f:
        json.dump(json_dict, f, indent=2)


if __name__ == '__main__':

    # export data (national)
    convert_csv_to_json_national(FP_NATIONAL, "RIVM_NL_national.json")
    convert_csv_to_json_national(FP_NATIONAL_LATEST, "RIVM_NL_national_latest.json")

    # export data (province)
    convert_csv_to_json_province(FP_PROVINCE, "RIVM_NL_provincial.json")
    convert_csv_to_json_province(FP_PROVINCE_LATEST, "RIVM_NL_provincial_latest.json")

    # export data (municipality)
    convert_csv_to_json_municipality(FP_MUNICIPALITY, "RIVM_NL_municipal.json")
    convert_csv_to_json_municipality(FP_MUNICIPALITY_LATEST, "RIVM_NL_municipal_latest.json")
