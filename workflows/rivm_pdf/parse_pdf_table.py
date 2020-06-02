import re
import datetime
from pathlib import Path

import pandas as pd

# DATE=datetime.date.today()
DATE = datetime.date(2020, 6, 2)

AGES = ["0-4", "5-9", "10-14", "15-19", "20-24", "25-29", "30-34", "35-39", "40-44", "45-49", "50-54", "55-59", "60-64", "65-69", "70-74", "75-79", "80-84", "85-89", "90-94", "95+", "Niet vermeld"]
PROVINCIES = ["Drenthe", "Flevoland", "Friesland", "Gelderland", "Groningen", "Limburg", "Noord-Brabant", "Noord-Holland", "Overijssel", "Utrecht", "Zeeland", "Zuid-Holland"]
GENDER = ["Man", "Vrouw", "Niet vermeld"]
ONDERLIGGEND_A = ["Totaal gemeld","Onderliggende aandoening en/of zwangerschap","Geen onderliggende aandoening","Niet vermeld"]
ONDERLIGGEND_B = ["Zwangerschap", "Cardio-vasculaire aandoeningen en hypertensie", "Diabetes", "Leveraandoening", "Chronische neurologische of neuromusculaire aandoeningen", "Immuundeficientie", "Nieraandoening", "Chronische longaandoeningen", "Maligniteit", "Overig"]


#### Data-misc
DATA_FOLDER = Path("data-misc/data-underlying")

def export_date(df, data_folder, prefix, data_date=None, label=None):

    if data_date:
        df_date = df.loc[df["Datum"] == data_date, :]
    else:
        df_date = df

    # export with data date
    if label is not None:
        export_path = Path(DATA_FOLDER, data_folder, f"{prefix}_{label}.csv")
    else:
        export_path = Path(DATA_FOLDER, data_folder, f"{prefix}.csv")

    print(f"Export {export_path}")
    df_date.to_csv(export_path, index=False)
    

def parse_onderliggende_a(content):
    DATA_FOLDER = Path("data-misc/data-underlying")

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
       
    new = pd.DataFrame()
    for i, v in enumerate(onderliggend_a[0]):   
        data = [(f"{DATE}",f"{ONDERLIGGEND_A[i]}",f"{v}")]
        new = new.append(data, ignore_index=True)
        
    new = new.rename(columns={0: 'Datum', 1: 'Type', 2: 'AantalCumulatief'})
        
    df = pd.read_csv(Path("data-misc/data-underlying/data-underlying_statistics", "RIVM_NL_deceased_under70_statistics.csv"), encoding = "utf8")
    
    if f"{DATE}" not in str(df['Datum']):
        df = df.append(new, ignore_index = True)
        df = df.sort_values(by='Datum')   
        df = df.reset_index(drop=True)
        
        Path(DATA_FOLDER, "data-underlying_statistics").mkdir(exist_ok=True)
       
        # export all
        export_date(df, "data-underlying_statistics", "RIVM_NL_deceased_under70_statistics", data_date=None, label=None)
    else:
        print("Selected date is already in statistics file")


def parse_onderliggende_b(content):
    DATA_FOLDER = Path("data-misc/data-underlying")

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
        
    new = pd.DataFrame()
    for i, v in enumerate(onderliggend_b[0]):   
        data = [(f"{DATE}",f"{ONDERLIGGEND_B[i]}",f"{v}")]
        new = new.append(data, ignore_index=True)
        
    new = new.rename(columns={0: 'Datum', 1: 'Type', 2: 'AantalCumulatief'})
        
    df = pd.read_csv(Path("data-misc/data-underlying/data-underlying_conditions", "RIVM_NL_deceased_under70_conditions.csv"), encoding = "utf8")
    
    if f"{DATE}" not in str(df['Datum']):
        df = df.append(new, ignore_index = True)
        df = df.sort_values(by='Datum')   
        df = df.reset_index(drop=True)
        
        Path(DATA_FOLDER, "data-underlying_conditions").mkdir(exist_ok=True)
        
        # export all
        export_date(df, "data-underlying_conditions", "RIVM_NL_deceased_under70_conditions", data_date=None, label=None)

    else:
        print("Selected date is already in conditions file")


### Data-desc 
DATA_FOLDER = Path("data")

def parse_age(content):
    
    DATA_FOLDER = Path("data")

    age_match = re.findall(r"Totaal gemeld\n0-4\n5-9\n10-14\n15-19\n20-24\n25-29\n30-34\n35-39\n40-44\n45-49\n50-54\n55-59\n60-64\n65-69\n70-74\n75-79\n80-84\n85-89\n90-94\n95\+\nNiet vermeld\n\n\d+\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n.*\nZiekenhuisopname\n\d+\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n.*\nOverleden\n\d+\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)\n(\d+)", content, re.MULTILINE)
    assert len(age_match[0]) == 63

    for i, v in enumerate(age_match[0][0:21]):
        print(f"{DATE},{AGES[i]},Totaal,{v}")

    for i, v in enumerate(age_match[0][21:42]):
        print(f"{DATE},{AGES[i]},Ziekenhuisopname,{v}")

    for i, v in enumerate(age_match[0][42:63]):
        print(f"{DATE},{AGES[i]},Overleden,{v}")
        

def parse_gender(content):
    
    DATA_FOLDER = Path("data")

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

    new = pd.DataFrame()
    for i, v in enumerate(gender[0][0:3]):
        #print(f"{DATE},{GENDER[i]},Totaal,{v}")
        data = [(f"{DATE}", f"{GENDER[i]}", "Totaal",f"{v}")]
        new = new.append(data, ignore_index=True)

    for i, v in enumerate(gender[0][3:6]):
        #print(f"{DATE},{GENDER[i]},Ziekenhuisopname,{v}")
        data = [(f"{DATE}", f"{GENDER[i]}", "Ziekenhuisopname",f"{v}")]
        new = new.append(data, ignore_index=True)

    for i, v in enumerate(gender[0][6:9]):
        #print(f"{DATE},{GENDER[i]},Overleden,{v}")
        data = [(f"{DATE}", f"{GENDER[i]}", "Overleden",f"{v}")]
        new = new.append(data, ignore_index=True)
    

    new = new.rename(columns={0: 'Datum', 1: 'Geslacht', 2: 'Type', 3: 'Aantal'})

    df = pd.read_csv(Path("data", "rivm_NL_covid19_sex.csv"), encoding = "utf8")
    
    if f"{DATE}" not in str(df['Datum']):
        df = df.append(new, ignore_index = True)
        df = df.reset_index(drop=True)
        
        Path(DATA_FOLDER).mkdir(exist_ok=True)
        
        # export all
        export_date(df, "", "rivm_NL_covid19_sex", data_date=None, label=None)

    else:
        print("Selected date is already in sex file")

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
    
    parse_onderliggende_b(content)
    
    parse_gender(content)

    # parse_age(content)

    # print("\n\n\n\n")
    
    parse_gender(content)

    parse_provincie(content)

    print("\n\n\n\n")

    

    print("\n\n\n\n")

    df = pd.DataFrame(parse_test_report(content))
    df["Totaal"] = df["Totaal"].cumsum()
    df["Positief"] = df["Positief"].cumsum()
    df = df.set_index(["Datum", "Labs"]).stack().reset_index()
    df.columns = ['Datum', 'Labs', 'Type', "Aantal"]
    df["PublicatieDatum"] = DATE
    print(df[['PublicatieDatum', 'Datum', 'Labs', 'Type', "Aantal"]].to_csv(index=False))
