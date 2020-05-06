# Codebook `data-geo` - CoronaWatchNL

## Data update

All datasets are updated on a daily base. Availability depends on the publication by RIVM.

## Data format

### National

**Directory:** [data-geo/data-national](data-national) <br>
**Daily file format:** RIVM_NL_national_yyyy-mm-dd.csv<br>
**Latest file format:** [RIVM_NL_national_latest.csv](data-national/RIVM_NL_national_latest.csv)<br>
**Complete file format:** [RIVM_NL_national.csv](data-national/RIVM_NL_national.csv)

| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date | Date of notification | YYYY-MM-DD (ISO 8601) | 2020-04-23 |
| **Type** | Type | Type of measurement (i.e., Totaal, Ziekenhuisopname, Overleden) | character | Totaal |
| **Aantal** | Count | Number of diagnosed (*Totaal*\*), hospitalized (*Ziekenhuisopname*\*\*), or deceased (*Overleden*\*\*) cases on the date of notification in the last 24 hours | numeric (integer) | 86|
| **AantalCumulatief** | Total count | Number of newly diagnosed (*Totaal*), hospitalized (*Ziekenhuisopname*), or deceased (*Overleden*) cases on the date of notification since the start of the outbreak | numeric (integer) | 86 |

**\*** 'Totaal' numbers are based on the reported cases with confirmed COVID-19 infection at the GGDs (Public Health Services). <br/>
**\*\*** The 'Totaal' and 'Overleden' numbers of COVID-19 cases are actually higher than displayed, as not all people with COVID-19 symptoms are being tested. The actual 'Ziekenhuisopname' numbers of COVID-19 cases are also higher, as these numbers are based on the information available on the moment of notification. Hospitalizations after notifications are not always known. <br/>


### Provincial

**Directory:** [data-geo/data-provincial](data-provincial) <br>
**Daily file format:** RIVM_NL_provincial_yyyy-mm-dd.csv<br>
**Latest file format:** [RIVM_NL_provincial_latest.csv](data-provincial/RIVM_NL_provincial_latest.csv)<br>
**Complete file format:** [RIVM_NL_provincial.csv](data-provincial/RIVM_NL_provincial.csv)


| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date | Date of notification | YYYY-MM-DD (ISO 8601) | 2020-04-23 |
| **Provincienaam** | Province name\* | Corresponding province of municipality | character | Noord-Brabant |
| **Provinciecode** | Province code | Corresponding code of province | character | Noord-Brabant |
| **Type** | Type | Type of measurement (i.e., Totaal, Ziekenhuisopname, Overleden) | character | Totaal |
| **Aantal** | Count | Number of diagnosed (*Totaal*\*\*), hospitalized (*Ziekenhuisopname*\*\*\*), or deceased (*Overleden*\*\*\*) cases per province on the date of notification in the last 24 hours | numeric (integer) | 86|
| **AantalCumulatief** | Total count | Number of newly diagnosed (*Totaal*), hospitalized (*Ziekenhuisopname*), or deceased (*Overleden*) cases per province on the date of notification since the start of the outbreak | numeric (integer) | 86 |

**\*** Some rows do not have a Province name, these are the number of patients with an unknown municipality of residence. <br/>
**\*\*** 'Totaal' numbers are based on the reported cases with confirmed COVID-19 infection at the GGDs (Public Health Services). <br/>
**\*\*\*** The 'Totaal' and 'Overleden' numbers of COVID-19 cases are actually higher than displayed, as not all people with COVID-19 symptoms are being tested. The actual 'Ziekenhuisopname' numbers of COVID-19 cases are also higher, as these numbers are based on the information available on the moment of notification. Hospitalizations after notifications are not always known. <br/>



### Municipal

**Directory:** [data-geo/data-municipal](data-municipal) <br>
**Daily file format:** RIVM_NL_municipal_yyyy-mm-dd.csv<br>
**Latest file format:** [RIVM_NL_municipal_latest.csv](data-municipal/RIVM_NL_municipal_latest.csv)<br>
**Complete file format:** [RIVM_NL_municipal.csv](data-municipal/RIVM_NL_municipal.csv)


| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date | Date of notification | YYYY-MM-DD (ISO 8601) | 2020-04-23 |
| **Gemeentenaam** | Municipality name | Municipality | character | Oosterhout |
| **Gemeentecode** | Municipality code | Corresponding code of municipality | numeric | 826 |
| **Provincienaam** | Province name | Corresponding province of municipality | character | Noord-Brabant |
| **Provinciecode** | Province code | Corresponding code of province | character | Noord-Brabant |
| **Type** | Type | Type of measurement (i.e., Totaal, Ziekenhuisopname, Overleden) | character | Totaal |
| **Aantal** | Count | Number of diagnosed (*Totaal*\*), hospitalized (*Ziekenhuisopname*\*\*), or deceased (*Overleden*\*\*) cases per municipality on the date of notification in the last 24 hours | numeric (integer) | 86|
| **AantalCumulatief** | Total count | Number of newly diagnosed (*Totaal*), hospitalized (*Ziekenhuisopname*), or deceased (*Overleden*) cases per municipality on the date of notification since the start of the outbreak | numeric (integer) | 86 |

**\*** 'Totaal' numbers are based on the reported cases with confirmed COVID-19 infection at the GGDs (Public Health Services). <br/>
**\*\*** The 'Totaal' and 'Overleden' numbers of COVID-19 cases are actually higher than displayed, as not all people with COVID-19 symptoms are being tested. The actual 'Ziekenhuisopname' numbers of COVID-19 cases are also higher, as these numbers are based on the information available on the moment of notification. Hospitalizations after notifications are not always known. <br/>


