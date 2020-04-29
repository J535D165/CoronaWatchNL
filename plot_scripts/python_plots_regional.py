#!/usr/bin/env python
# coding: utf-8

# In[68]:
from plot_utils import process_plots

# In[105]:

SUBJECT = "voor de provincie "
DATA_FILENAME = "data/rivm_NL_covid19_province.csv"
EXPONENTIAL_PLOT_FILENAME = ""
EXPONENTIAL_BI_PLOT_FILENAME = ""

REGIONS =  [
                'Drenthe',
                'Flevoland',
                'Friesland',
                'Gelderland',
                'Groningen',
                'Limburg',
                'Noord-Brabant',
                'Noord-Holland',
                'Overijssel',
                'Utrecht',
                'Zeeland',
                'Zuid-Holland'
           ]

if __name__ == "__main__":

    for region in REGIONS:

        growth_factor_plot_filename = "plots/growthfactor_" + region + ".png" 
        sigmoid_plot_filename = "plots/sigmoid_" + region + ".png"
        region_subject = SUBJECT + region + " "

        print("Processing: ", region)

        try:
            process_plots(region_subject,
                          DATA_FILENAME,
                          growth_factor_plot_filename,
                          sigmoid_plot_filename,
                          EXPONENTIAL_PLOT_FILENAME,
                          EXPONENTIAL_BI_PLOT_FILENAME,
                          region,
                          True)
        except RuntimeError:
            print("No results")
            #No results
            continue
