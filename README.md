![corona_artwork.jpg](corona_artwork.jpg)

# Dataset: COVID-19 case counts in The Netherlands

**CoronaWatchNL** collects COVID-19 disease count cases in **The Netherlands**. Numbers are collected from the RIVM (National Institute for Public Health and the Environment) website on a daily basis. This project standardizes, and publishes data and makes it **Findable, Accessible, Interoperable, and Reusable (FAIR)**. We aim to collect a complete time series and prepare a dataset for reproducible analysis and academic use.

Dutch:
> CoronalWatchNL verzamelt ziektecijfers over COVID-19 in Nederland. Dagelijks worden de cijfers verzameld van de website van het RIVM. Dit project standaardiseert en publiceert de gegevens en maakt ze vindbaar, toegankelijk, interoperabel en herbruikbaar (FAIR). We streven ernaar om een dataset beschikbaar te stellen voor reproduceerbare analyses en wetenschappelijk gebruik.


## Datasets
The datasets available on CoronaWatchNL are updated on a daily base. Availability depends on the publication by RIVM. The datasets are organized into four main categories:

* [Geographical data](#geographical-datasets)
* [Descriptive data](#descriptive-datasets)
* [Intensive care data](#intensive-care-datasets)
* [Miscellaneous datasets](#miscellaneous-datasets)

For (interactive) applications based on these datasets, have a look at the [applications folder](/applications). For predictive models based on these datasets, check out the parallel repository [CoronaWatchNL Extended](https://github.com/J535D165/CoronaWatchNLExtended). Please note that the intention of these (too) simplistic models - made by CoronaWatchNL volunteers - is to show how the data can be used for modelling,  *not* to answer specific hypotheses or follow scientific protocol.


### Geographical datasets

These datasets describe the new and cumulative number of confirmed, hospitalized and deceased COVID-19 cases per day. The datasets are categorized by their geographical level (national, provincial, municipal).

The following datasets contain newly reported cases.

| Dataset | Source | Variables |
|---|---| --- |
| [Newly reported case counts by date in NL\*](data-geo#national) | RIVM | Date, Type (Total, hopitalized and deceased COVID-19 cases), (Cumulative) Count|
| [Newly reported case counts by date in NL per province\*](data-geo#provincial) | RIVM | Date, Province, Type (Total, hopitalized and deceased COVID-19 cases), (Cumulative) Count |
| [Newly reported case counts by date in NL per municipality\*](data-geo#municipal) | RIVM | Date, Municipality, Province, Type (Total, hopitalized and deceased COVID-19 cases), (Cumulative) Count |

**\*** For more detail about the specific structure of the geographical datasets, have a look at the `data-geo`[codebook](/data-geo/README.md). <br/>

The following datasets contain the actual case counts on the given date.

| Dataset | Source | Variables |
|---|---| --- |
| [ Case counts by date in NL ](data/rivm_NL_covid19_national_by_date/) | RIVM | Date, Type (Total, hopitalized and deceased patients), (Cumulative) Count |

#### Visualizations geographical data

To get a better picture of the content of the geographical datasets, have a look at the following visuals. These visuals show the development of the COVID-19 disease outbreak on a national level.

[<img src="plots/overview_plot.png" width="430">](plots) [<img src="plots/overview_plot_diff.png" width="430">](plots) [<img src="plots/overview_plot_true_vs_reported.png" width="430">](plots) [<img src="plots/overview_plot_true_vs_reported_diff.png" width="430">](plots) [<img src="plots/overview_reports.png" width="430">](plots)

[![plots/map_province.png](plots/map_province.png)](plots)


### Descriptive datasets

The datasets in this section describe the new and cumulative number of confirmed, hospitalized and deceased COVID-19 cases per day and contain variables like age and sex.

| Dataset | Source | Variables |
|---|---| --- |
| [Case counts in NL per age\*](data-desc#age) | RIVM | Date, Age group, Type (Total, hopitalized and deceased COVID-19 cases), (Cumulative) Count |
| [Case counts in NL per sex\*](data-desc#sex) | RIVM | Date, Sex, Type (Total, hopitalized and deceased COVID-19 cases), (Cumulative) Count|
| [Deceased case counts in NL per sex and age group\*](data-desc#deceased) | RIVM | Date, Age group, Sex, (Cumulative) Count of deceased cases |

**\*** For more detail about the specific structure of the descriptive datasets, have a look at the `data-desc`[codebook](/data-desc/README.md). <br/>

#### Visualizations descriptive data

The graphs below visualize the development of the COVID-19 disease outbreak per sex and age group.

[<img src="plots/overview_plot_geslacht.png" width="430">](plots)[<img src="plots/ratio_plot_geslacht.png" width="430">](plots)[<img src="plots/toename_plot_geslacht.png" width="430">](plots)[<img src="plots/ratio_toename_geslacht.png" width="430">](plots)[<img src="plots/overview_plot_leeftijd_cum.png" width="430">](plots)[<img src="plots/overview_plot_leeftijd.png" width="430">](plots)[<img src="plots/deceased_age_sex.png" width="430">](plots)[<img src="plots/deceased_age_sex_toename.png" width="430">](plots)


### Intensive care datasets

The intensive care datasets describe the new and cumulative number of COVID-19 intensive care unit (ICU) admissions per day. The datasets are categorized by their source.

| Dataset | Source | Variables |
| --- | --- | --- |
| [COVID-19 intensive care patient counts in NL ](data-ic#nice) | Stichting NICE | Date, New, Total and Cumulative ICU admissions per day, Number of ICUs with at least one COVID-19 case, New and Cumulative fatal, survived and discharged ICU admissions |
| [COVID-19 intensive care patient counts with country of hospitalisation ](data-ic#lcps) | LCPS | Date, Country of Hospitalization, Total COVID-19 ICU admissions |

**\*** For more detail about the specific structure of the intensive care datasets, have a look at the `data-ic`[codebook](/data-ic/README.md). <br/>

#### Visualizations intensive care
The first two graphs show the number of new (*Nieuw*), total (*Actueel*), cumulative (*Cumulatief*), deceased (*Overleden*), and survived (*Overleefd*) COVID-19 ICU admissions per day, as declared by NICE. The total number of ICU admissions per day as reported by LCPS is also shown.

[<img src="plots/ic_nice_intakes.png" width="430">](plots) [<img src="plots/ic_nice_vrijkomst.png" width="430">](plots) [<img src="plots/ic_lcps_intakes.png" width="430">](plots) [<img src="plots/ic_lcps_intakes_country.png" width="430">](plots) [<img src="plots/ic_lcps_nice.png" width="430">](plots)


#### Intensive care: RIVM, LCPS, NICE
CoronaWatchNL reports COVID-19 related hospital data of three different sources: RIVM, LCPS and NICE.

* **RIVM** reports hospitalized COVID-19 cases, including - but not limited to - the intensive care unit (ICU) admissions. These are the highest and most inclusive counts.
* **NICE** only reports COVID-19 cases that are admitted to the ICU.
* **LCPS**, similarly to NICE, reports COVID-19 ICU admissions. However, LCPS tries to compensate for the reporting lag, by estimating its size and adding it to the numbers reported by NICE. These estimates are not corrected, resulting in consistently higher counts compared to NICE.

[<img src="plots/overview_IC_data.png" width="430">](plots) [<img src="plots/overview_IC_nieuw.png" width="430">](plots) [<img src="plots/overview_IC_actueel.png" width="430">](plots) [<img src="plots/overview_IC_totaal.png" width="430">](plots)


### Miscellaneous datasets

This folder contains datasets describing various topics, such as the number of (positively) tested people, the reproduction index, an estimate of the number of contagious peope, number of (deceased) infected nursery home residents, the underlying conditions and/or pregnancy of deceased cases younger than 70, and on overview of the reinforced measures and press releases in the Netherlands.

| Dataset | Source | Variables |
|---|---| --- |
| [COVID-19 tests in NL per week\*](data-misc#test) | RIVM | Year, Calendar week, Start date (Monday), End date (Sunday), Included labs, Type (Total and positive tests), Count |
| [Reproduction index COVID-19 virus\*](data-misc#reproduction) | RIVM | Date, Type of measure, Value |
| [Contagion estimate COVID-19 virus\*](data-misc#contagious) | RIVM | Date, Type of measure, Value |
| [Number of infected and deceased nursery home cases\*](data-misc#nursery) | RIVM | Date, Type of measure, (Cumulative) Count |
| [Underlying conditions and/or pregnancy in deceased COVID-19 cased under the age of 70\*](data-misc#underlying) | RIVM | Date, Type of condition, Cumulative count |
| [COVID-19 measures by the government (NEW)\*](data-misc#measures) | European Commission Joint Research Centre | Various variables on governmental measures (in English) |
| [RIVM press releases\*](data/rivm_press_releases.csv) | RIVM | Date and Time, Content of press release |

**\*** For more detail about the specific structure of the miscellaneous datasets, have a look at the `data-misc`[codebook](/data-misc/README.md). <br/>

#### Visualizations miscellaneous data

These graphs display the number of (positively) tested people per week. The end date of each week - Sunday - is used as indicator for the respective week.<br/>

[<img src="plots/overview_plot_tests_weeks_cum.png" width="430">](plots)[<img src="plots/overview_plot_tests_weeks.png" width="430">](plots)

The reproduction index, plotted with the corresponding minimum and maximum values, indicates how quickly the COVID-19 virus is spreading in the Netherlands.<br/>

[<img src="plots/reproductie_index.png" width="600">](plots)

The number of (deceased) nursery home residents infected with COVID-19 are shown here. <br/>

[<img src="plots/overview_nursery_count.png" width="430">](plots) [<img src="plots/overview_nursery_cumulative.png" width="430">](plots)

Below, the cumulative number of deceased COVID-19 cases younger than 70 with and without underlying conditions and/or pregnancy are displayed per notification date. <br/>

[<img src="plots/conditions_statistics.png" width="600">](plots)

The cumulative number of specific conditions found in these deceased COVID-19 cases are shown here. <br/>
[<img src="plots/underlying_conditions.png" width="600">](plots)

## Inactive/deprecated datasets

### Deprecated (pending)

The following datasets are awaiting deprecation. They are replaced by new datasets.

| Dataset | URL | Source | Variables | Alternative
|---|---| --- | --- | --- |
| [COVID-19 disease case counts in NL](data/rivm_corona_in_nl_daily.csv) | RIVM | Date, Number of positive COVID-19 disease cases in NL| rivm_NL_covid19_national.csv | [COVID-19 case counts in NL](data/rivm_NL_covid19_national.csv) |
| [COVID-19 fatalities in NL](data/rivm_corona_in_nl_fatalities.csv) | RIVM | Date, Number of COVID-19 fatalities in NL | rivm_NL_covid19_national.csv | [COVID-19 case counts in NL](data/rivm_NL_covid19_national.csv) |
| [COVID-19 hospitalizations in NL](data/rivm_corona_in_nl_hosp.csv) | RIVM | Date, Number of COVID-19 hospitalized patients in NL | rivm_NL_covid19_national.csv | [COVID-19 case counts in NL](data/rivm_NL_covid19_national.csv) |
| [Newly reported relative case counts by date in NL per municipality (PDF maps)\*](data/rivm_NL_covid19_municipality_range.csv) | RIVM | Date, Type, Number of positive COVID-19 disease cases, hospitalizations and fatalities per 100.000 people, Municipality, Province|

**\*** This dataset is extracted from the maps in the PDF's. The values are relative counts per 100.000 residents in the municipality.

### Inactive

The following datasets are no longer appended with new data (because RIVM is no longer providing the data).

| Dataset | URL | Source | Variables | Expire date
|---|---| --- | --- | --- |
| COVID-19 disease case counts in NL\* |[[long format]](data/rivm_corona_in_nl.csv) [[wide format]](data/rivm_corona_in_nl_table.csv) | RIVM | Date, Number of positive COVID-19 disease cases in NL, Municipality of residence, Municipality code (2019), Province | 2020-03-30

**\*** Nowadays, the data is published again. Please use dataset [data-geo#municipal](https://github.com/J535D165/CoronaWatchNL/tree/master/data-geo#municipal).

## Raw data

CoronaWatchNL collects copies of the raw data such that data collection is verifiable. Copies of the collected data can be found in the folder [raw_data](raw_data/). The data isn't standardised.


## Data collection sources

The following sources are used for data collection.

| Source | Institute |Collected variables |
|---|---| --- |
| https://www.rivm.nl/nieuws/actuele-informatie-over-coronavirus | RIVM | Total, hopitalized and deceased COVID-19 cases |
| https://www.rivm.nl/coronavirus-kaart-van-nederland-per-gemeente | RIVM | Positive tests per municipality |
| https://www.rivm.nl/nieuws/actuele-informatie-over-coronavirus/data | RIVM | Epidemiological reports |
| https://www.stichting-nice.nl/ | Stichting NICE | New, total, cumulative number of COVID-19 ICU admissions, Number of ICUs with positively tested patient(s), Number of fatal, survived and discharged ICU admissions |

## Remarks

Please see the [Remarks](REMARKS.md) document for notes about the datasets. Do you have remarks? Please let us know.


## License and academic use

The graphs and data are licensed [CC0](https://creativecommons.org/share-your-work/public-domain/cc0/). The original data is copyright RIVM.

For academic use, use presistent data from [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3711575.svg)](https://doi.org/10.5281/zenodo.3711575). This is a persistent copy of the data. Version number refer to the date. Please cite:

```De Bruin, J. (2020). Number of diagnoses with coronavirus disease (COVID-19) in The Netherlands (Version v2020.3.15) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.3711575```

Image from [iXimus](https://pixabay.com/nl/users/iXimus-2352783/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4901881) via [Pixabay](https://pixabay.com/nl/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4901881)

## CoronaWatchNL

CoronaWatchNL is collective of researchers and volunteers in The Netherlands. We aim to make the reported number on COVID-19 disease in The Netherlands FAIR. The project is initiated and maintained by [Utrecht University Research Data Management Support](https://www.uu.nl/en/research/research-data-management) and receives support from [Utrecht University Applied Data Science](https://www.uu.nl/en/research/applied-data-science).

Help on this project is appreciated. We are looking for new datasets, data updates, graphs and maps. Please report issues in the Issue Tracker. Want to contribute? Please check out the `help wanted` tag in the [Issue Tracker](https://github.com/J535D165/CoronaWatchNL/issues). Do you wish to share an application based on these [datasets](/data)? Have a look at the [applications folder](/applications). For predictive models, check out the parallel repository [CoronaWatchNL Extended](https://github.com/J535D165/CoronaWatchNLExtended).

Please send an email to jonathandebruinos@gmail.com and/or r.voorvaart@uu.nl
