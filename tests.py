from pathlib import Path

import pandas


def test_national():

    fp = Path("data", "rivm_NL_covid19_national.csv")

    national = pandas.read_csv(fp)

    # all datum have 3 items in group
    assert (national.groupby("Datum")['Type'].count() == 3).all()
    assert (national.groupby("Datum")['Type'].nunique() == 3).all()


if __name__ == '__main__':

    test_national()
