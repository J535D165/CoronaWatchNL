import json
import requests
from bs4 import BeautifulSoup
import pandas as pd


# Change this
OUTPUT_FILE = 'euromomo.json'

# Change this if the script breaks
BASE_PAGE = "https://www.euromomo.eu/graphs-and-maps/"
JS_FILE_PATTERN = "src-templates-graphs-and-maps-js"


def normalize_country_name(name):
    return name.lower().strip().replace(' ', '-').replace('(', '').replace(')', '')


def extract_pandas(data):
    keys = list(data.keys())

    expected = ['pooled', 'countries']

    valid = all([True if k in keys else False for k in expected])

    if not valid:
        raise Exception('EuroMOMO changed something, expected keys not found in data')

    weeks = data['countries']['weeks']

    sheetdata = {'year-week': weeks, 'year': [d.split('-')[0] for d in weeks], 'week': [d.split('-')[1] for d in weeks]}

    for country in data['countries']['countries']:
        #print(country['country'])
        for group in country['groups']:
            #print(group['group'])

            column_name = normalize_country_name(country['country']) +\
                '_' +\
                group['group'].lower().strip().replace(' ', '-')

            groupdata = group['zscore']

            sheetdata[column_name] = groupdata
            
    return pd.DataFrame.from_dict(sheetdata).set_index('year-week').dropna()


# First, we need to find the JS link inside the webpage
r = requests.get(BASE_PAGE)
if r.status_code != 200:
    raise Exception(f"Cannot reach webpage {BASE_PAGE} {r.status_code}")
soup = BeautifulSoup(r.text)
link_to_file = None
for possible in soup.find_all("link", attrs={"as": "script"}):
    if JS_FILE_PATTERN in possible['href']:
        link_to_file = "https://www.euromomo.eu" + possible['href']
        break

if link_to_file is None:
    print(f"Could not find a JS file with {JS_FILE_PATTERN} in its name :-(")
    exit(1)

# Now we have found the file, let's download it and find a large JSON part inside
try:
    js_file: str = requests.get(link_to_file).text
    pos = 0
    found = []
    while True:
        pos = js_file.find("JSON.parse('", pos)
        if pos == -1:
            break
        end_pos = js_file.find("')", pos)

        content = js_file[pos+len("JSON.parse('"):end_pos]
        assert "'" not in content
        found.append(content)
        pos += 1

    # the biggest JSON part in the file is probably the good one ;-)
    biggest = max(found, key=lambda x: len(x))  
    
    # Load it!
    data = json.loads(biggest)

    df = extract_pandas(data)
    df.to_csv('data/euromomo_excess_mortality_zscores.csv', index=True)
except:
    print("EUROMOMO modified something in the JS, you need to adapt the script!")
    raise

