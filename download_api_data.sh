d=`date +%Y-%m-%d`
d="2020-07-02"

curl https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_cumulatief.json > raw_data/api_data/COVID-19_aantallen_gemeente_cumulatief-${d}.json
curl https://data.rivm.nl/covid-19/COVID-19_aantallen_gemeente_cumulatief.csv > raw_data/api_data/COVID-19_aantallen_gemeente_cumulatief-${d}.csv
curl https://data.rivm.nl/covid-19/COVID-19_casus_landelijk.json > raw_data/api_data/COVID-19_casus_landelijk-${d}.json
curl https://data.rivm.nl/covid-19/COVID-19_casus_landelijk.csv > raw_data/api_data/COVID-19_casus_landelijk-${d}.csv
