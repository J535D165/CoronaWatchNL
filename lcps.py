import dateparser
from datetime import datetime
import re

from requests import Session
from retry_requests import retry
import pandas as pd


LCPS_API_URL = 'https://s3.eu-de.cloud-object-storage.appdomain.cloud/cloud-object-storage-lcps/news.json'  # noqa


def get(url):
    session = retry(Session(), retries=10, backoff_factor=0.2)

    ret = session.get(url)

    while ret.status_code != 200:  # keep trying until we succeed
        ret = session.get(url)

    return ret


def titlenormalizer(title):
    return ' '.join(title.split(' ')[0:2]).replace('.', '').lower().strip()


def titleclassifier(title):
    split = title.split(' ')

    if len(split) != 2:
        return False

    try:

        if split[1].startswith('covid') or split[1].startswith('corona'):
            return True

    except ValueError:
        pass

    return False


if __name__ == '__main__':

    news = get(LCPS_API_URL).json()

    year = datetime.now().year

    data = []

    for item in news['updates']:

        # print(item["content"])

        title = titlenormalizer(item['title'])

        # print(item['content'])
        if titleclassifier(title):
            patients = int(title.split(' ')[0])

            date = str(dateparser.parse(item['date'], languages=["nl"]).date())

            matches = re.search(
                r"(\d+)\s+in\s+Duitsland",
                item['content'],
                re.MULTILINE
            )
            patients_in_de = None
            try:
                patients_in_de = int(matches.group(1))
            except AttributeError:
                pass

            data.append({'Date': date, 'Aantal': patients, 'AantalDuitsland': patients_in_de})

    df_parsed_nums = pd.DataFrame(data).set_index('Date').sort_index()

    df_lcps = pd.read_csv('data/lcps_ic.csv', index_col=0)

    df_lcps = df_lcps.combine_first(df_parsed_nums)
    df_lcps['Aantal'] = df_lcps['Aantal'].astype(int)
    df_lcps['AantalDuitsland'] = df_lcps['AantalDuitsland'].astype(int)

    # -- this only needs to run once
    # -- to drop duplicates
    df_lcps.drop_duplicates(inplace=True)
    # -- end

    df_lcps.to_csv('data/lcps_ic.csv')
