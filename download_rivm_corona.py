"""Download RIVM daily stats"""

from pathlib import Path
import re

import requests
from lxml import html

# global variables
RIVM_DATA_BASE_CORONA_URL = "https://www.rivm.nl/coronavirus-kaart-van-nederland"


def verify_dataset():
    pass


def download_rivm_data():

    verify_dataset()

    # create raw_data folder
    Path('raw_data').mkdir(parents=True, exist_ok=True)

    # download data
    doc = requests.get(RIVM_DATA_BASE_CORONA_URL)
    page = html.fromstring(doc.content)
    data = page.get_element_by_id("csvData").text
    data = data.lstrip()

    print(data)

    datetime_pub = data.split("\n")[1].split(";")[0]
    datetime_pub = re.sub('[^a-zA-Z0-9]', '-', datetime_pub)

    with open(str(Path('raw_data', "{}.csv".format(datetime_pub))), "w", encoding="utf-8") as f:
        f.write(data)

    print("Downloaded {}".format(str(Path('raw_data', "{}.csv".format(datetime_pub)))))

if __name__ == '__main__':

    print("Downloading")
    download_rivm_data()
