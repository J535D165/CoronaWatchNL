"""Download and parse NICE data to CSV"""

import csv
import json
import os
import sys
import shutil
from datetime import datetime
from pathlib import Path
import numpy as np
import pandas as pd
import requests

# JSONs to download.
# Files with single object (dict) and files with single array (list(dict)) are supported out of the box
NICE_URLS = ['https://www.stichting-nice.nl/covid-19/public/new-intake',  # new IC patients with proven COVID-19, per day
             # current total IC patients with proven COVID-19, per day
             'https://www.stichting-nice.nl/covid-19/public/intake-count',
             # cumulative IC patients with proven COVID-19, per day
             'https://www.stichting-nice.nl/covid-19/public/intake-cumulative',
             # current total of ICUs with at least one proven COVID-19 patient, per day
             'https://www.stichting-nice.nl/covid-19/public/ic-count',
             'https://www.stichting-nice.nl/covid-19/public/died-and-survivors-cumulative']  # cumulative IC patients with proven COVID-19 that died and survived, per day

# https://www.stichting-nice.nl/covid-19/public/global is also available, but doesn't have a date or other lastupdate indicator


def download_json(urls):
    """Download a list of JSONs, return dictionary with filename => data"""
    data = {}
    for url in urls:
        name = url.rsplit('/', 1)[-1]
        print('Downloading {}'.format(url))
        try:
            resp = requests.get(url)
        except Exception as e:
            sys.exit('ERROR: could not download {} ({})'.format(url, e))

        if name == 'died-and-survivors-cumulative':
            # parse died and survivors to their own files
            died = []
            survived = []
            for i, v in enumerate(resp.json()):
                for l in v:
                    if i == 0:
                        l['diedCumulativeNew'] = l.pop('value')
                        died.append(l)

                    else:
                        l['survivedCumulative'] = l.pop('value')
                        survived.append(l)

            data['died-cumulative'] = died
            data['survived-cumulative'] = survived
        else:
            data[name] = resp.json()

    return data

# use this if you want to store the raw JSONs


def dump_json(data, dir):
    """Parse a dictionary of JSONs. Key = filename (without .json)"""

    try:
        Path(dir).mkdir(parents=True, exist_ok=True)
    except Exception as e:
        sys.exit('ERROR: could not create dir {} ({})'.format(dir, e))

    # add current datetime to filename
    dt = datetime.now().strftime('%Y-%m-%d')

    for name, content in data.items():
        file = dir + name + '-' + dt + '.json'
        print('Dumping raw to {}'.format(file))

        try:
            with open(file, 'w') as out:
                json.dump(content, out)
        except Exception as e:
            sys.exit('ERROR: could not dump json to {} ({})'.format(file, e))

    return True


def write_json_to_csv(data, dir):
    """Write a dictionary of filename => data (dict) to CSVs in dir"""
    for file, json in data.items():
        file = dir + file + '.csv'

        print('Writing json to {}'.format(file))

        try:
            with open(file, 'w', newline='') as out_f:
                if isinstance(json, dict):
                    # single object
                    # get header
                    header = list(json.keys())

                    # put data in list so it will fit in the DictWriter
                    lines = [json]
                else:
                    # single array
                    # get header
                    l = json[0]
                    header = []
                    for k, v in l.items():
                        header.append(k)

                    lines = json

                # write the header
                writer = csv.DictWriter(out_f, fieldnames=header)
                writer.writeheader()

                # write the data
                for l in lines:
                    writer.writerow(l)
        except Exception as e:
            sys.exit('ERROR: could not write json to csv {} ({})'.format(file, e))


def merge_csvs(merge_list, dir, on, choose, dtype=int):
    """Merge CSV files from list in dir, join on 'on', select values
    with numpy func 'choose', convert values to dtype.

    Returns pandas DataFrame"""
    # first file is filea
    filea = merge_list[0]
    try:
        a = pd.read_csv(dir + filea)
    except Exception as e:
        sys.exit('ERROR: could not read {} ({})'.format(dir + filea, e))

    l = iter(merge_list)
    next(l)

    labels = []

    # loop through the rest as fileb
    for fileb in l:
        try:
            b = pd.read_csv(dir + fileb)
        except Exception as e:
            sys.exit('ERROR: could not read {} ({})'.format(dir + fileb, e))

        # merge filea and b
        print('Merging {} to {}'.format(fileb, filea))
        merged = a.merge(b, how='left', on=on)

        # collect labels; choose values; fix N/A; convert to int
        for k in b.keys():
            if k != on:
                xy = [k + '_x', k + '_y']
                for label in xy:
                    if label in merged.columns:
                        merged[k] = choose(merged[xy], axis=1)
                        if label not in labels:
                            labels.append(label)
                # forward fill NaN. First row = 0
                if np.isnan(merged.iloc[0, merged.columns.get_loc(k)]):
                    merged.iloc[0, merged.columns.get_loc(k)] = 0
                merged[k] = merged[k].fillna(method='ffill').astype(int)

        a = merged
    # drop _x and _y labels
    a.drop(labels=labels, axis=1, inplace=True)

    return a


def cleanup_processing(dir):
    """Delete all contents in dir of dir itself"""
    print('Cleaning up processing')
    for filename in os.listdir(dir):
        file_path = os.path.join(dir, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print('ERROR: could not delete {}. ({})'.format(file_path, e))


if __name__ == '__main__':
    # download jsons
    data = download_json(NICE_URLS)

    # dump jsons to raw_data, by date
    json_dir = 'raw_data/nice/'
    dump_json(data, json_dir)

    # write jsons to csv
    processing_dir = 'raw_data/nice/processing/'
    Path(processing_dir).mkdir(parents=True, exist_ok=True)
    write_json_to_csv(data, processing_dir)

    # list of csvs to merge (join)
    merge_list = ('ic-count.csv', 'intake-count.csv', 'intake-cumulative.csv',
                  'new-intake.csv', 'died-cumulative.csv', 'survived-cumulative.csv')

    # join files on
    on = 'date'

    # numpy function for choosing which value, in case of duplicate columns
    choose = np.max

    # merge the CSVs
    new_csv = merge_csvs(merge_list, processing_dir, on, choose)

    # fix 0s in intakeCumulative: replace all with NaN, ffill, replace first NaN with 0
    new_csv['intakeCumulative'] = new_csv.intakeCumulative.replace(0, np.nan)
    new_csv['intakeCumulative'] = new_csv.intakeCumulative.fillna(
        method='ffill')
    new_csv['intakeCumulative'] = new_csv.intakeCumulative.fillna(
        0).astype(int)

    # clean up columns. diedCumulative and isCumulative never have data, so drop them.
    drop_columns = ['diedCumulative', 'icCumulative']
    new_csv.drop(labels=drop_columns, axis=1, inplace=True)
    new_csv.rename(
        columns={'diedCumulativeNew': 'diedCumulative'}, inplace=True)

    # new file to merge to
    data_dir = 'data/'
    filename = 'nice_ic_by_day.csv'
    file_new = data_dir + filename

    # write to csv
    print('Writing merged data to {}'.format(file_new))
    try:
        new_csv.to_csv(file_new, index=False)
    except Exception as e:
        print('ERROR: could not write new csv to {} ({})'.format(file_new, e))

    # clean up processing
    cleanup_processing(processing_dir)
