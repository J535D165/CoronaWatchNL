![corona_artwork.jpg](corona_artwork.jpg)

# Dataset: COVID-19 case counts in The Netherlands

[:exclamation: :exclamation: :exclamation: Data changes by RIVM - 31 March 2020 #44 :exclamation: :exclamation: :exclamation: ](https://github.com/J535D165/CoronaWatchNL/issues/44)

**CoronaWatchNL** collects COVID-19 disease count cases in **The Netherlands**. Numbers are collected from the RIVM (National Institute for Public Health and the Environment) website on a daily basis. This project standardizes, and publishes data and makes it **Findable, Accessible, Interoperable, and Reusable (FAIR)**. We aim to collect a complete time series and prepare a dataset for reproducible analysis and academic use.

Dutch: 
> CoronalWatchNL verzamelt ziektecijfers over COVID-19 in Nederland. Dagelijks worden de cijfers verzameld van de website van het RIVM. Dit project standaardiseert en publiceert de gegevens en maakt ze vindbaar, toegankelijk, interoperabel en herbruikbaar (FAIR). We streven ernaar om een dataset beschikbaar te stellen voor reproduceerbare analyses en wetenschappelijk gebruik. 


## Datasets

The following datasets are available for reuse. :exclamation: Daily updates :exclamation:

| Dataset | URL | Source | Variables |
|---|---| --- | --- |
| COVID-19 disease case counts in NL per province (NEW) | [data/rivm_NL_covid19_province.csv](data/rivm_NL_covid19_province.csv) | RIVM | Date, Province, Number of positive COVID-19 disease cases in NL| 
| COVID-19 hospitalizations in NL per municipality (NEW) |[data/rivm_NL_covid19_hosp_municipality.csv](data/rivm_NL_covid19_hosp_municipality.csv) | RIVM | Date, Number of COVID-19 hospitalized patients in NL, Municipality of residence, Municipality code (2019), Province |
| COVID-19 disease case counts in NL per age (NEW) | [data/rivm_NL_covid19_age.csv](data/rivm_NL_covid19_age.csv) | RIVM | Date, Age group, Type, Number of positive COVID-19 disease cases in NL| 
| COVID-19 disease case counts in NL per gender (NEW) | [data/rivm_NL_covid19_sex.csv](data/rivm_NL_covid19_sex.csv) | RIVM | Date, Gender group, Type, Number of positive COVID-19 disease cases in NL| 
| COVID-19 disease case counts in NL | [data/rivm_corona_in_nl_daily.csv](data/rivm_corona_in_nl_daily.csv) | RIVM | Date, Number of positive COVID-19 disease cases in NL| 
| COVID-19 fatalities in NL | [data/rivm_corona_in_nl_fatalities.csv](data/rivm_corona_in_nl_fatalities.csv) | RIVM | Date, Number of COVID-19 fatalities in NL | 
| COVID-19 hospitalizations in NL | [data/rivm_corona_in_nl_hosp.csv](data/rivm_corona_in_nl_hosp.csv) | RIVM | Date, Number of COVID-19 hospitalized patients in NL | 
| RIVM press releases (NEW) | [data/rivm_press_releases.csv](data/rivm_press_releases.csv) | RIVM | Date and Time, Content of press release | 

### Inactive

| Dataset | URL | Source | Variables | Expire date
|---|---| --- | --- | --- | 
| COVID-19 disease case counts in NL |[[long format]](data/rivm_corona_in_nl.csv) [[wide format]](data/rivm_corona_in_nl_table.csv) | RIVM | Date, Number of positive COVID-19 disease cases in NL, Municipality of residence, Municipality code (2019), Province | 2020-03-30


CoronaWatchNL collects copies of the raw data such that data collection is verifiable. Copies of the collected data can be found in the folder [raw_data/](raw_data/). The data isn't standardised.

For academic use, please use  [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3711575.svg)](https://doi.org/10.5281/zenodo.3711575) and see the section [License and academic use](#license-and-academic-use)

## Data collection sources

The following sources are used for data collection. 

| Source | Institute |Collected variables |
|---|---| --- |
| https://www.rivm.nl/nieuws/actuele-informatie-over-coronavirus | RIVM | Positively tested patients, Fatalities (total), Hospitalized (total) | 
| https://www.rivm.nl/coronavirus-kaart-van-nederland-per-gemeente | RIVM | Positive tests per municipality | 
| https://www.rivm.nl/nieuws/actuele-informatie-over-coronavirus/data | RIVM |Epidemiological reports | 


## Remarks 

Since 3 March 2020, RIVM reports the number of diagnoses with the coronavirus and their municipality of residence on a daily base. The data contains the total number of positively tested patients. It is not a dataset with the current number of sick people in the Netherlands. The RIVM does not currently provide data on people who have been cured.


## Graphs

The following graphs show the development of Coronavirus on a daily basis. The underlying data can be found in the [data folder](/data). The [graphs](/plots) are updated on an hourly basis and were generated automatically. Please validate the numbers in the graphs before publishing. See the license section for information about sharing the graphs.

### Descriptive

[Click here for a subpage with all descriptive plots](readmes/descriptive_plots.md)

[<img src="plots/overview_plot.png" width="430">](readmes/descriptive_plots.md) [<img src="plots/overview_plot_diff.png" width="430">](readmes/descriptive_plots.md) [<img src="plots/overview_plot_geslacht.png" width="430">](readmes/descriptive_plots.md) [<img src="plots/overview_plot_leeftijd.png" width="430">](readmes/descriptive_plots.md)



### Maps

[Click here for a subpage with all maps](readmes/map_plots.md)

[![Map plots](plots/map_province.png)](readmes/descriptive_plots.md)

### Forecast

[Click here fore a subpage with all forecasts](readmes/forecast_plots.md)

<p float="left">
  <a href="/readmes/forecast_plots.md"><img src="/plots/prediction.png" width="250" /></a>
  <a href="/readmes/forecast_plots.md"><img src="/plots/growthfactor.png" width="250" /></a>
  <a href="/readmes/forecast_plots.md"><img src="/plots/sigmoid.png" width="250" /></a>
</p>

## Interesting links

- https://medium.com/@tomaspueyo/coronavirus-act-today-or-people-will-die-f4d3d9cd99ca
- http://www.casperalbers.nl/nl/post/2020-03-11-coronagrafieken/
- https://worktimesheet2014.blogspot.com/2020/03/coronovirus-in-netherlands-power-bi.html (Made with CoronaWatchNL data)
- https://www.youtube.com/watch?v=Kas0tIxDvrg

## License and academic use

The graphs and data are licensed [CC0](https://creativecommons.org/share-your-work/public-domain/cc0/). The original data is copyright RIVM.

For academic use, use presistent data from [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3711575.svg)](https://doi.org/10.5281/zenodo.3711575). This is a persistent copy of the data. Version number refer to the date. Please cite:

```De Bruin, J. (2020). Number of diagnoses with coronavirus disease (COVID-19) in The Netherlands (Version v2020.3.15) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.3711575```

Image from [iXimus](https://pixabay.com/nl/users/iXimus-2352783/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4901881) via [Pixabay](https://pixabay.com/nl/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4901881)

## CoronaWatchNL 

CoronaWatchNL is collective of researchers and volunteers in The Netherlands. We aim to make the reported number on COVID-19 disease in The Netherlands FAIR. 

Help on this project is appreciated. We are looking for new datasets, data updates, graphs and maps. Please report issues in the Issue Tracker. Want to contribute? Please check out the `help wanted` tag in the [Issue Tracker](https://github.com/J535D165/CoronaWatchNL/issues).

Please send an email to jonathandebruinos@gmail.com
