# Codebook `data-dashboard` - CoronaWatchNL

## Data update

All datasets are updated on a daily base. Availability depends on the publication by RIVM.

## Data format

### Cases

**Directory:** [data-dashboard/data-cases](data-cases) <br>
**Daily file format:** RIVM_NL_national_dashboard_yyyy-mm-dd.csv<br>
**Latest file format:** [RIVM_NL_national_dashboard_latest.csv](data-cases/RIVM_NL_national_dashboard_latest.csv)<br>
**Complete file format:** [RIVM_NL_national_dashboard.csv](data-cases/RIVM_NL_national_dashboard.csv)<br>

| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date | Date of notification | YYYY-MM-DD (ISO 8601) | 2020-05-09 |
| **Type** | Type | Type of measurement (i.e., Totaal, Ziekenhuisopname) | character | Totaal |
| **Aantal** | Count | Number of newly diagnosed (*Totaal*) and hospitalized (*Ziekenhuisopname*) cases as reported by the national dashboard on the date of notification | numeric (integer) | 289|
| **AantalCumulatief** | Total count | Number of diagnosed (*Totaal*) and hospitalized (*Ziekenhuisopname*) cases as reported by the national dashboard on the date of notification since the start of the outbreak | numeric (integer) | 42402 |

### Contagious

#### Estimates
**Directory:** [data-dashboard/data-contagious/data-contagious_estimates](data-contagious/data-contagious_estimates) <br>
**Daily file format:** RIVM_NL_contagious_estimate_yyyy-mm-dd.csv<br>
**Complete file format:** [RIVM_NL_contagious_estimate.csv](data-contagious/data-contagious_estimates/RIVM_NL_contagious_estimate.csv)<br>
**Latest file format:** [RIVM_NL_contagious_estimate_latest.csv](data-contagious/data-contagious_estimates/RIVM_NL_contagious_estimate_latest.csv)<br>

| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date | Date of notification | YYYY-MM-DD (ISO 8601) | 2020-05-29 |
| **Type** | Type | Type of measure (i.e., Geschat aantal besmettelijke mensen, Minimum aantal besmettelijke mensen, Maximum aantal besmettelijke mensen) | character | Geschat aantal besmettelijke mensen |
| **Waarde** | Value\* | The (minimum and maximum) estimate of contagious people per 100.000 inhabitants per week | numeric | 9.9 |

**\*** This calculated value estimates how many people infected with COVID-19 per 100.000 inhabitants are contagious for others. This value is calculated by RIVM on a weekly basis.

#### Count
**Directory:** [data-dashboard/data-contagious/data-contagious_count](data-contagious/data-contagious_count) <br>
**Daily file format:** RIVM_NL_contagious_count_yyyy-mm-dd.csv<br>
**Complete file format:** [RIVM_NL_contagious_count.csv](data-contagious/data-contagious_count/RIVM_NL_contagious_count.csv)<br>
**Latest file format:** [RIVM_NL_contagious_count_latest.csv](data-contagious/data-contagious_count/RIVM_NL_contagious_count_latest.csv)<br>

| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date | Date of notification| YYYY-MM-DD (ISO 8601) | 2020-07-10 |
| **Type** | Type | Type of measure (i.e., Geschat aantal besmettelijke mensen) | character | Geschat aantal besmettelijke mensen |
| **Waarde** | Value\* | The estimated number of contagious people per week | numeric | 2726 |

**\*** This calculated value estimates how many people infected with COVID-19 are contagious for others. This value is calculated by RIVM on a weekly basis.

### Descriptive

**Directory:** [data-dashboard/data-descriptive](data-descriptive) <br>
**Daily file format:** RIVM_NL_age_distribution_yyyy-mm-dd.csv<br>
**Complete file format:** [RIVM_NL_age_distribution.csv](data-descriptive/RIVM_NL_age_distribution.csv)<br>
**Latest file format:** [RIVM_NL_age_distribution_latest.csv](data-descriptive/RIVM_NL_age_distribution_latest.csv)<br>

| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date | Date of notification | YYYY-MM-DD (ISO 8601) | 2020-07-21 |
| **LeeftijdGroep** | Age group | Age group (i.e., 0-20, 20-40, 40-60, 60-80, 80+, Unknown) | character | 20 tot 40 |
| **Aantal** | Aantal | The number of positively tested patients per age group on the date of notificiation | numeric | 70 |

### Nursery

#### Residents
**Directory:** [data-dashboard/data-nursery/data-nursery_residents](data-nursery/data-nursery_residents) <br>
**Complete file format:** [RIVM_NL_nursery_residents.csv](data-nursery/data-nursery_residents/RIVM_NL_nursery_residents.csv)<br>

| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date | Date of notification | YYYY-MM-DD (ISO 8601) | 2020-04-11 |
| **Type** | Type | Type of measurment: Positief geteste bewoners (*Positively tested residents*), Overleden besmette bewoners (*Deceased residents*) | character | Positief geteste bewoners |
| **Aantal** | Count | Number of newly reported (deceased) COVID-19 cases of nursery home residents on the date of notification | numeric (integer) | 160 |
| **AantalCumulatief** | Total count | Number of (deceased) COVID-19 cases of nursery home residents on the date of notification since the start of the outbreak | numeric (integer) | 4017 |

#### Homes
**Directory:** [data-dashboard/data-nursery/data-nursery_homes](data-nursery/data-nursery_homes) <br>
**Complete file format:** [RIVM_NL_nursery_counts.csv](data-nursery/data-nursery_homes/RIVM_NL_nursery_counts.csv)<br>

| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date | Date of notification | YYYY-MM-DD (ISO 8601) | 2020-04-11 |
| **Type** | Type | Type of measurment (i.e., Besmette verpleeghuizen) | character | Besmette verpleeghuizen |
| **NieuwAantal** | New count | Number of newly reported nursery homes with at least one COVID-19 infected resident on the date of notification | numeric (integer) | 9 |
| **Aantal** | Total count | Total number of reported nursery homes with at least one COVID-19 infected resident on the date of notification | numeric (integer) | 828 |

### Reproduction

**Directory:** [data-dashboard/data-reproduction](data-reproduction) <br>
**Complete file format:** [RIVM_NL_reproduction_index.csv](data-reproduction/RIVM_NL_reproduction_index.csv)<br>

| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date\* | Date of calculated reproduction index | YYYY-MM-DD (ISO 8601) | 2020-04-11 |
| **Type** | Type | Type of reproduction measure (i.e., Reproductie index, Minimum, Maximum) | character | Reproductie index |
| **Waarde** | Value\*\* | The (minimum and maximum) reproduction index (*Reproductie index*) per day, indicating how quickly the virus is spreading | numeric | 0.69 |

**\*** As the reproduction index is calculated in retrospect, the reproduction index for the most recent dates are, therefore, still unknown. <br/>
**\*\*** The reproduction index is an estimate made by RIVM based on various data sources. The exact number is unknown. The reproduction index is an average for the entire Netherlands.

### Sewage

**Directory:** [data-dashboard/data-sewage](data-sewage) <br>
**Complete file format:** [RIVM_NL_sewage_counts.csv](data-sewage/RIVM_NL_sewage_counts.csv)<br>

| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date | Date of notification | YYYY-MM-DD (ISO 8601) | 2020-07-06 |
| **Type** | Type | Type of measurement (i.e., Virusdeeltjes per ml rioolwater) | character | Virusdeeltjes per ml rioolwater |
| **Aantal** | Count\* | The number of virus particles measured in one mililiter sewage water per week | numeric | 3.25 |

**\*** Once per week the number of virus particles per mililiter sewage water, obtained at 28 location in the Netherlands, is determined.

### Suspects

**Directory:** [data-dashboard/data-suspects](data-suspects) <br>
**Complete file format:** [RIVM_NL_suspects.csv](data-suspects/RIVM_NL_suspects.csv)<br>

| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date | Date of notification | YYYY-MM-DD (ISO 8601) | 2020-07-05 |
| **Type** | Type | Type of measurement (i.e., Verdachte patiënten) | character | Verdachte patiënten |
| **Aantal** | Count | The number of GP registered *suspected* COVID-19 cases per 100.000 inhabitants per week | numeric | 11.0 |
