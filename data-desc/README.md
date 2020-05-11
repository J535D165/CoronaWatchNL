# Codebook `data-desc` - CoronaWatchNL

## Data update

All datasets are updated on a daily base. Availability depends on the publication by RIVM.

## Data format

### Sex

**Directory:** [data-desc/data-sex](data-sex) <br>
**Daily file format:** RIVM_NL_sex_yyyy-mm-dd.csv<br>
**Latest file format:** [RIVM_NL_sex_latest.csv](data-sex/RIVM_NL_sex_latest.csv)<br>
**Complete file format:** [RIVM_NL_sex.csv](data-sex/RIVM_NL_sex.csv)

| Column name                  | Translation                       | Description                       | Format                            | Example                       | 
|-----------------------------|-----------------------------------|-----------------------------------|----------------------------------------|-------------------------------|
| **Datum**                        | Date                   | Date of notification                   | YYYY-MM-DD (ISO 8601) | 2020-03-27 |
| **Geslacht**                       | Sex                   | Sex: Man, Vrouw, Niet vermeld (i.e., man, woman, not specified, respectively)                   | character      | Vrouw   
| **Type**                       | Type                   | Type of measurement: Totaal, Ziekenhuisopname, Overleden (i.e., total, hospitilzed, deceased, respectively)                   | character      | Totaal                 |
| **AantalCumulatief** | Total count | Number of newly diagnosed (*Totaal*\*), hospitalized (*Ziekenhuisopname*\*\*), or deceased (*Overleden*\*\*) cases per sex (*Man*, *Vrouw* or *Niet vermeld*) on the date of notification since the start of the outbreak | numeric (integer) | 25566 |

**\*** 'Totaal' numbers are based on the reported cases with confirmed COVID-19 infection at the GGDs (Public Health Services). <br/>
**\*\*** The 'Totaal' and 'Overleden' numbers of COVID-19 cases are actually higher than displayed, as not all people with COVID-19 symptoms are being tested. The actual 'Ziekenhuisopname' numbers of COVID-19 cases are also higher, as these numbers are based on the information available on the moment of notification. Hospitalizations after notifications are not always known. <br/>

### Age

**Directory:** [data-desc/data-age](data-age) <br>
**Daily file format:** RIVM_NL_age_yyyy-mm-dd.csv<br>
**Latest file format:** [RIVM_NL_age_latest.csv](data-age/RIVM_NL_age_latest.csv)<br>
**Complete file format:** [RIVM_NL_age.csv](data-age/RIVM_NL_age.csv)

| Column name                  | Translation                       | Description                       | Format                            | Example                       | 
|-----------------------------|-----------------------------------|-----------------------------------|----------------------------------------|-------------------------------|
| **Datum**                        | Date                   | Date of notification                   | YYYY-MM-DD (ISO 8601) | 2020-03-27 |
| **Leeftijdsgroep**                       | Age group                   | Ages, ranging from 0 to 95,  divided in 19 groups of 5. Two additional groups are 95+ and Niet vermeld (i.e., not specified)                     | character      | 25-29      
| **Type**                       | Type                   | Type of measurement: Totaal, Ziekenhuisopname, Overleden (i.e., total, hospitilzed, deceased, respectively)                   | character      | Totaal                 |
| **AantalCumulatief** | Total count | Number of newly diagnosed (*Totaal*\*), hospitalized (*Ziekenhuisopname*\*\*), or deceased (*Overleden*\*\*) cases per sex (*Man*, *Vrouw* or *Niet vermeld*) on the date of notification since the start of the outbreak | numeric (integer) | 390 |

**\*** 'Totaal' numbers are based on the reported cases with confirmed COVID-19 infection at the GGDs (Public Health Services). <br/>
**\*\*** The 'Totaal' and 'Overleden' numbers of COVID-19 cases are actually higher than displayed, as not all people with COVID-19 symptoms are being tested. The actual 'Ziekenhuisopname' numbers of COVID-19 cases are also higher, as these numbers are based on the information available on the moment of notification. Hospitalizations after notifications are not always known. <br/>
