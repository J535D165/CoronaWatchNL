# python -m pip install pdftotext pandas 

from pathlib import Path

# this should point to the CoronaWatchNL reports dir
reports_dir = Path('reports/')

def extract_date_from_report_filename(el):
    return int(str(el).split('_')[-1].split('.')[0])

report_files = []
for d in reports_dir.iterdir():
    if str(d).endswith('.pdf') and 'epidemiological' in str(d):
        report_files.append(d)
        
report_files = sorted(report_files, key=extract_date_from_report_filename)

from pprint import pprint
pprint(report_files)


import pdftotext
import pandas as pd
import re

def filter_table_single_day_only(df):
    print

def pdf_find_page_for_text(file, text):
    with open(file, "rb") as fh:
        pdf = pdftotext.PDF(fh)

    counter = 1
    for page in pdf:
        if text.lower() in page.lower():
            return counter
        counter += 1

def isint(s):
    try:
        i = int(s)
        return True
    except ValueError:
        return False


def extract_rows(lines):
    columns = re.findall('[A-Z][^A-Z]*', lines[0].strip())  # split on uppercase letters
    #columns = re.split(r'\s{2,}', lines[0].strip())  # split on >= 2 whitespaces

    data = []

    for row in lines[1:]:
        values = re.split(r'\s{2,}', row.strip())  # split field values on >= whitespaces

        if len(values) <= 1:
            continue

        if values[1] == '-':
            values = [f'{values[0]} - {values[2]}'] + values[3:]

        if values[1].strip().startswith('- 2'):
            values = [f'{values[0]} {values[1]}'] + values[2:]

        rowdata = {}
        for i in range(0, len(columns)):
            column = columns[i].replace('%', '').strip()  # remove %-sign, it is in the wrong column
            rowdata[column] = values[i].strip()

        data.append(rowdata)

    return pd.DataFrame(data)


def alt_table_extractor(file, page):
    with open(file, "rb") as fh:
        pdf = pdftotext.PDF(fh)
        page = pdf[page]
        valid_lines = []

        table_found = False
        for line in page.splitlines():
            if line.strip().lower().startswith('tabel'):
                table_found = True
                continue

            if not (line.strip().lower().startswith('datum') or isint(line.strip()[0:4])):
                continue

            if not table_found:
                continue

            if line.strip() == '':
                continue

            valid_lines.append(line)

    ret = extract_rows(valid_lines)

    return ret


column_mappings = {
    ('Datum', 'Rapp. labs', 'Geteste pers.', 'Pers. met pos. uitslag', 'Perc. pos.', ): {
        'drop': [],
        'mappings': {
            'Datum': 'date',
            'Rapp. labs': 'labs',
            'Geteste pers.': 'tested',
            'Pers. met pos. uitslag': 'positive',
            'Perc. pos.': 'perc_positive'
        }
    },
    ('Datum', 'Rapp.', 'labs', 'Geteste pers.', 'Pers.', 'met pos.', 'uitslag', 'Perc.', 'pos.', ): {
        'drop': ['Rapp.', 'Pers.', 'met pos.', 'Perc.'],
        'mappings': {
            'Datum': 'date',
            'labs': 'labs',
            'Geteste pers.': 'tested',
            'uitslag': 'positive',
            'pos.': 'perc_positive'
        }
    },
    ('Datum van - tot', 'Labs', 'Geteste pers.', 'Pos.', 'uitslag', '% Pos.', ): {
        'drop': ['Pos.'],
        'mappings': {
            'Datum van - tot': 'date',
            'Labs': 'labs',
            'Geteste pers.': 'tested',
            'uitslag': 'positive',
            '% Pos.': 'perc_positive'
        }
    },
    ('Datum van - tot', 'Labs', 'Geteste pers.', 'Pos. uitslag', 'Pos.'): {
        'drop': [],
        'mappings': {
            'Datum van - tot': 'date',
            'Labs': 'labs',
            'Geteste pers.': 'tested',
            'Pos. uitslag': 'positive',
            'Pos.': 'perc_positive'
        }
    }
}

def get_df_for_pdf(rapport_file, page_text):
    page = pdf_find_page_for_text(rapport_file, page_text)

    if page is None:
        return None

    pubdate = str(extract_date_from_report_filename(rapport_file))
    pubdate = f'{pubdate[0:4]}-{pubdate[4:6]}-{pubdate[6:8]}'

    print(f'page: {page}', rapport_file)

    df = alt_table_extractor(rapport_file, page - 1)
    cols = tuple(list(df.columns))

    if cols not in column_mappings:
        print('Columns did not match any known patterns, something is wrong')
        print(f'Got: {cols}')
        print(df)
        return None

    df = df.drop(columns=column_mappings[cols]['drop'])
    df = df.rename(columns=column_mappings[cols]['mappings'])

    data = []
    for idx, row in df.iterrows():
        if ' - ' not in row['date'] and 'T/m' not in row['date']:  # only use single-day stats, skip the ranged 'van-tot' ones
            data.append({
                'PublicatieDatum': pubdate,
                'Datum': row['date'].strip(),
                'Labs': row['labs'],
                'Type': 'Getest',
                'Aantal': row['tested']
            })

            data.append({
                'PublicatieDatum': pubdate,
                'Datum': row['date'].strip(),
                'Labs': row['labs'],
                'Type': 'Positief',
                'Aantal': row['positive']
            })

    return pd.DataFrame(data)

result = None
counter = 0
tests_dfs = []
for report_file in report_files:
    result = get_df_for_pdf(report_file, "Virologische dagstaten")
    if result is not None:
        tests_dfs.append(result)


df_result = tests_dfs[0].copy()

for test_df in tests_dfs[1:]:
    for idx, row in test_df.iterrows():
        original_row = df_result[(df_result['Datum'] == row['Datum']) & (df_result['Type'] == row['Type'])]

        if len(original_row) > 0:  # row exists in df_result, let's update
            for col in test_df.columns:
                df_result.at[original_row.index[0], col] = row[col]
        else:  # this row is new
            df_result = df_result.append(row, ignore_index=True)

df_result['Labs'] = df_result['Labs'].astype(int)
df_result['Aantal'] = df_result['Aantal'].astype(int)

df_result_cumulative = df_result.copy()

# append first-known values manually
df_result_cumulative.loc[-2] = ['2020-03-31', '2020-03-21',  33, 'Positief', 4733]
df_result_cumulative.loc[-1] = ['2020-03-31', '2020-03-21',  33, 'Getest', 35317]
df_result_cumulative.index = df_result_cumulative.index + 2
df_result_cumulative.sort_index(inplace=True)

df_result_cumulative['Aantal'].update(df_result_cumulative[df_result_cumulative['Type'] == 'Positief']['Aantal'].cumsum())
df_result_cumulative['Aantal'].update(df_result_cumulative[df_result_cumulative['Type'] == 'Getest']['Aantal'].cumsum())

df_result_cumulative

df_result_cumulative.to_csv('data/rivm_NL_covid19_tests.csv')
