![corona_artwork.jpg](corona_artwork.jpg)

# Dataset: COVID-19 case counts in The Netherlands

**CoronaWatchNL** collects numbers on COVID-19 disease count cases in **The Netherlands**. The numbers are collected from various sources on a daily base, like [RIVM (National Institute for Public Health and the Environment)](https://www.rivm.nl/nieuws/actuele-informatie-over-coronavirus), [LCPS (Landelijk Coördinatiecentrum Patiënten Spreiding)](https://www.lcps.nu/), [NICE (Nationale Intesive Care Evaluatie)](https://www.stichting-nice.nl/), and the [National Corona Dashboard](https://coronadashboard.rijksoverheid.nl/). This project standardizes, and publishes data and makes it **Findable, Accessible, Interoperable, and Reusable (FAIR)**. We aim to collect a complete time series and prepare a dataset for reproducible analysis and academic use.

Dutch:
> CoronalWatchNL verzamelt ziektecijfers over COVID-19 in Nederland. Dagelijks worden de cijfers verzameld van het [RIVM (Rijksinstituut voor de Volksgezondheid en Milieu)](https://www.rivm.nl/nieuws/actuele-informatie-over-coronavirus), [LCPS (Landelijk Coördinatiecentrum Patiënten Spreiding)](https://www.lcps.nu/), [NICE (Nationale Intesive Care Evaluatie)](https://www.stichting-nice.nl/) en [Nationale Corona Dashboard](https://coronadashboard.rijksoverheid.nl/). Dit project standaardiseert en publiceert de gegevens en maakt ze vindbaar, toegankelijk, interoperabel en herbruikbaar (FAIR). We streven ernaar om een dataset beschikbaar te stellen voor reproduceerbare analyses en wetenschappelijk gebruik.


## Datasets
The datasets available on CoronaWatchNL are updated on a daily base. Availability depends on the publication by the respective sources. The CoronaWatchNL project divides the datasets into four main categories:

* [Geographical data](#geographical-datasets)
* [Descriptive data](#descriptive-datasets)
* [Intensive care data](#intensive-care-datasets)
* [Miscellaneous datasets](#miscellaneous-datasets)

For (interactive) applications based on these datasets, have a look at the [applications folder](/applications). For predictive models based on these datasets, check out the parallel repository [CoronaWatchNL Extended](https://github.com/J535D165/CoronaWatchNLExtended). Please note that the intention of these (too) simplistic models - made by CoronaWatchNL volunteers - is to show how the data can be used for modelling,  *not* to answer specific hypotheses or follow scientific protocol.

Please see the [Remarks](REMARKS.md) document for notes about the datasets. Do you have remarks? Please let us know


### Geographical datasets

#### Reference time: 10:00 AM

These datasets describe the new and cumulative number of confirmed, hospitalized and deceased COVID-19 cases. Every day, the data is retrieved from the central database [OSIRIS](https://www.rivm.nl/sniv/handleiding-osiris) at 10:00 AM by RIVM. The datasets are categorized by their geographical level (national, provincial, municipal).

For more detail about the specific structure of the geographical datasets, have a look at the `data-geo`[codebook](/data-geo/README.md). <br/>

| Dataset | Source | Variables |
|---|---| --- |
| [Reported case counts by date in NL](data-geo#national) | RIVM | Date, Type (Total, hopitalized and deceased COVID-19 cases), (Cumulative) Count|
| [Reported case counts by date in NL per province](data-geo#provincial) | RIVM | Date, Province, Type (Total, hopitalized and deceased COVID-19 cases), (Cumulative) Count |
| [Reported case counts by date in NL per municipality](data-geo#municipal) | RIVM | Date, Municipality, Province, Type (Total, hopitalized and deceased COVID-19 cases), (Cumulative) Count |

#### Reference time: by day (0:00 AM)

These datasets describe the new and cumulative number of confirmed, hospitalized and deceased COVID-19 cases per day. The data is retrieved from the central database [OSIRIS](https://www.rivm.nl/sniv/handleiding-osiris) and counts the number per day (0:00 AM) by RIVM. The dataset concerns numbers on a national level.

For more detail about the specific structure of the geographical datasets, have a look at the `data-geo`[codebook](/data-geo/README.md). <br/>

| Dataset | Source | Variables |
|---|---| --- |
| [ Case counts by date in NL ](data/rivm_NL_covid19_national_by_date/) | RIVM | Date, Type (Total, hopitalized and deceased patients), (Cumulative) Count |

#### Visualizations geographical data

To get a better picture of the content of the geographical datasets, have a look at the following visuals. These visuals show the development of the COVID-19 disease outbreak on a national level.

[<img src="plots/overview_plot.png" width="419">](plots)[<img src="plots/overview_plot_diff.png" width="419">](plots)[<img src="plots/overview_plot_true_vs_reported.png" width="419">](plots)[<img src="plots/overview_plot_true_vs_reported_diff.png" width="419">](plots)[<img src="plots/overview_reports.png" width="419">](plots)

[![plots/map_province.png](plots/map_province.png)](plots)


### Descriptive datasets

The datasets in this section describe the new and cumulative number of confirmed, hospitalized and deceased COVID-19 cases per day and contain variables like age and sex.

For more detail about the specific structure of the descriptive datasets, have a look at the `data-desc`[codebook](/data-desc/README.md). <br/>

| Dataset | Source | Variables |
|---|---| --- |
| [Case counts in NL per age](data-desc#age) | RIVM | Date, Age group, Type (Total, hopitalized and deceased COVID-19 cases), (Cumulative) Count |
| [Case counts in NL per sex](data-desc#sex) | RIVM | Date, Sex, Type (Total, hopitalized and deceased COVID-19 cases), (Cumulative) Count|
| [Deceased case counts in NL per sex and age group](data-desc#deceased) | RIVM | Date, Age group, Sex, (Cumulative) Count of deceased cases |


#### Visualizations descriptive data

The graphs below visualize the development of the COVID-19 disease outbreak per sex and age group.

[<img src="plots/overview_plot_geslacht.png" width="419">](plots)[<img src="plots/ratio_plot_geslacht.png" width="419">](plots)[<img src="plots/toename_plot_geslacht.png" width="419">](plots)[<img src="plots/ratio_toename_geslacht.png" width="419">](plots)[<img src="plots/overview_plot_leeftijd_cum.png" width="419">](plots)[<img src="plots/overview_plot_leeftijd.png" width="419">](plots)[<img src="plots/deceased_age_sex.png" width="419">](plots)[<img src="plots/deceased_age_sex_toename.png" width="419">](plots)


### Intensive care datasets

The intensive care datasets describe the new and cumulative number of COVID-19 intensive care unit (ICU) admissions per day. The datasets are categorized by their source. Compared to RIVM (reporting COVID-19 hospital admissions), CoronaWatchNL collects COVID-19 related intensive care data from LCPS and NICE. 

* **RIVM** reports hospitalized COVID-19 cases, including - but not limited to - the intensive care unit (ICU) admissions. These are the largest numbers and most inclusive counts.
* **NICE** only reports COVID-19 cases that are admitted to the ICU.
* **LCPS**, similarly to NICE, reports COVID-19 ICU admissions. However, LCPS tries to compensate for the reporting lag, by estimating its size and adding it to the numbers reported by NICE.


For more detail about the specific structure of the intensive care datasets, have a look at the `data-ic`[codebook](/data-ic/README.md). <br/>

| Dataset | Source | Variables |
| --- | --- | --- |
| [COVID-19 intensive care patient counts in NL ](data-ic#nice) | Stichting NICE | Date, New, Total and Cumulative ICU admissions per day, Number of ICUs with at least one COVID-19 case, New and Cumulative fatal, survived and discharged ICU admissions |
| [COVID-19 intensive care patient counts with country of hospitalisation ](data-ic#lcps) | LCPS | Date, Country of Hospitalization, Total COVID-19 ICU admissions |


#### Visualizations intensive care
The first two graphs show the number of new (*Nieuw*), total (*Actueel*), cumulative (*Cumulatief*), deceased (*Overleden*), and survived (*Overleefd*) COVID-19 ICU admissions per day, as declared by NICE. The total number of ICU admissions per day as reported by LCPS is also shown.

[<img src="plots/ic_nice_intakes.png" width="419">](plots)[<img src="plots/ic_nice_vrijkomst.png" width="419">](plots)[<img src="plots/ic_lcps_intakes.png" width="419">](plots)[<img src="plots/ic_lcps_intakes_country.png" width="419">](plots)[<img src="plots/ic_lcps_nice.png" width="419">](plots)[<img src="plots/overview_IC_data.png" width="419">](plots) [<img src="plots/overview_IC_nieuw.png" width="419">](plots[<img src="plots/overview_IC_actueel.png" width="419">](plots)[<img src="plots/overview_IC_totaal.png" width="419">](plots)


### Miscellaneous datasets

This folder contains datasets describing various topics, such as the number of (positively) tested people, the reproduction index, an estimate of the number of contagious peope, number of (deceased) infected nursery home residents, the underlying conditions and/or pregnancy of deceased cases younger than 70, and on overview of the reinforced measures and press releases in the Netherlands.

For more detail about the specific structure of the miscellaneous datasets, have a look at the `data-misc`[codebook](/data-misc/README.md).

| Dataset | Source | Variables |
|---|---| --- |
| [COVID-19 tests in NL per week](data-misc#test) | RIVM | Year, Calendar week, Start date (Monday), End date (Sunday), Included labs, Type (Total and positive tests), Count |
| [Reproduction index COVID-19 virus](data-misc#reproduction) | National Dashboard | Date, Type of measure, Value |
| [Contagion estimate COVID-19 virus](data-misc#contagious) | National Dashboard | Date, Type of measure, Value |
| [Number of infected and deceased nursery home cases](data-misc#nursery) | National Dashboard | Date, Type of measure, (Cumulative) Count |
| [Underlying conditions and/or pregnancy in deceased COVID-19 cased under the age of 70](data-misc#underlying) | RIVM | Date, Type of condition, Cumulative count |
| [COVID-19 measures by the government](data-misc#measures) | European Commission Joint Research Centre | Various variables on governmental measures (in English) |
| [RIVM press releases](data/rivm_press_releases.csv) | RIVM | Date and Time, Content of press release |


#### Visualizations miscellaneous data

These graphs display the number of (positively) tested people per week. The end date of each week - Sunday - is used as indicator for the respective week.<br/>

[<img src="plots/overview_plot_tests_weeks_cum.png" width="419">](plots)[<img src="plots/overview_plot_tests_weeks.png" width="419">](plots)

The reproduction index, plotted with the corresponding minimum and maximum values, indicates how quickly the COVID-19 virus is spreading in the Netherlands.<br/>

[<img src="plots/reproductie_index.png" width="600">](plots)

The number of (deceased) nursery home residents infected with COVID-19 are shown here. <br/>

[<img src="plots/overview_nursery_count.png" width="419">](plots)[<img src="plots/overview_nursery_cumulative.png" width="419">](plots)

Below, the cumulative number of deceased COVID-19 cases younger than 70 with and without underlying conditions and/or pregnancy are displayed per notification date. <br/>

[<img src="plots/conditions_statistics.png" width="600">](plots)

The cumulative number of specific conditions found in these deceased COVID-19 cases are shown here. <br/>
[<img src="plots/underlying_conditions.png" width="600">](plots)

## Inactive/deprecated datasets

### Deprecated (pending)

The following datasets are awaiting deprecation. They are replaced by new datasets.

| Dataset | URL | Source | Variables | Alternative
|---|---| --- | --- | --- |
| [COVID-19 disease case counts in NL](https://github.com/J535D165/CoronaWatchNL/blob/b71cd70e51bb2e30e8fb9244f360a1e70446c939/data/rivm_corona_in_nl_daily.csv) | RIVM | Date, Number of positive COVID-19 disease cases in NL| rivm_NL_covid19_national.csv | [COVID-19 case counts in NL](data/rivm_NL_covid19_national.csv) |
| [COVID-19 fatalities in NL](https://github.com/J535D165/CoronaWatchNL/blob/b71cd70e51bb2e30e8fb9244f360a1e70446c939/data/rivm_corona_in_nl_fatalities.csv) | RIVM | Date, Number of COVID-19 fatalities in NL | rivm_NL_covid19_national.csv | [COVID-19 case counts in NL](data/rivm_NL_covid19_national.csv) |
| [COVID-19 hospitalizations in NL](https://github.com/J535D165/CoronaWatchNL/blob/b71cd70e51bb2e30e8fb9244f360a1e70446c939/data/rivm_corona_in_nl_hosp.csv) | RIVM | Date, Number of COVID-19 hospitalized patients in NL | rivm_NL_covid19_national.csv | [COVID-19 case counts in NL](data/rivm_NL_covid19_national.csv) |
| [Newly reported relative case counts by date in NL per municipality (PDF maps)\*](data/rivm_NL_covid19_municipality_range.csv) | RIVM | Date, Type, Number of positive COVID-19 disease cases, hospitalizations and fatalities per 100.000 people, Municipality, Province|

**\*** This dataset is extracted from the maps in the PDF's. The values are relative counts per 100.000 residents in the municipality.

### Inactive

The following datasets are no longer appended with new data (because RIVM is no longer providing the data).

| Dataset | URL | Source | Variables | Expire date
|---|---| --- | --- | --- |
| COVID-19 disease case counts in NL\* |[[long format]](https://github.com/J535D165/CoronaWatchNL/blob/b71cd70e51bb2e30e8fb9244f360a1e70446c939/data/rivm_corona_in_nl.csv) [[wide format]](https://github.com/J535D165/CoronaWatchNL/blob/b71cd70e51bb2e30e8fb9244f360a1e70446c939/data/rivm_corona_in_nl_table.csv) | RIVM | Date, Number of positive COVID-19 disease cases in NL, Municipality of residence, Municipality code (2019), Province | 2020-03-30

**\*** Nowadays, the data is published again. Please use dataset [data-geo#municipal](https://github.com/J535D165/CoronaWatchNL/tree/master/data-geo#municipal).

## Raw data

CoronaWatchNL collects copies of the raw data such that data collection is verifiable. Copies of the collected data can be found in the folder [raw_data](raw_data/). The data isn't standardised.


## Data collection sources

The following sources are used for data collection.

| Source | Institute | Variables |
|---|---| --- |
| https://www.rivm.nl/coronavirus-covid-19/actueel | RIVM | National cumulative numbers and press releases |
| https://www.rivm.nl/coronavirus-covid-19/grafieken | RIVM | Case counts per day |
| https://www.rivm.nl/documenten/dagelijkse-update-epidemiologische-situatie-covid-19-in-nederland | RIVM | Epidemiological report |
| https://www.stichting-nice.nl/ | Stichting NICE | Intensive care numbers on COVID-19 patients |
| https://www.lcsp.nu/ | LCPS | Intensive care numbers on COVID-19 patients |
| https://coronadashboard.rijksoverheid.nl/ | National Dashboard | Various variables and estimations like Reproduction Index |
| https://covid-statistics.jrc.ec.europa.eu/ | European Commision Joint Research Centre | Governmental measures database |


## License and academic use

The graphs and data are licensed [CC0](https://creativecommons.org/share-your-work/public-domain/cc0/). The original data is copyright RIVM.

For academic use, use presistent data from [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3711575.svg)](https://doi.org/10.5281/zenodo.3711575). This is a persistent copy of the data. Version number refer to the date. Please cite:

```De Bruin, J. (2020). Number of diagnoses with coronavirus disease (COVID-19) in The Netherlands (Version v2020.3.15) [Data set]. Zenodo. http://doi.org/10.5281/zenodo.3711575```

Image from [iXimus](https://pixabay.com/nl/users/iXimus-2352783/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4901881) via [Pixabay](https://pixabay.com/nl/?utm_source=link-attribution&amp;utm_medium=referral&amp;utm_campaign=image&amp;utm_content=4901881)

## CoronaWatchNL

CoronaWatchNL is collective of researchers and volunteers in The Netherlands. We aim to make the reported number on COVID-19 disease in The Netherlands FAIR. The project is initiated and maintained by [Utrecht University Research Data Management Support](https://www.uu.nl/en/research/research-data-management) and receives support from [Utrecht University Applied Data Science](https://www.uu.nl/en/research/applied-data-science).

Help on this project is appreciated. We are looking for new datasets, data updates, graphs and maps. Please report issues in the Issue Tracker. Want to contribute? Please check out the `help wanted` tag in the [Issue Tracker](https://github.com/J535D165/CoronaWatchNL/issues). Do you wish to share an application based on these [datasets](/data)? Have a look at the [applications folder](/applications). For predictive models, check out the parallel repository [CoronaWatchNL Extended](https://github.com/J535D165/CoronaWatchNLExtended).

Please send an email to jonathandebruinos@gmail.com and/or r.voorvaart@uu.nl
