#!/usr/bin/env python
# coding: utf-8

# In[68]:
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

# In[105]:

SUBJECT = "voor de provincie "
DATA_FILENAME = "data/rivm_NL_covid19_province.csv"
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
                          region,
                          True)
        except RuntimeError:
            print("No results")
            #No results
            continue
