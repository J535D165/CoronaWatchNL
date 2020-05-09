"""Download and parse measures data to CSV"""

import csv
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd
from urllib.request import urlretrieve

# JSONs to download.
URL_MEASURES_HISTORY = 'https://covid-statistics.jrc.ec.europa.eu/api/Measure/GetHistory/NLD/true'
URL_MEASURES_LATEST = 'https://covid-statistics.jrc.ec.europa.eu/api/Measure/GetLast/NLD'


def write_json_to_csv(fp_import, fp_export):

    print('Writing json to {}'.format(fp_export))

    try:
        with open(fp_import, "r") as f:
            measures_dict = json.load(f)
            df_measures = pd.DataFrame(measures_dict["measures"])
            del df_measures["rowCount"]
            df_measures.to_csv(fp_export, index=False)
    except Exception as e:
        sys.exit('ERROR: could not write json to csv {} ({})'.format(fp_export, e))


if __name__ == '__main__':

    # download the files
    Path("raw_data", "measures").mkdir(parents=True, exist_ok=True)

    urlretrieve(
        URL_MEASURES_HISTORY,
        str(Path("raw_data", "measures", "MeasureGetHistoryNLD.json"))
    )

    urlretrieve(
        URL_MEASURES_LATEST,
        str(Path("raw_data", "measures", "MeasureGetLastNLD.json"))
    )

    Path("data-misc", "data-measures").mkdir(parents=True, exist_ok=True)

    write_json_to_csv(
        Path("raw_data", "measures", "MeasureGetHistoryNLD.json"),
        Path("data-misc", "data-measures", "NLD_measures.csv")
    )

    write_json_to_csv(
        Path("raw_data", "measures", "MeasureGetLastNLD.json"),
        Path("data-misc", "data-measures", "NLD_measures_latest.csv")
    )
