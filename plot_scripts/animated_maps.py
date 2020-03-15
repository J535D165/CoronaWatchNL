#!/usr/bin/env python
# coding: utf-8

# In[216]:


import geopandas  # requires descartes
import numpy
import pandas
from PIL import Image

import io
from copy import deepcopy

from matplotlib import cm
from matplotlib.colors import LinearSegmentedColormap


# In[14]:


df = geopandas.read_file("ext/gemeente-2019.geojson")


# In[159]:


data = pandas.read_csv("data/rivm_corona_in_nl_table.csv")
data = df.merge(data, left_on="Gemnr", right_on="Gemeentecode", how="left")


# In[217]:


cmap = LinearSegmentedColormap.from_list('mycmap', ['grey', 'red'])


# In[240]:


def draw_map(data, col, text=None, cc=True, title=None):
    
    ax = data.plot(column=col, cmap=cmap, figsize=(7.5, 9))
    ax.axis('off')
    ax.axis('tight');
    ax.axis('equal');

    if text:
        # place a text box in upper left in axes coords
        ax.text(0.1, 0.82, text, transform=ax.transAxes, fontsize=14,
                verticalalignment='top')   

    # place a text box in upper left in axes coords
    ax.text(0.92, 0.4, "github.com/J535D165/CoronaWatchNL", transform=ax.transAxes, fontsize=9,
            verticalalignment='top', rotation='vertical')  

    if title:
        ax.text(0.15, 1, title, transform=ax.transAxes, fontsize=12,
                verticalalignment='top') 

    buf = io.BytesIO()
    ax.figure.savefig(buf, format='png', dpi = 200)
    buf.seek(0)
    pil_img = deepcopy(Image.open(buf))
    buf.close()

    return pil_img

# draw_map(data, '2020-03-12', "2020-03-12", title="Aantal positieve coronavirus testen in NL")


# In[238]:


data['2020-02-24'] = 0
data['2020-02-25'] = 0
data['2020-02-26'] = 0

col_days = sorted([col for col in list(data) if col.startswith("2020")])

figs_corona = []
for col in col_days:
    figs_corona.append(
        draw_map(data, col, col, title="Totaal Coronavirus (COVID-19)-meldingen in NL")
    )

figs_corona[0].save('plots/map_nl_corona_abs_municipality.gif',
               save_all=True, append_images=figs_corona[1:], optimize=False, duration=400, loop=0)


# In[239]:


data['2020-02-23'] = 0
data['2020-02-24'] = 0
data['2020-02-25'] = 0
data['2020-02-26'] = 0

col_days_raw = sorted([col for col in list(data) if col.startswith("2020")])

new_data = data.copy()

for i, col in enumerate(col_days_raw[1:]):
    print(i, col)
    new_data["diff_" + col] = new_data[col_days_raw[i+1]] - new_data[col_days_raw[i]]
    new_data.loc[new_data["diff_" + col] < 0, "diff_" + col] = 0

col_days = sorted([col for col in list(new_data) if col.startswith("diff")])

# relative
# new_data[col_days] = new_data[col_days]/new_data[col_days].max().max()

figs_corona = []
for col in col_days:
    figs_corona.append(
        draw_map(new_data, col, col[5:], title="Nieuwe Coronavirus (COVID-19)-meldingen in NL")
    )
    
figs_corona[0].save('plots/map_nl_corona_diff_municipality.gif',
               save_all=True, append_images=figs_corona[1:], optimize=False, duration=400, loop=0)


# In[ ]:




