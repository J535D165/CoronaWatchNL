# Codebook `data-misc` - CoronaWatchNL

## Data update

All datasets are updated on a daily base. Availability depends on the publication by RIVM.

## Data format

### Test data (virologische dagstaten)

Number of persons tested and number of persons tested positively on SARS-CoV-2 in
the Netherlands, reported by laboratories per week.

> Om zicht te houden op het aantal geteste personen en het aantal positief geteste personen
op het SARS-CoV-2 virus in Nederland, is alle laboratoria in Nederland die diagnostiek voor
SARS-CoV-2 uitvoeren gevraagd om vanaf 9 maart deze data dagelijks te melden. De laboratoria
rapporteren op maandag voor 12 uur over de voorgaande week. Het aantal personen met een
positieve uitslag wijkt af van het aantal patiënten gemeld door GGD’en omdat sommige personen
mogelijk vaker getest worden en omdat positieve laboratorium uitslagen sneller gerapporteerd
kunnen worden. (reports/COVID-19_epidemiological_report_20201027.pdf, Table 15)

**Directory:** [data-misc/data-test](data-test) <br>
**Daily file format:** RIVM_NL_test_yyyy-mm-dd.csv<br>
**Latest file format:** [RIVM_NL_test_latest.csv](data-test/RIVM_NL_test_latest.csv)<br>
**Deprecated file(s):** [RIVM_NL_test_depr_2020-04-20.csv](data-test/RIVM_NL_test_depr_2020-04-20.csv)<br>

| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Jaar** | Year | Year of notification | YYYY (ISO 8601) | 2020 |
| **Week** | Week number\* | Week of notification | numeric | 11 |
| **BeginDatum** | Start date | Beginning of the week (Monday) of notification | YYYY-MM-DD (ISO 8601) | 2020-03-09 |
| **EindDatum** | End date | End of the week (Sunday) of notification | YYYY-MM-DD (ISO 8601) | 2020-03-15 |
| **Bron**                        | Source                   | The id of the report [(See report metadata)](/reports/reports_metadata.csv)                 | RIVM_report_YYYYMMDD | RIVM_report_20200327 |
| **AantalLaboratoria** | Number of laboratories | Number of Dutch laboratories that have performed diagnostics for SARS-CoV-2 in said week | character | 30 |
| **Type** | Type | Type of test measurement (i.e., Totaal, Positief) | character | Totaal |
| **Aantal** | Count | Number of people tested for COVID-19 (*Totaal*), and number of positively tested people for COVID-19 (*Positief*\*\*) per week | numeric (integer) | 17080|

**\*** Before the 21st of April, RIVM reports did not use weeks but seperate dates to report test counts. This format can be found in the [RIVM_NL_test_depr_2020-04-20.csv](data-test/RIVM_NL_test_depr_2020-04-20.csv) dataset. Note that, due to this change in format, this specific file could not be updated after the 20th of April.<br/>
**\*\*** The number of people positively tested on COVID-19 differs from the number of patients reported by the GGDs, as some people might have been tested more than once. <br/>

### Test data (GGD GHOR)

Number of persons tested by GGD organizations.

Source: https://ggdghor.nl/actueel-bericht/weekupdate-cijfers-coronatests-bij-de-ggden-2/

**Directory:** [data-misc/data-test-ggd-ghor](data-test-ggd-ghor) <br>
**Daily file format:** RIVM_NL_test_ggd_ghor_yyyy-mm-dd.csv<br>
**Latest file format:** [RIVM_NL_test_ggd_ghor_latest.csv](data-test-ggd-ghor/RIVM_NL_test_ggd_ghor_latest.csv)<br>

| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Jaar** | Year | Year of notification | YYYY (ISO 8601) | 2020 |
| **Week** | Week number | Week of notification | numeric | 11 |
| **BeginDatum** | Start date | Beginning of the week (Monday) of notification | YYYY-MM-DD (ISO 8601) | 2020-03-09 |
| **EindDatum** | End date | End of the week (Sunday) of notification | YYYY-MM-DD (ISO 8601) | 2020-03-15 |
| **Bron**                        | Source                   | URL to GGD website | URL | https://ggdghor.nl/actueel-bericht/weekupdate-cijfers-coronatests-bij-de-ggden-2/ |
| **Type** | Type | Type of test measurement (i.e., Totaal, Positief) | character | Totaal |
| **Aantal** | Count | Number of people tested for COVID-19 (*Totaal*) per week\*\* | numeric (integer) | 17080|

**\*\*** These numbers relate to the persons tested by the GGDs. In addition, tests are also carried out by others (including GPs and hospitals).

### Underlying

For deceased COVID-19 cases younger than 70, RIVM reported whether or not they suffered from underlying conditions and/or were pregnant. The number of deceased patients with and without underlying disorders and/or pregnancy are listed in [data-underlying_statistics](#underlying-statistics). The number of detected underlying conditions and/or pregnancies can be found in [data-underlying_conditions](#underlying-conditions).

#### Underlying statistics

**Directory:** [data-misc/data-underlying/data-underlying_statistics](data-underlying/data-underlying_statistics) <br>
**Daily file format:** RIVM_NL_deceased_under70_statistics_yyyy-mm-dd.csv<br>
**Latest file format:** [RIVM_NL_deceased_under70_statistics_latest.csv](data-underlying/data-underlying_statistics/RIVM_NL_deceased_under70_statistics_latest.csv)<br>
**Complete file format:** [RIVM_NL_deceased_under70_statistics.csv](data-underlying/data-underlying_statistics/RIVM_NL_deceased_under70_statistics.csv)<br>

| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date | Date of notification | YYYY-MM-DD (ISO 8601) | 2020-04-11 |
| **Type** | Type | Type of test measurement (i.e., Totaal gemeld, Onderliggende aandoeningen en/of zwangerschap, Geen onderliggende aandoening, Niet vermeld) | character | Onderliggende aandoening en/of zwangerschap |
| **AantalCumulatief** | Cumulative count | The cumulative number of deceased COVID-19 cases younger than 70 (*Totaal gemeld*) with (*Onderliggende aandoening en/of zwangerschap*) or without (*Geen onderliggende aandoening*) an underlying condition and/or pregnancy, and the cumulative count of cases where it was unknown whether they had an underlying condition and/or were pregnant (*Niet vermeld*) | numeric (integer) | 218 |

#### Underlying conditions

**Directory:** [data-misc/data-underlying/data-underlying_conditions](data-underlying/data-underlying_conditions) <br>
**Daily file format:** RIVM_NL_deceased_under70_conditions_yyyy-mm-dd.csv<br>
**Latest file format:** [RIVM_NL_deceased_under70_conditions_latest.csv](data-underlying/data-underlying_conditions/RIVM_NL_deceased_under70_conditions_latest.csv)<br>
**Complete file format:** [RIVM_NL_deceased_under70_conditions.csv](data-underlying/data-underlying_conditions/RIVM_NL_deceased_under70_conditions.csv)<br>

| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date | Date of notification | YYYY-MM-DD (ISO 8601) | 2020-04-11 |
| **Type** | Type | Type of test measurement (i.e., Zwangerschap, Cardio-vasculaire aandoeningen en hypertensie, Diabetes, Leveraandoening, Chronische neurologische of neuromusculaire aandoeningen, Immuundeficientie, Nieraandoening, Chronische longaandoeningen, Maligniteit, Overig) | character | Nieraandoening |
| **AantalCumulatief\*** | Cumulative count | The cumulative number of deceased COVID-19 cases younger than 70 that suffered from cardio vascular conditions and hypertension (*Cardio-vasculaire aandoeningen en hypertensie*), Dementia/Alzheimer, Diabetes, Liver condition (*Leveraandoening*), Chronic neurological or neuromuscular conditions (*Chronische neurologische of neuromusculaire aandoeningen*), Obesitas, Parkinson, Immunodeficiency (*Immuundeficientie*), Kidney conditions (*Nieraandoening*), Chronic lung conditions (*Chronische longaandoeningen*), Malignancy (*Magligniteit*), or other conditions (*Overig*), or that were pregnant (*Zwangerschap*) | numeric (integer) | 12 |

**\*** Note that one patient can have multiple conditions. Therefore, the sum of the cumulatives per condition is higher than the cumulative number of deceased patients with a known underlying condition and/or pregnancy as mentioned in [data-underlying_statistics](#underlying-statistics).

### Measures

**Directory:** [data-misc/data-measures](data-measures) <br>
**Daily file format:** [NLD_measures.csv](data-measures/NLD_measures.csv) <br>
**Latest file format:** [NLD_measures_latest.csv](data-measures/NLD_measures_latest.csv)<br>

| Column name | Description | Format | Example |
|---|---|---|---|
| **measureID** | Measure ID | numeric | 1 |
| **measureDescription** | Description of the enforced measure | character | Schools/Univ. closure |
| **lastMeasureUpdate** | Date on which the measure was last updated | YYYY-MM-DD (ISO 8601) |  	2020-03-23 |
| **area** | The area in which the measure is/was enforced | character | National |
| **status** | Restriction status of the enforced measure (i.e., 'events' can be: Closed, Partially closed, Partially banned, Banned, or Partially cancelled) | character | Closed |
| **restrictiveMeasures** | Adherence level of the measure (i.e., measure can be: Recommended or Mandatory)  | numeric (integer) | Mandatory|
| **startDate** | Date on which the measure was first enforced | YYYY-MM-DD (ISO 8601) | 2020-03-16|
| **endDate** | Date on which the measure was no longer enforced | YYYY-MM-DD (ISO 8601) | 2020-04-06 |
| **notes** | Notes about the measure | character string | Child care facilities open only for childrens of parents working in crucial departments (doctors, police etc...). Restriction valid until April 6th|

### Economy

**Directory:** [data-misc/data-economy](data-misc/data-economy) <br>
**Complete file format:** [now-registry-20200710.csv](data-economy/now-registry-20200710.csv)<br>

| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Bedrijfsnaam** | Company name | Name of company requesting financial support\*| character | Betonvereniging |
| **Vestigingsplaats** | Location | Location of company | character | Gouda |
| **Uitbetaald voorschotbedrag** | Paid amount| The advance paid to the company in euros | numeric (integer) | 123492 |

**\*** The NOW register, published by UWV, mentions the companies that requested and received an advance on the reimbursement.
