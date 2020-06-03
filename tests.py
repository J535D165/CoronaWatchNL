from pathlib import Path

import pandas


def test_national():

    fp = Path("data", "rivm_NL_covid19_national.csv")

    national = pandas.read_csv(fp)

    # all datum have 3 items in group
    assert (national.groupby("Datum")['Type'].count() == 3).all()
    assert (national.groupby("Datum")['Type'].nunique() == 3).all()


def test_age():

    print("test age")

    fp = Path("data", "rivm_NL_covid19_age.csv")

    df_age = pandas.read_csv(fp)

    assert df_age["Aantal"].notnull().all()


def test_sex():

    print("test gender")

    fp = Path("data", "rivm_NL_covid19_sex.csv")

    df_sex = pandas.read_csv(fp)

    assert df_sex["Aantal"].notnull().all()


if __name__ == '__main__':

    test_national()

    test_age()

    test_sex()
