#!/usr/bin/env python
# coding: utf-8

from pdf2image import convert_from_path
import pandas as pd
from pathlib import Path
import numpy as np
from matplotlib import pyplot as plt
from collections import Counter
from itertools import cycle, groupby
from datetime import datetime, date
import cv2
from PIL import Image

province_mapping = {
    0: "Drenthe",
    1: "Groningen",
    2: "Overijssel",
    3: "Utrecht",
    4: "Flevoland",
    5: "Limburg",
    6: "Noord-Brabant",
    7: "Zeeland",
    8: "Friesland",
    9: "Gelderland",
    10: "Noord-Holland",
    11: "Zuid-Holland",
}


def runs_of_ones(bits, min_length):
    "Return start/end of truthy values with min length."
    start = 0
    for bit, group in groupby(bits):
        length = sum(1 for _ in group)
        if bit and length > min_length:
            end = start + length
            yield (start, end)
        start += length


def get_subplot_sections(im):
    """Return the subplots one by one."""
    cols = list(runs_of_ones((im == 255).sum(axis=0) < im.shape[0], im.shape[0] // 6))
    rows = list(runs_of_ones((im == 255).sum(axis=1) < im.shape[1], im.shape[1] // 6))
    for i, row, col in zip(range(12), cycle(rows), cycle(cols)):
        yield im[row[0] + 1 : row[1] - 1, col[0] + 1 : col[1] - 1]


def get_grid_color(section):
    bottom_row_counts = Counter(section[-1])
    grid_color = bottom_row_counts.most_common()[1][0]
    assert grid_color == 235
    return grid_color


def get_bar_pixel_heights(section, grid_color):
    for bar_nr, (start, end) in enumerate(
        runs_of_ones(section[-1] < 250, min_length=1)
    ):
        center = (start + end) // 2
        pixels = sum((section[:, center] != grid_color) & (section[:, center] < 255))
        yield (bar_nr, pixels)


def get_values_for_image(image, value_per_pixel, date):
    im = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)
    im = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    for i, section in enumerate(get_subplot_sections(im)):
        grid_color = get_grid_color(section)
        for (bar_nr, pixels) in get_bar_pixel_heights(section, grid_color):
            yield {
                "report_date": date,
                "province": province_mapping[i],
                "bar_nr": bar_nr,
                "value": int(round(pixels / value_per_pixel)),
            }


def extract_data(category, transalated, report_dir, resolution=720):
    index = pd.read_csv(report_dir / "index.csv", parse_dates=["date"])
    for i, row in index[~index[f"{category}_page"].isna()].iterrows():
        date = row["date"]
        export_path = Path(__file__).parent / translated / f"{date:%Y-%m-%d}.csv"
        export_path.parent.mkdir(exist_ok=True)
        if export_path.exists():
            continue
        print(f"Processing {category} from {row['file']}")
        file = report_dir / row["file"]
        (image,) = convert_from_path(
            str(file),
            dpi=resolution,
            first_page=int(row[f"{category}_page"]),
            last_page=int(row[f"{category}_page"]),
        )

        # crop image
        image = image.crop(
            (
                int(image.size[0] * 0.15),
                int(image.size[1] * 0.122),
                int(image.size[0] * 0.9),
                int(image.size[1] * 0.8),
            )
        )

        value_per_pixel = resolution / row[f"{category}_per_inch"]

        df = pd.DataFrame(get_values_for_image(image, value_per_pixel, date))
        totals = df.groupby("report_date")["value"].sum()
        df["date"] = pd.Timestamp("20200227") + pd.to_timedelta(
            df["bar_nr"], unit="days"
        )
        df[["report_date", "date", "province", "value"]].to_csv(
            export_path, index=False
        )


categories = {
    "ziekenhuis_per_provincie": "hospitalizations_per_province",
    "patienten_per_provincie": "patients_per_province",
    "overleden_per_provincie": "deceased_per_province",
}

report_dir = Path(__file__).parent.parent.parent / "reports"
for category, translated in categories.items():
    extract_data(category, translated, report_dir, resolution=720)
