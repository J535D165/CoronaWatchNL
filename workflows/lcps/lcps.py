import dateparser
from datetime import datetime
import re

from requests import Session
from retry_requests import retry
import pandas as pd

from bs4 import BeautifulSoup


LCPS_API_URL = 'https://lcps.nu/nieuws/'  # noqa


def htmltoobj(content):
    soup = BeautifulSoup(content, 'html.parser')
    updates = []

    for post in soup.select('div.post'):
        title = post.select_one('h3').text
        date = post.select_one('span.meta span').text
        content = post.select_one('div.excerpt').text

        updates.append({
            "title": title.strip(),
            "date": date.strip(),
            "content": content.strip()
        })

    return {'updates': updates}


def get(url):
    session = retry(Session(), retries=10, backoff_factor=0.2)

    headers = {'User-Agent': 'curl/7.51.0'}  # curl is fine, requests is not :/
    ret = session.get(url, headers=headers)

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

    news = htmltoobj(get(LCPS_API_URL).content)

    year = datetime.now().year

    data = []

    for item in news['updates'][0:10]:

        # print(item["date"])

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
            patients_in_de = 0
            try:
                patients_in_de = int(matches.group(1))
            except AttributeError:
                pass

            data.append({'Date': date, 'Aantal': patients,
                         'AantalDuitsland': patients_in_de})

    df_parsed_nums = pd.DataFrame(data).set_index('Date').sort_index()

    df_lcps = pd.read_csv('data/lcps_ic.csv', index_col=0)

    df_lcps = df_lcps.combine_first(df_parsed_nums)
    df_lcps['Aantal'] = df_lcps['Aantal'].astype(pd.Int64Dtype())
    df_lcps['AantalDuitsland'] = df_lcps['AantalDuitsland'].astype(pd.Int64Dtype())

    df_lcps[~df_lcps.index.duplicated()]
    df_lcps[["Aantal"]].to_csv('data/lcps_ic.csv')

    df_lcps_country = df_lcps.copy()
    df_lcps_country['Nederland'] = df_lcps['Aantal'] - df_lcps['AantalDuitsland']
    df_lcps_country['Duitsland'] = df_lcps['AantalDuitsland']
    df_lcps_country = df_lcps_country[["Nederland"]].stack(dropna=False)
    df_lcps_country.index.names = ['Datum', 'Land']
    df_lcps_country.name = "Aantal"
    df_lcps_country = df_lcps_country.to_frame()

    df_lcps_country_from_file = pd.read_csv('data/lcps_ic_country.csv', index_col=[0, 1])

    df_lcps_country = df_lcps_country_from_file.combine_first(df_lcps_country)
    df_lcps_country[~df_lcps_country.index.duplicated()]
    df_lcps_country['Aantal'] = df_lcps_country['Aantal'].astype(pd.Int64Dtype())

    df_lcps_country = df_lcps_country[df_lcps_country['Aantal'] != 0]
    df_lcps_country[["Aantal"]].to_csv('data/lcps_ic_country.csv')
