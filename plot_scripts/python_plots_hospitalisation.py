#!/usr/bin/env python
# coding: utf-8

# In[68]:
from plot_utils import process_plots

SUBJECT = "ziekenhuisopnamen "
DATA_FILENAME = "data/rivm_corona_in_nl_hosp.csv"
GROWTH_FACTOR_PLOT_FILENAME = "plots/growthfactor_hospitalisation.png" 
SIGMOID_PLOT_FILENAME = "plots/sigmoid_hospitalisation.png"
EXPONENTIAL_PLOT_FILENAME = "plots/exponential_hospitalisation_growth_daily.png"
EXPONENTIAL_BI_PLOT_FILENAME = "plots/exponential_hospitalisation_growth_bi_daily.png"

# In[105]:

if __name__ == "__main__":

    process_plots(SUBJECT,
                  DATA_FILENAME,
                  GROWTH_FACTOR_PLOT_FILENAME,
                  SIGMOID_PLOT_FILENAME,
                  EXPONENTIAL_PLOT_FILENAME,
                  EXPONENTIAL_BI_PLOT_FILENAME,                 
                  "",
                  False)
