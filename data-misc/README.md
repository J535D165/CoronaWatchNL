# Codebook `data-misc` - CoronaWatchNL

## Data update

All datasets are updated on a daily base. Availability depends on the publication by RIVM.

## Data format

### Test

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
| **AantalLaboratoria** | Number of laboratories | Number of Dutch laboratories that have performed diagnostics for SARS-CoV-2 in said week | character | 30 |
| **Type** | Type | Type of test measurement (i.e., Totaal, Positief) | character | Totaal |
| **Aantal** | Count | Number of people tested for COVID-19 (*Totaal*), and number of positively tested people for COVID-19 (*Positief*\*\*) per week\*\*\* | numeric (integer) | 17080|

**\*** Before the 21st of April, RIVM reports did not use weeks but seperate dates to report test counts. This format can be found in the [RIVM_NL_test_depr_2020-04-20.csv](data-test/RIVM_NL_test_depr_2020-04-20.csv) dataset. Note that, due to this change in format, this specific file could not be updated after the 20th of April.<br/>
**\*\*** The number of people positively tested on COVID-19 differs from the number of patients reported by the GGDs, as some people might have been tested more than once. <br/>
**\*\*\*** The data is updated every day, except for weekends and holidays. <br/>


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
