#!/usr/bin/env python
# coding: utf-8

# In[105]:
from plot_utils import process_plots

SUBJECT = ""
DATA_FILENAME = "data/rivm_corona_in_nl_daily.csv"
GROWTH_FACTOR_PLOT_FILENAME = "plots/growthfactor.png"
SIGMOID_PLOT_FILENAME = "plots/sigmoid.png"
EXPONENTIAL_PLOT_FILENAME = "plots/exponential_growth_daily.png"
EXPONENTIAL_BI_PLOT_FILENAME = "plots/exponential_growth_bi_daily.png"

if __name__ == "__main__":

    process_plots(SUBJECT,
                  DATA_FILENAME,
                  GROWTH_FACTOR_PLOT_FILENAME,
                  SIGMOID_PLOT_FILENAME,
                  EXPONENTIAL_PLOT_FILENAME,
                  EXPONENTIAL_BI_PLOT_FILENAME,
                  "",
                  False)
