"""Download RIVM daily stats"""

from pathlib import Path
import urllib.request

import requests
from lxml import html

# global variables
RIVM_DATA_BASE_URL = "https://www.volksgezondheidenzorg.info"
RIVM_DATA_BASE_CORONA_URL = RIVM_DATA_BASE_URL + \
    "/onderwerp/infectieziekten/regionaal-internationaal/coronavirus-covid-19"


def verify_dataset():
    pass


def download_rivm_data(url):

    retrieved_url = RIVM_DATA_BASE_URL + url
    file_name = retrieved_url.split("/")[-1]

    verify_dataset()

    # create raw_data folder
    Path('raw_data').mkdir(parents=True, exist_ok=True)

    # download data
    # if not Path('raw_data', file_name).exists():
    urllib.request.urlretrieve(
        retrieved_url,
        Path('raw_data', file_name)
    )

    print("File downloaded:", str(Path('raw_data', file_name)))


def find_data_url():

    web_response = requests.get(RIVM_DATA_BASE_CORONA_URL)
    element_tree = html.fromstring(web_response.text)

    result = element_tree.xpath("//a[@class='csv-export detail-data']")
    if len(result) == 1:
        return result[0].attrib['href']
    else:
        raise Exception("URL not found")


if __name__ == '__main__':

    url = find_data_url()
    print("Downloading", url)
    download_rivm_data(url)
