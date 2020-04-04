#!/usr/bin/env python
# coding: utf-8

# In[105]:
from plot_utils import add_variables
from plot_utils import analyze_growth_factor
from plot_utils import compute_inflection_cases
from plot_utils import compute_inflection_point
from plot_utils import create_growthfactor_plot
from plot_utils import curve_fit
from plot_utils import fit_sigmoid
from plot_utils import fit_sigmoid_repeated
from plot_utils import process_plots
from plot_utils import plot_sigmoids
from plot_utils import read_data

SUBJECT = ""
DATA_FILENAME = "data/rivm_corona_in_nl_daily.csv"
GROWTH_FACTOR_PLOT_FILENAME = "plots/growthfactor.png"
SIGMOID_PLOT_FILENAME = "plots/sigmoid.png"


if __name__ == "__main__":

    process_plots(SUBJECT,
                  DATA_FILENAME,
                  GROWTH_FACTOR_PLOT_FILENAME,
                  SIGMOID_PLOT_FILENAME,
                  "",
                  False)
