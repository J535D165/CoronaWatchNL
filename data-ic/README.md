# Codebook `data-ic` - CoronaWatchNL

## Data update

All datasets are updated on a daily base. Availability depends on the publication by NICE and LCPS.

## Data format

### NICE

**Directory:** [data-ic/data-nice](data-nice) <br>
**Long file format:** [NICE_IC_long_latest.csv](data-nice/NICE_IC_long_latest.csv)<br>
**Wide file format:** [NICE_IC_wide_latest.csv](data-nice/NICE_IC_wide_latest.csv)<br>

#### Wide format
| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date | Date of notification | YYYY-MM-DD (ISO 8601) | 2020-03-27 |
| **IngezetteICs** | Used IC units | Number of intensive care (IC) units\* with at least one Dutch COVID-19 case on the date of notification | numeric (integer) | 74 |
| **TotaalOpnamen** | Total IC intakes | Total number of IC intakes on the date of notificationn | numeric (integer) | 921 |
| **ToenameOpnamen** | New IC intakes | Number of newly confirmed or suspected COVID-19 IC intakes on the date of notification | numeric (integer) | 112 |
| **CumulatiefOpnamen** | Cumulative IC intakes | Total number of IC intakes since the start of the outbreak until the date of notification | numeric (integer) | 1135 |
| **ToenameOntslagZiekenhuis** | New hospital discharges | New number of IC-cases that left the hospital alive on the date of notification | numeric (integer) | 5 |
| **CumulatiefOntslagZiekenhuis** | Cumulative hospital discharges | Total number of IC-cases that left the hospital alive since the start of the outbreak until the date of notification | numeric (integer) | 39 |
| **ToenameOntslagOverleden** | New IC deaths | New number of IC-cases that died\*\* in hospital during/after IC intake on the date of notification | numeric (integer) | 14 |
| **CumulatiefOntslagOverleden** | Cumulative IC deaths | Total number of IC-cases that died in hospital during/after IC intake since the start of the outbreak until the date of notification | numeric (integer) | 121 |
| **TotaalOntslagIC** | Total IC discharges | Total number of discharged IC-cases that are still in hospital\*\*\* on the date of notification | numeric (integer) | 83 |

**\*** These can be situated in either the Netherlands or in Germany. <br/>
**\*\*** Deaths outside hospitals are not included in these numbers. <br/>
**\*\*\*** These people are discharged from the IC but are still hospitalized. Eventually, these cases will be either added to the hospital discharges or IC deaths counts. <br/>

#### Long format
| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date | Date of notification | YYYY-MM-DD (ISO 8601) | 2020-03-27 |
| **Type** | Type | Type of measurement: i.e., Totaal ingezette IC's, Toename opnamen (IC), Totaal opnamen (IC), Cumulatief opnamen (IC), Toename ontslag (ziekenhuis), Cumulatief ontslag (ziekenhuis), Toename ontslag (overleden), Cumulatief ontslag (overleden), Totaal ontslag (IC).| character | Cumulatief opgenomen (IC) |
| **Aantal** | Count | Number of intensive care (IC) units\* with at least one Dutch COVID-19 case on the date of notification (*Totaal ingezette IC's*), number of newly confirmed or suspected COVID-19 IC intakes on the date of notification (*Toename opnamen (IC)*), total number of IC intakes on the date of notification (*Totaal opnamen (IC)*), total number of IC intakes since the start of the outbreak until the date of notification (*Cumulatief opnamen (IC)*), new and total number of IC-cases that left the hospital alive (*Toename ontslag (ziekenhuis)* and *Cumulatief ontslag (ziekenhuis)*, respectively), new and total number of IC-cases that died in hospital after IC intake (*Toename ontslag (overleden)*\*\* and *Cumulatief ontslag (overleden)*, respectively), and total number of discharged IC-cases that are still in hospital (*Totaal ontslag (IC)*\*\*\*)  | numeric (integer) | 1135|

**\*** These can be situated in either the Netherlands or in Germany. <br/>
**\*\*** Deaths outside hospitals are not included in these numbers. <br/>
**\*\*\*** These people are discharged from the IC but are still hospitalized. Eventually, these cases will be either added to the hospital discharges or IC deaths counts. <br/>

### LCPS

**Directory:** [data-ic/data-lcps](data-lcps) <br>
**Complete file format:** [LCPS_IC_latest.csv](data-lcps/LCPS_IC_latest.csv)

| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date | Date of notification | YYYY-MM-DD (ISO 8601) | 2020-04-04 |
| **Land** | Country | Dutch COVID-19 cases were taken into the IC in either Germany (*Duitsland*) or the Netherlands (*Nederland*) | character | Nederland |
| **Aantal** | Count | Total number of IC intakes\* in Germany, the Netherlands, and in total (sum of both countries) on the date of notification  | numeric (integer) | 1343 |

**\*** These numbers are based on NICE data. However, to compensate for the reporting lag, LCPS tries to estimate the size of this lag and adds it to the numbers reported by NICE. LCPS data is, therefore, consistently higher than the 'totaalOpnamen' reported by NICE. <br/>