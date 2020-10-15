#!/usr/bin/env bash

d=`date +%Y-%m-%d`
d="2020-07-03"

RIVM_CDN="https://data.rivm.nl/"
COVID_CDN="$RIVM_CDN/covid-19"

curl "$COVID_CDN/COVID-19_aantallen_gemeente_cumulatief.json" -o "raw_data/api_data/COVID-19_aantallen_gemeente_cumulatief-${d}.json"
curl "$COVID_CDN/COVID-19_aantallen_gemeente_cumulatief.csv" -o "raw_data/api_data/COVID-19_aantallen_gemeente_cumulatief-${d}.csv"
curl "$COVID_CDN/COVID-19_casus_landelijk.json" -o "raw_data/api_data/COVID-19_casus_landelijk-${d}.json"
curl "$COVID_CDN/COVID-19_casus_landelijk.csv" -o "raw_data/api_data/COVID-19_casus_landelijk-${d}.csv"
