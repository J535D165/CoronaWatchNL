from retry_requests import retry
from requests import Session
from datetime import datetime
import locale
import pandas as pd


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
        retval = int(split[0])
        if split[1].startswith('covid') or split[1].startswith('corona'):
            return True

    except ValueError:
        pass

    return False

locale.setlocale(locale.LC_TIME, 'nl_NL.utf8')  # set locale to netherlands for date parsing

news = get('https://s3.eu-de.cloud-object-storage.appdomain.cloud/cloud-object-storage-lcps/news.json').json()

year = datetime.now().year

data = []

for item in news['updates']:
    title = titlenormalizer(item['title'])
    if titleclassifier(title):
        patients = int(title.split(' ')[0])
        date = str(datetime.strptime(item['date'], '%A %d %B').replace(year=year).date())

        data.append({'Date': date, 'Aantal': patients})


df_parsed_nums = pd.DataFrame(data).set_index('Date').sort_index()

df_lcps = pd.read_csv('data/lcps_ic.csv', index_col=0)

df_lcps = df_lcps.combine_first(df_parsed_nums)
df_lcps['Aantal'] = df_lcps['Aantal'].astype(int)

df_lcps.to_csv('data/lcps_ic.csv')
