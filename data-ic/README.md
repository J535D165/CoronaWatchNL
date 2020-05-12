# Codebook `data-ic` - CoronaWatchNL

## Data update

All datasets are updated on a daily base. Availability depends on the publication by RIVM.

## Data format

### NICE

**Directory:** [data-ic/data-nice](data-nice) <br>
**Daily file format:** NICE_NL_IC_yyyy-mm-dd.csv<br>
**Latest file format:** [NICE_NL_IC_latest.csv](data-nice/NICE_NL_IC_latest.csv)<br>
**Complete file format:** [NICE_NL_IC.csv](data-nice/NICE_NL_IC.csv)

| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date | Date of notification | YYYY-MM-DD (ISO 8601) | 2020-03-27 |
| **Type** | Type | Type of measurement (i.e., icCount, newIntake, intakeCount, intakeCumulative, survivedCumulative, diedCumulative) | character | intakeCumulative |
| **Aantal** | Count | Number of intensive care (IC) units\* with at least one Dutch COVID-19 case on the date of notification (*icCount*), number of newly confirmed COVID-19 IC intakes on the date of notification (*newIntake*), number of 'actual' IC intakes on the date of notification (*intakeCount*), total number of IC intakes on the date of notification since the start of the outbreak (*intakeCumulative*), total number of IC-cases that left the IC alive (*survivedCumulative*), and total number of IC-cases that died in hospital (*diedCumulative*\*\*)  | numeric (integer) | 1143|

**\*** These can be situated in either the Netherlands or in Germany. <br/>
**\*\*** Deaths outside hospitals are not included in these numbers. <br/>

### LCPS

**Directory:** [data-ic/data-lcps](data-lcps\) <br>
**Daily file format:** LCPS_NL_IC_yyyy-mm-dd.csv<br>
**Latest file format:** [LCPS_NL_IC_latest.csv](data-lcps/LCPS_NL_IC_latest.csv)<br>
**Complete file format:** [LCPS_NL_IC_.csv](data-lcps/LCPS_NL_IC.csv)

| Column name | Translation | Description | Format | Example |
|---|---|---|---|---|
| **Datum** | Date | Date of notification | YYYY-MM-DD (ISO 8601) | 2020-04-04 |
| **Land** | Country | Dutch COVID-19 cases were taken into the IC in either Germany (*Duitsland*) or the Netherlands (*Nederland*) | character | Nederland |
| **Aantal** | Count | Number of 'actual' IC intakes\* in Germany, the Netherlands, and in total (sum of both countries) on the date of notification  | numeric (integer) | 1343 |

**\*** These numbers are based on NICE data. However, to compensate for the reporting lag, LCPS tries to estimate the size of this lag and adds it to the numbers reported by NICE. LCPS data is, therefore, consistently higher than the 'intakeCount' reported by NICE. <br/>