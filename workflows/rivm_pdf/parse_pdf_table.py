import re
import datetime

import pandas as pd

# DATE=datetime.date.today()
DATE = datetime.date(2020, 6, 1)


AGES = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80-84", "85-89", "90-94", "95+", "Niet vermeld"]
PROVINCIES = ["Drenthe", "Flevoland", "Friesland", "Gelderland", "Groningen", "Limburg", "Noord-Brabant", "Noord-Holland", "Overijssel", "Utrecht", "Zeeland", "Zuid-Holland"]
GENDER = ["Man", "Vrouw", "Niet vermeld"]
ONDERLIGGEND_A = ["Totaal gemeld","Onderliggende aandoening en/of zwangerschap","Geen onderliggende aandoening","Niet vermeld"]
ONDERLIGGEND_B = ["Overleden", "Zwangerschap", "Cardio-vasculaire aandoeningen en hypertensie", "Diabetes", "Leveraandoening", "Chronische neurologische of neuromusculaire aandoeningen", "Immuundeficiëntie", "Nieraandoening", "Chronische longaandoeningen", "Maligniteit", "Overig"]


def parse_onderliggende_a(content):

    onderliggend_a = re.findall(
        r"Totaal gemeld\n"
        r"Onderliggende aandoening en\/of zwangerschap\n"
        r"Geen onderliggende aandoening\n"
        r"Niet vermeld\n\n"
        r"\%\n\n"
        r"(\d+)\n"
        r"(\d+) \([0-9\.]+\)\n"
        r"(\d+) \([0-9\.]+\)\n"
        r"(\d+) \([0-9\.]+\)",
        content
    )
    assert len(onderliggend_a[0]) == 4

    for i, v in enumerate(onderliggend_a[0]):
        print(f"{DATE},{ONDERLIGGEND_A[i]},Totaal,{v}")


def parse_onderliggende_b(content):

    onderliggend_b = re.findall(
        r"Nieraandoening\n"
        r"Chronische longaandoeningen\n"
        r"Maligniteit\n"
        r"Overig\n\n"
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

    assert len(onderliggend_b[0]) == 10

    for i, v in enumerate(onderliggend_b[0]):
        print(f"{DATE},{ONDERLIGGEND_B[i]},Totaal,{v}")


def parse_age(content):

    age_match = re.findall(r"Totaal gemeld\n0-4\n5-9\n10-14\n15-19\n20-24\n25-29\n30-34\n35-39\n40-44\n45-49\n50-54\n55-59\n60-64\n65-69\n70-74\n75-79\n80-84\n85-89\n90-94\n95\+\nNiet vermeld\n\n\d+\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n.*\nZiekenhuisopname\n\d+\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n.*\nOverleden\n\d+\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)", content, re.MULTILINE)
    assert len(age_match[0]) == 63

    for i, v in enumerate(age_match[0][0:21]):
        print(f"{DATE},{AGES[i]},Totaal,{v}")

    for i, v in enumerate(age_match[0][21:42]):
        print(f"{DATE},{AGES[i]},Ziekenhuisopname,{v}")

    for i, v in enumerate(age_match[0][42:63]):
        print(f"{DATE},{AGES[i]},Overleden,{v}")


def parse_provincie(content):

    provincie_match = re.findall(
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
        r"Limburg\n\n"
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
        r"(\d+)", content, re.MULTILINE)

    assert len(provincie_match[0]) == 12

    for i, v in enumerate(provincie_match[0]):
        print(f"{DATE},{PROVINCIES[i]},{v}")


def parse_gender(content):

    gender = re.findall(
        r"Geslacht\n"
        r"Totaal gemeld\n"
        r"Man\n"
        r"Vrouw\n"
        r"Niet vermeld\n\n"
        r"Totaal gemeld\n\n"
        r"%\n\n"
        r"\d+\n"
        r"(\d+) \d+\.\d\n"
        r"(\d+) \d+\.\d\n"
        r"(\d+) \d+\.\d\n\n"
        r"Ziekenhuisopname\n\n"
        r"%\n\n"
        r"\d+\n"
        r"(\d+) \d+\.\d\n"
        r"(\d+) \d+\.\d\n"
        r"(\d+) \d+\.\d\n\n"
        r"Overleden\n\n"
        r"%\n\n"
        r"\d+\n"
        r"(\d+) \d+\.\d\n"
        r"(\d+) \d+\.\d\n"
        r"(\d+) \d+\.\d",
        content,
        re.MULTILINE
    )

    assert len(gender[0]) == 9

    for i, v in enumerate(gender[0][0:3]):
        print(f"{DATE},{GENDER[i]},Totaal,{v}")

    for i, v in enumerate(gender[0][3:6]):
        print(f"{DATE},{GENDER[i]},Ziekenhuisopname,{v}")

    for i, v in enumerate(gender[0][6:9]):
        print(f"{DATE},{GENDER[i]},Overleden,{v}")


def parse_test_report(content):

    try:
        regex = r"Virologische dagstaat\. Meldingen t\/m [0-9\-]+ zijn samengevoegd.* Datum T\/m ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) ([0-9\-]+) Rapp\. labs (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) Geteste pers\. (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) Pers\. met pos\. uitslag (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+) (\d+)"

        pos_tests = re.findall(regex, content, re.MULTILINE)

        assert len(pos_tests[0]) == 40

        result = []

        for i in range(10):

            result.append({
                "Datum": pos_tests[0][i],
                "Labs": int(pos_tests[0][i+10]),
                "Totaal": int(pos_tests[0][i+20]),
                "Positief": int(pos_tests[0][i+30]),
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
                "Labs": int(pos_tests[0][i+10]),
                "Totaal": int(pos_tests[0][i+20]),
                "Positief": int(pos_tests[0][i+30]),
            })

        return result


def read_pdf(fp):
    """Read the pdf"""

    with open(fp, "r", encoding="latin1") as f:
        return f.read()


if __name__ == '__main__':

    content = read_pdf(
        "reports/COVID-19_epidemiological_report_{}.txt".format(str(DATE).replace("-", ""))
    )

    parse_onderliggende_a(content)
    print("\n")
    parse_onderliggende_b(content)

    print("\n\n\n\n")

    # parse_age(content)

    # print("\n\n\n\n")

    parse_provincie(content)

    print("\n\n\n\n")

    parse_gender(content)

    print("\n\n\n\n")

    df = pd.DataFrame(parse_test_report(content))
    df["Totaal"] = df["Totaal"].cumsum()
    df["Positief"] = df["Positief"].cumsum()
    df = df.set_index(["Datum", "Labs"]).stack().reset_index()
    df.columns = ['Datum', 'Labs', 'Type', "Aantal"]
    df["PublicatieDatum"] = DATE
    print(df[['PublicatieDatum', 'Datum', 'Labs', 'Type', "Aantal"]].to_csv(index=False))
