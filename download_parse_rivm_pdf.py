# make sure poppler is installed else pdftotext build fails
# https://stackoverflow.com/questions/45912641/unable-to-install-pdftotext-on-python-3-6-missing-poppler

# python -m pip install tabula-py pdftotext retry_requests requests

from retry_requests import retry
from requests import Session
import re

def get(url):
    session = retry(Session(), retries=10, backoff_factor=0.2)

    ret = session.get(url)

    while ret.status_code != 200:  # keep trying until we succeed
        ret = session.get(url)

    return ret

site_text = get('https://www.rivm.nl/coronavirus-covid-19/grafieken').text

m = re.search(r'href="([^ ]*COVID-19_WebSite_rapport_([^_]*)_[^ "]*.pdf)"', site_text)
pdf_url = m.group(1)

rapport_file = 'rivm_rapport.pdf'
unparsed_date = m.group(2)
publication_date = unparsed_date[0:4] + '-' + unparsed_date[4:6] + '-' + unparsed_date[6:8]

print(f'Publication date: {publication_date}')

with open(rapport_file, 'wb') as fh:
    dl = get(pdf_url)
    fh.write(dl.content)

import tabula
import pdftotext
import pandas as pd

def filter_table_single_day_only(df):
    print

def pdf_find_page_for_text(file, text):
    with open(file, "rb") as fh:
        pdf = pdftotext.PDF(fh)
    
    counter = 1
    for page in pdf:
        if text in page:
            return counter
        counter += 1
    

page = pdf_find_page_for_text(rapport_file, "Virologische dagstaten")
print(f'page: {page}', rapport_file)
df = tabula.read_pdf(rapport_file, pages=f'{page}')[0]

expected_columns = ['Datum van - tot', 'Labs', 'Geteste pers.', 'Pos.', 'uitslag', '% Pos.']
drop = ['Pos.']

if list(df.columns) != expected_columns:
    print('Columns did not match, something is wrong')
    print(f'Expected: {expected_columns}')
    print(f'Got: {list(df.columns)}')
    
df = df.drop(columns=drop)

data = []
for idx, row in df.iterrows():
    if ' - ' not in row['Datum van - tot']:  # only use single-day stats, skip the ranged 'van-tot' ones
        data.append({
            'PublicatieDatum': publication_date,
            'Datum': row['Datum van - tot'].strip(),
            'Labs': row['Labs'],
            'Type': 'Getest',
            'Aantal': row['Geteste pers.']
        })
        
        data.append({
            'PublicatieDatum': publication_date,
            'Datum': row['Datum van - tot'].strip(),
            'Labs': row['Labs'],
            'Type': 'Positief',
            'Aantal': row['uitslag']
        })
        
print(pd.DataFrame(data))
