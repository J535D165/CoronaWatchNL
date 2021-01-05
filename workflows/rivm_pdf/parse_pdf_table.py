import re
import datetime
from pathlib import Path

import pandas as pd

DATE = datetime.date.today()
# DATE = datetime.date(2020, 12, 29)


AGES = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54",
        "55-59", "60-64", "65-69", "70-74", "75-79", "80-84", "85-89", "90-94", "95+", "Niet vermeld"]
PROVINCIES = ["Groningen", "Friesland", "Drenthe", "Overijssel", "Flevoland", "Gelderland",
              "Utrecht", "Noord-Holland", "Zuid-Holland", "Zeeland", "Noord-Brabant", "Limburg"]
GENDER = ["Man", "Vrouw", "Niet vermeld"]
ONDERLIGGEND_A = ["Totaal gemeld", "Onderliggende aandoening en/of zwangerschap",
                  "Geen onderliggende aandoening", "Niet vermeld"]
ONDERLIGGEND_B = [
    "Zwangerschap",
    "Postpartum",
    "Cardio-vasculaire aandoeningen en hypertensie",
    "Diabetes",
    "Leveraandoening",
    "Chronische neurologische of neuromusculaire aandoeningen",
    "Immuundeficientie",
    "Nieraandoening",
    "Chronische longaandoeningen",
    "Maligniteit",
    "Obesitas",
    "Dementie/Alzheimer",
    "Parkinson",
    "Overig"
]


# Data-misc
def parse_onderliggende_a(content):

    onderliggend_a = re.findall(
        r"Totaal gemeld\n"
        r"Onderliggende aandoening en\/of zwangerschap\n"
        r"Geen onderliggende aandoening\n"
        r"Niet vermeld\n"
        r"1\n\n"
        r"%\n\n"
        r"(\d+)\n"
        r"(\d+) [0-9\.]+\n"
        r"(\d+) [0-9\.]+\n"
        r"(\d+) [0-9\.]+",
        content
    )
    assert len(onderliggend_a[0]) == 4

    new = pd.DataFrame()
    for i, v in enumerate(onderliggend_a[0]):
        data = [(f"{DATE}", f"{ONDERLIGGEND_A[i]}", f"{v}")]
        new = new.append(data, ignore_index=True)

    new = new.rename(columns={0: 'Datum', 1: 'Type', 2: 'AantalCumulatief'})

    df = pd.read_csv(Path("data-misc/data-underlying/data-underlying_statistics",
                          "RIVM_NL_deceased_under70_statistics.csv"), encoding="utf8")

    if f"{DATE}" not in str(df['Datum']):
        df = df.append(new, ignore_index=True)
        df = df.sort_values(by=['Datum', 'Type'], ascending=[True, False])
        df = df.reset_index(drop=True)

        export_path = Path("data-misc/data-underlying", "data-underlying_statistics",
                           "RIVM_NL_deceased_under70_statistics.csv")
        print(f"Export {export_path}")
        df.to_csv(export_path, index=False)

    else:
        print("Selected date is already in statistics file")


def parse_onderliggende_b(content):

    onderliggend_b = re.findall(
        r"Nieraandoening\n"
        r"Chronische longaandoeningen\n"
        r"Maligniteit\n"
        r"Obesitas3\n"
        r"Dementie/Alzheimer3\n"
        r"Parkinson3\n"
        r"Overig\n"
        r"1\n\n"
        r"2\n\n"
        r"3\n\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)",
        content)

    assert len(onderliggend_b[0]) == 14

    new = pd.DataFrame()
    for i, v in enumerate(onderliggend_b[0]):
        data = [(f"{DATE}", f"{ONDERLIGGEND_B[i]}", f"{v}")]
        new = new.append(data, ignore_index=True)

    new = new.rename(columns={0: 'Datum', 1: 'Type', 2: 'AantalCumulatief'})

    df = pd.read_csv(Path("data-misc/data-underlying/data-underlying_conditions",
                          "RIVM_NL_deceased_under70_conditions.csv"), encoding="utf8")

    if f"{DATE}" not in str(df['Datum']):
        df = df.append(new, ignore_index=True)
        df = df.sort_values(by=['Datum', 'Type'])
        df = df.reset_index(drop=True)

        export_path = Path("data-misc/data-underlying", "data-underlying_conditions",
                           "RIVM_NL_deceased_under70_conditions.csv")
        print(f"Export {export_path}")
        df.to_csv(export_path, index=False)

    else:
        print("Selected date is already in conditions file")


# Data-desc
def parse_age(content):

    age_match = re.findall(
        r"Leeftijdsgroep\n"
        r"Totaal gemeld\n"
        r"0-4\n"
        r"5-9\n"
        r"10-14\n"
        r"15-19\n"
        r"20-24\n"
        r"25-29\n"
        r"30-34\n"
        r"35-39\n"
        r"40-44\n"
        r"45-49\n"
        r"50-54\n"
        r"55-59\n"
        r"60-64\n"
        r"65-69\n"
        r"70-74\n"
        r"75-79\n"
        r"80-84\n"
        r"85-89\n"
        r"90-94\n"
        r"95\+\n"
        r"Niet vermeld\n"
        r"1\n\n"
        r"2\n\n"
        r"Totaal %\ngemeld\n"
        r"\d+\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n"
        r"\d+\.\d\n\n"
        r"Ziekenhuisopname %\n"
        r"\d+\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n\n"
        r"Overleden %\n"
        r"\d+\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n\n",
        content)

    assert len(age_match[0]) == 63

    new = pd.DataFrame()
    for i, v in enumerate(age_match[0][0:21]):
        data = [(f"{DATE}", f"{AGES[i]}", "Totaal", f"{v}")]
        new = new.append(data, ignore_index=True)

    for i, v in enumerate(age_match[0][21:42]):
        data = [(f"{DATE}", f"{AGES[i]}", "Ziekenhuisopname", f"{v}")]
        new = new.append(data, ignore_index=True)

    for i, v in enumerate(age_match[0][42:63]):
        data = [(f"{DATE}", f"{AGES[i]}", "Overleden", f"{v}")]
        new = new.append(data, ignore_index=True)

    new = new.rename(
        columns={0: 'Datum', 1: 'LeeftijdGroep', 2: 'Type', 3: 'Aantal'})

    df = pd.read_csv(Path("data", "rivm_NL_covid19_age.csv"), encoding="utf8")

    if f"{DATE}" not in str(df['Datum']):
        df = df.append(new, ignore_index=True)
        df = df.reset_index(drop=True)

        export_path = Path("data", "rivm_NL_covid19_age.csv")
        print(f"Export {export_path}")
        df.to_csv(export_path, index=False)

    else:
        print("Selected date is already in age file")


def parse_gender(content):

    gender = re.findall(
        r"Geslacht\n"
        r"Totaal gemeld\n"
        r"Man\n"
        r"Vrouw\n"
        r"Niet vermeld\n"
        r"1\n"
        r"2\n\n"
        r"Totaal %\ngemeld"
        r"\d+\n"
        r"(\d+) \d+\.\d\n"
        r"(\d+) \d+\.\d\n"
        r"(\d+) \d+\.\d\n\n"
        r"Ziekenhuisopname %\n\n"
        r"Overleden %\n\n"
        r"\d+\n"
        r"(\d+) \d+\.\d\n"
        r"(\d+) \d+\.\d\n"
        r"(\d+) \d+\.\d\n\n"
        r"\d+\n"
        r"(\d+) \d+\.\d\n"
        r"(\d+) \d+\.\d\n"
        r"(\d+) \d+\.\d",
        content,
        re.MULTILINE
    )

    assert len(gender[0]) == 9

    new = pd.DataFrame()
    for i, v in enumerate(gender[0][0:3]):
        # print(f"{DATE},{GENDER[i]},Totaal,{v}")
        data = [(f"{DATE}", f"{GENDER[i]}", "Totaal", f"{v}")]
        new = new.append(data, ignore_index=True)

    for i, v in enumerate(gender[0][3:6]):
        # print(f"{DATE},{GENDER[i]},Ziekenhuisopname,{v}")
        data = [(f"{DATE}", f"{GENDER[i]}", "Ziekenhuisopname", f"{v}")]
        new = new.append(data, ignore_index=True)

    for i, v in enumerate(gender[0][6:9]):
        # print(f"{DATE},{GENDER[i]},Overleden,{v}")
        data = [(f"{DATE}", f"{GENDER[i]}", "Overleden", f"{v}")]
        new = new.append(data, ignore_index=True)

    new = new.rename(
        columns={0: 'Datum', 1: 'Geslacht', 2: 'Type', 3: 'Aantal'})

    df = pd.read_csv(Path("data", "rivm_NL_covid19_sex.csv"), encoding="utf8")

    if f"{DATE}" not in str(df['Datum']):
        df = df.append(new, ignore_index=True)
        df = df.reset_index(drop=True)

        export_path = Path("data", "rivm_NL_covid19_sex.csv")
        print(f"Export {export_path}")
        df.to_csv(export_path, index=False)

    else:
        print("Selected date is already in sex file")

def parse_provincie(content):

    provincie_match = re.findall(
        r"Provincie\n"
        r"Totaal gemeld\n"
        r"Groningen\n"
        r"Friesland\n"
        r"Drenthe\n"
        r"Overijssel\n"
        r"Flevoland\n"
        r"Gelderland\n"
        r"Utrecht\n"
        r"Noord-Holland\n"
        r"Zuid-Holland\n"
        r"Zeeland\n"
        r"Noord-Brabant\n"
        r"Limburg\n"
        r"1\n\n"
        r"2\n\n"
        r"Totaal gemeld\n"
        r"\d+\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)\n"
        r"(\d+)",
        content, re.MULTILINE)

    assert len(provincie_match[1]) == 12

    new = pd.DataFrame()
    for i, v in enumerate(provincie_match[1]):
        data = [(f"{DATE}", f"{PROVINCIES[i]}", f"{v}")]
        new = new.append(data, ignore_index=True)

    new = new.rename(columns={0: 'Datum', 1: 'Provincienaam', 2: 'Aantal'})

    df = pd.read_csv(
        Path("data", "rivm_NL_covid19_province.csv"), encoding="utf8")

    if f"{DATE}" not in str(df['Datum']):
        df = df.append(new, ignore_index=True)
        df = df.sort_values(by='Datum')
        df = df.reset_index(drop=True)

        export_path = Path("data", "rivm_NL_covid19_province.csv")
        print(f"Export {export_path}")
        df.to_csv(export_path, index=False)

    else:
        print("Selected date is already in province file")

def parse_test_report(content):

    try:
        regex = r"Virologische dagstaat\. Meldingen t\/m [0-9\-]+ zijn samengevoegd.* Datum T\/m ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) Rapp\. labs (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) Geteste pers\. (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) Pers\. met pos\. uitslag (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)"

        pos_tests = re.findall(regex, content, re.MULTILINE)

        assert len(pos_tests[0]) == 40

        result = []

        for i in range(10):

            result.append({
                "Datum": pos_tests[0][i],
                "Labs": int(pos_tests[0][i + 10]),
                "Totaal": int(pos_tests[0][i + 20]),
                "Positief": int(pos_tests[0][i + 30]),
            })

        return result
    except Exception:

        regex = (r"Datum T\/m ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+)\n"
                 r"\d+\n\n"
                 r"\d+ \d+\n\n"
                 r"Rapp. labs (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)\n\n"
                 r"Geteste pers. (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)\n\n"
                 r"Pers. met pos. uitslag (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)")
        pos_tests = re.findall(regex, content, re.MULTILINE)

        assert len(pos_tests[0]) == 40

        result = []

        for i in range(10):

            result.append({
                "Datum": pos_tests[0][i],
                "Labs": int(pos_tests[0][i + 10]),
                "Totaal": int(pos_tests[0][i + 20]),
                "Positief": int(pos_tests[0][i + 30]),
            })

        return result


def read_pdf(fp):
    """Read the pdf"""

    with open(fp, "r", encoding="latin1") as f:
        return f.read()


if __name__ == '__main__':

    content = read_pdf(
        "reports/COVID-19_epidemiological_report_{}.txt".format(
            str(DATE).replace("-", ""))
    )

    parse_onderliggende_a(content)

    parse_onderliggende_b(content)

    parse_gender(content)

    parse_age(content)

    parse_provincie(content)
