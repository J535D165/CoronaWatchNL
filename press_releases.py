"""Download RIVM daily stats"""

from pathlib import Path
import re
import datetime

import pandas
import requests
from lxml import html

# global variables
RIVM_NEWSFEED_URL = "https://www.rivm.nl/nieuws/actuele-informatie-over-coronavirus"


def download_rivm_press_releases():

    # create raw_data folder
    Path('raw_data', 'news').mkdir(parents=True, exist_ok=True)

    # download data
    doc = requests.get(RIVM_NEWSFEED_URL)
    page = html.fromstring(doc.content)
    data = page.xpath("//div[@class='par content-block-wrapper']/div")

    # get the html and split on the <hr> tag (data[0] to data[1] for old posts)
    articles = str(html.tostring(data[0])).split("<hr>")[2:-1]

    for article in articles:

        # extract the date
        article_tree = html.fromstring(article)

        date = re.search("(\d{2})-(\d{1,2})-(\d{4}).*?(\d{1,2}).(\d{2})", article)
        date_flat = date.group(3) + "-" + date.group(2).rjust(2, "0") + "-" + date.group(1).rjust(2, "0") + "-" + date.group(4).rjust(2, "0") + "-" + date.group(5)

        with open(Path('raw_data', 'news', f"rivm_news_{date_flat}.html"), "w") as f:
            f.write(article)

        with open(Path('raw_data', 'news', f"rivm_news_{date_flat}.txt"), "w", newline="\n") as f:
            content = article_tree.text_content().replace("\\n", "\n").replace("\\t", "\t")
            f.write(content)


def merge_press_releases():

    files = Path('raw_data', 'news').glob("*.txt")

    result = []

    for release in files:

        # extract date
        date = re.search("(\d{4})-(\d{2})-(\d{2})-(\d{2})-(\d{2})", str(release))
        parsed_date = datetime.datetime(
            int(date.group(1)),
            int(date.group(2)),
            int(date.group(3)),
            int(date.group(4)),
            int(date.group(5)),
        )

        with open(release, "r") as f:
            content = f.read()
        item = {
            'DatumTijd': parsed_date,
            'Persbericht': content
        }
        result.append(item)

    df = pandas.DataFrame(result)
    df.sort_values('DatumTijd', inplace=True)

    return df


if __name__ == '__main__':

    download_rivm_press_releases()
    df = merge_press_releases()

    df.to_csv(Path("data", "rivm_press_releases.csv"), index=False)
