import re
from pathlib import Path
import requests
import datetime
import json
import pandas as pd

URL_NICE_BASE = "https://www.stichting-nice.nl"
URL_NICE_API_JSON = "https://www.stichting-nice.nl/js/covid-19.js"

RAW_DATA_FOLDER = Path("raw_data", "nice")

regex = r"\'\/covid-19\/public\/([0-9A-Za-z\-]+)[\/']"


def download_extract_api_calls():
    """Get the API URLS"""
    r = requests.get(URL_NICE_API_JSON)

    matches = re.finditer(regex, r.text, re.MULTILINE)

    result = {}

    for _, match in enumerate(matches, start=1):

        result[match.group(1)] = URL_NICE_BASE + "/covid-19/public/" + match.group(1)

    return result


def merge_data():
    """Get the API URLS"""
    df = pd.read_json(Path(RAW_DATA_FOLDER, "intake-count-2020-04-18.json"))
    df = pd.read_json(Path(RAW_DATA_FOLDER, "intake-cumulative-2020-04-18.json"))
    df = pd.read_json(Path(RAW_DATA_FOLDER, "ic-count-2020-04-18.json"))
    df = pd.read_json(Path(RAW_DATA_FOLDER, "died-cumulative-2020-04-18.json"))
    df = pd.read_json(Path(RAW_DATA_FOLDER, "died-and-survivors-cumulative-2020-04-18.json"))
    print(df)


# def export_data():

#     files = Path("raw_data", "nice").glob("intake-count-*.json")
#     files = sorted([str(file) for file in files])

#     for file in files[:1]:
#         date_str = re.search(r"(\d{4}-\d{2}-\d{2})", str(file)).group(1)



#         # check if file is latest
#         if files[-1] == str(file):
#             df.to_csv(
#                 Path("data", "nice", "rivm_NL_covid19_national_by_date_latest.csv".format(date_str)),
#                 index=False
#             )

#         # df.to_csv(
#         #     Path("data", "rivm_NL_covid19_national_by_date", "rivm_NL_covid19_national_by_date_{}.csv".format(date_str)),
#         #     index=False
#         # )


def open_multi_dim_table(fp):

    with open(fp, "r") as f:
        content = json.load(f)

    n_dims = len(content)

    return tuple(pd.DataFrame(file) for file in content)


if __name__ == '__main__':

    # api_urls = download_extract_api_calls()

    # RAW_DATA_FOLDER.mkdir(parents=True, exist_ok=True)

    # for key, value in api_urls.items():
    #     r = requests.get(value)

    #     fp = RAW_DATA_FOLDER / f"{key}-{datetime.date.today()}.json"
    #     with open(fp, "w") as f:
    #         f.write(r.text)

    df_ic_count = pd.read_json(Path(RAW_DATA_FOLDER, "ic-count-2020-04-18.json", convert_dates=False)) \
        .rename({"date": "Datum", "value": "icCount"}, axis=1) \
        # .set_index("Datum")

    print(df_ic_count.dtypes)

    df_intake_count = pd.read_json(Path(RAW_DATA_FOLDER, "intake-count-2020-04-18.json", convert_dates=False)) \
        .rename({"date": "Datum", "value": "intakeCount"}, axis=1) \
        .set_index("Datum")

    print(df_intake_count.dtypes)

    df_new_intake_count, df_new_intake_susp = open_multi_dim_table(
        Path(RAW_DATA_FOLDER, "new-intake-2020-04-18.json")
    )
    df_new_intake_count = df_new_intake_count\
        .rename({"date": "Datum", "value": "intakeCumulative"}, axis=1) \
        .set_index("Datum")

    df_died, df2, df_survived = open_multi_dim_table(
        Path(RAW_DATA_FOLDER, "died-and-survivors-cumulative-2020-04-18.json")
    )
    df_died = df_died \
        .rename({"date": "Datum", "value": "diedCumulative"}, axis=1) \
        .set_index("Datum")

    df_survived = df_survived \
        .rename({"date": "Datum", "value": "survivedCumulative"}, axis=1) \
        .set_index("Datum")

    print(df_intake_count)


    print(pd.concat([df_died, df_survived, df_new_intake_count, df_intake_count, df_ic_count], axis=1))
