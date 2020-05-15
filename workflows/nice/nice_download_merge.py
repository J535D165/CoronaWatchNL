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


def collect_api_calls():
    """Get the API URLS"""

    r = requests.get(URL_NICE_API_JSON)

    matches = re.finditer(regex, r.text, re.MULTILINE)

    result = {}

    for _, match in enumerate(matches, start=1):

        print("Found API entry point at: {}".format(match.group(1)))

        result[match.group(1)] = URL_NICE_BASE + "/covid-19/public/" + match.group(1)

    return result


def download_api_nice(url, name):
    """Download NICE data"""

    RAW_DATA_FOLDER.mkdir(parents=True, exist_ok=True)

    r = requests.get(url)

    fp = RAW_DATA_FOLDER / f"{name}-{datetime.date.today()}.json"
    with open(fp, "w") as f:
        f.write(r.text)


def open_multi_dim_table(fp):

    with open(fp, "r") as f:
        content = json.load(f)

    return tuple(pd.read_json(json.dumps(file)) for file in content)


if __name__ == '__main__':

    # get API entry points
    api_urls = collect_api_calls()

    # download data
    for key, value in api_urls.items():
        download_api_nice(url=value, name=key)

    # get data
    # icCount: number of ICs with at least 1 COVID-19 case on date of notification
    df_ic_count = pd.read_json(Path(RAW_DATA_FOLDER, f"ic-count-{datetime.date.today()}.json")) \
        .rename({"date": "Datum", "value": "icCount"}, axis=1) \
        .set_index("Datum")

    # intakeCount: number of COVID-19 cases taken into the IC on date of notification
    df_intake_count = pd.read_json(Path(RAW_DATA_FOLDER, f"intake-count-{datetime.date.today()}.json")) \
        .rename({"date": "Datum", "value": "intakeCount"}, axis=1) \
        .set_index("Datum")

    # intakeCumulative: total number of COVID-19 cases that have been taken into the IC up to the date of notification 
    df_intake_cum = pd.read_json(Path(RAW_DATA_FOLDER, f"intake-cumulative-{datetime.date.today()}.json")) \
        .rename({"date": "Datum", "value": "intakeCumulative"}, axis=1) \
        .set_index("Datum")

    # newIntake: number of new COVID-19 cases taken into the IC on the date of notification
    df_new_intake_count, df_new_intake_susp = open_multi_dim_table(
        Path(RAW_DATA_FOLDER, f"new-intake-{datetime.date.today()}.json")
    )
    df_new_intake_count = df_new_intake_count\
        .rename({"date": "Datum", "value": "newIntake"}, axis=1) \
        .set_index("Datum")
        
    # newSuspected: number of new suspected COVID-19 cases taken into the IC on the date of notification   
    df_new_intake_susp = df_new_intake_susp\
        .rename({"date": "Datum", "value": "newSuspected"}, axis=1) \
        .set_index("Datum")
           
    # diedCumulative: total number of IC COVID-19 cases that died up to the date of notification
    df_died, df_survived, df_ontslagen = open_multi_dim_table(
        Path(RAW_DATA_FOLDER, f"died-and-survivors-cumulative-{datetime.date.today()}.json")
    )
    df_died = df_died \
        .rename({"date": "Datum", "value": "diedCumulative"}, axis=1) \
        .set_index("Datum")

    # survivedCumulative: total number of IC COVID-19 cases that walked out of hospital alive up to the date of notification
    df_survived = df_survived \
        .rename({"date": "Datum", "value": "survivedCumulative"}, axis=1) \
        .set_index("Datum")
    
    # dischargedCumulative: total number of IC COVID-19 cases that were discharged from the IC up to the date of notification    
    df_ontslagen = df_ontslagen \
        .rename({"date": "Datum", "value": "dischargedTotal"}, axis=1) \
        .set_index("Datum")

    df_result = pd.concat([
        df_ic_count,
        df_new_intake_count,
        df_intake_count,
        df_intake_cum,
        df_survived,
        df_died,
        df_new_intake_susp,
        df_ontslagen
    ], axis=1)

    print(df_result.head())
    df_result.to_csv(Path("data", "nice_ic_by_day.csv", index=False))
