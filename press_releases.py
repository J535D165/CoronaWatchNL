"""Download RIVM daily stats"""

from pathlib import Path
import re

import requests
from lxml import html

# global variables
RIVM_NEWSFEED_URL = "https://www.rivm.nl/nieuws/actuele-informatie-over-coronavirus"


def download_rivm_data():

    # create raw_data folder
    Path('raw_data', 'news').mkdir(parents=True, exist_ok=True)

    # download data
    doc = requests.get(RIVM_NEWSFEED_URL)
    page = html.fromstring(doc.content)
    data = page.xpath("//div[@class='par content-block-wrapper']/div")

    # get the html and split on the <hr> tag
    articles = str(html.tostring(data[0])).split("<hr>")[2:-1]

    for article in articles:

        # extract the date
        article_tree = html.fromstring(article)

        date = re.search("(\d{2})-(\d{1,2})-(\d{4}).*?(\d{1,2}).(\d{2})", article)
        date_flat = date.group(3) + "-" + date.group(2).rjust(2, "0") + "-" + date.group(1).rjust(2, "0") + "-" + date.group(4) + "-" + date.group(5)

        with open(Path('raw_data', 'news', f"rivm_news_{date_flat}.html"), "w") as f:
            f.write(article)

        with open(Path('raw_data', 'news', f"rivm_news_{date_flat}.txt"), "w", newline="\n") as f:
            content = article_tree.text_content().replace("\\n", "\n").replace("\\t", "\t")
            f.write(content)


if __name__ == '__main__':

    download_rivm_data()
