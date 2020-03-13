#!/usr/bin/env python
# coding: utf-8

# In[68]:


import pandas as pd
import numpy as np

import math

import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression


# In[69]:


def read_data():
    
    # Read and preprocess data file
    df = pd.read_csv("data/rivm_corona_in_nl_daily.csv")

    df['Datum'] = pd.to_datetime(df['Datum'])

    df['Dag'] = np.arange(len(df))

    df = df.set_index('Datum')
    
    return (df)  


# In[70]:


def add_variables(df):
    
    # New cases
    df['New_cases'] = df['Aantal'] - df['Aantal'].shift(1)

    # Groeifactor
    df['Growth_factor'] = df['New_cases'] / df['New_cases'].shift(1)    
    
    return(df)


# In[71]:


def analyze_growth_factor(df):

    ## regression analysis of growth factor

    df = df[df['Growth_factor'].notnull()] # remove missing values
    df = df[df['Aantal'] > 25] # only include after 25 cases were reported

    intercepts = []
    coefficients = []

    n_samples = 500

    for i in range(n_samples):

        df_resampled = df.sample(frac=1,  
                                 replace=True,
                                 random_state=i) # bootstrap

        X = df_resampled['Dag'].values.reshape(-1, 1)
        y = df_resampled['Growth_factor'].values.reshape(-1, 1)

        regr = LinearRegression()
        regr.fit(X, y)

        intercepts.append(regr.intercept_[0])
        coefficients.append(regr.coef_[0][0])
    
    return (intercepts, coefficients)


# In[72]:


def create_growthfactor_plot(df, intercepts, coefficients, inflection_date, plot_max_bootstraps=50):

    mean_intercept = np.mean(intercepts)
    mean_coefficient = np.mean(coefficients)
    
    num_days = (df.index.max() - df.index.min()) / pd.Timedelta("1 day")    
    
    plt.figure(figsize=(15,10))

    plt.plot(df['Growth_factor'],
             linestyle='',
             marker='.',
             markersize=10,
             color='black',
             label="Groeifactor",
            )

    plt.hlines(1, 
               xmin=df.index.min(), 
               xmax=df.index.max(),
               linestyles='dashed',
               color='red',
               label="Groeifactor=1"
              )

    for intercept, coefficient in zip(intercepts[:plot_max_bootstraps], coefficients[:plot_max_bootstraps]):

        plt.plot([df.index.min(), df.index.max()],
                 [intercept, intercept + num_days * coefficient],
                 alpha=0.05,
                 color='blue',
                )


    plt.plot([df.index.min(), df.index.max()],
             [mean_intercept, mean_intercept + num_days * mean_coefficient],
             label="Lineair model",
             color='blue'
            )

    plt.xticks(rotation=60)
    plt.xlabel("Datum", size=15)
    plt.ylabel("Groeifactor", size=15)
    plt.title("Groeifactor (delta nieuwe cases), maximum groei verwacht op {:%d/%m/%Y %H:00}".format(inflection_date), 
              size=20)
    plt.legend(fontsize=20)

    # plt.show()
    
    plt.savefig("plots/growthfactor.png")


# In[73]:


def compute_inflection_point(df, intercepts, coefficients):
    inflection_x = (1-np.mean(intercepts))/np.mean(coefficients) # based on intercept + coefficient * day = 1
    inflection_date = df.index.min() + inflection_x * pd.Timedelta("1 day")

    return(inflection_x, inflection_date)


# In[74]:


import math

def compute_inflection_cases(df, inflection_x):
    # Estimate number of cases at inflection point

    # if past inflection point, linear interpolation from nearest cases
    if inflection_x < len(df):

        lower_bound = df[df['Dag'] == math.floor(inflection_x)].iloc[0]['Aantal']
        upper_bound = df[df['Dag'] == math.ceil(inflection_x)].iloc[0]['Aantal']

        inflection_y = lower_bound + (inflection_x % 1) * (upper_bound - lower_bound)

    # else, estimate from exponential curve
    else:

        X = df['Dag'].values.reshape(-1, 1)
        y = df['Aantal'].values.reshape(-1, 1)

        regr = LinearRegression()
        regr.fit(X, np.log(y))

        inflection_y = np.e**(regr.intercept_ + inflection_x * regr.coef_)
        inflection_y = inflection_y[0][0]

    return inflection_y
        


# In[75]:


from scipy.optimize import curve_fit

def sigmoid(x, x0, y0, c, k):
    y = c / (1 + np.exp(-k*(x-x0))) + y0
    return y


def fit_sigmoid(df, inflection_x, inflection_y):

    X = df['Dag'].values.reshape(-1, 1)
    y = df['Aantal'].values.reshape(-1, 1)

    inference_X = [inflection_x]
    inference_y = [inflection_y]

    # mirror data in inflection point to estimate sigmoid    
    for x_val, [y_val] in zip(X[X<inflection_x], y):
        inference_X.append(x_val)
        inference_y.append(y_val)
        inference_X.append(2*inflection_x-x_val)
        inference_y.append(2*inflection_y-y_val)

    popt, pcov = curve_fit(sigmoid, inference_X, inference_y/max(inference_y))

    fitted_sigmoid = lambda k : sigmoid(k, *popt)
    
    sigmoid_X = sorted(inference_X)

    sigmoid_y = fitted_sigmoid(sigmoid_X) * max(inference_y)
    
    return(fitted_sigmoid, sigmoid_X, sigmoid_y)


# In[104]:


def plot_sigmoid(df, sigmoid_X, sigmoid_y, inflection_x, inflection_y):

    X = df['Dag'].values.reshape(-1, 1)
    y = df['Aantal'].values.reshape(-1, 1)
    
    plt.figure(figsize=(15,10))

    plt.plot(X, 
             y, 
             linestyle='', 
             marker='.', 
             label="bevestigde aantallen")

    plt.plot(sigmoid_X,
             sigmoid_y,
             linestyle='-',         
             color='green', 
             label='logistische fit'
            )

    plt.plot([inflection_x], 
             [inflection_y], 
             marker='+', 
             linestyle='none',
             color='black', 
             label='inflectiepunt',
             markersize=10
            )

    plt.xlabel("Datum", size=15)
    plt.ylabel("Aantal gevallen", size=15)
    plt.title("Logistische curve gefit o.b.v. inflectiepunt", size=20)
    plt.legend(fontsize=20)

    min_x_val = 0
    max_x_val = int(max(sigmoid_X))
    
    labels = np.arange(max_x_val+1)
    labels = [df.index.min() + pd.Timedelta("{} day".format(l)) for l in labels]
    labels = ["{:%d/%m/%Y}".format(l) for l in labels]
    
    plt.xticks(ticks = np.arange(max_x_val+1),
               labels=labels,
               rotation=60)

    
    # plt.show()
    
    plt.savefig("plots/sigmoid.png")

    # plt.xticks(df.index, rotation=60)


# In[105]:


if __name__ == "__main__":

    df = read_data()

    df = add_variables(df)

    intercepts, coefficients = analyze_growth_factor(df)

    inflection_x, inflection_date = compute_inflection_point(df, intercepts, coefficients)

    print("Inflection expected after {:.1f} days, at date {:%d/%m/%Y %H:00}".format(inflection_x, inflection_date))

    create_growthfactor_plot(df, intercepts, coefficients, inflection_date)

    inflection_y = compute_inflection_cases(df, inflection_x)

    fitted_sigmoid, sigmoid_X, sigmoid_y = fit_sigmoid(df, inflection_x, inflection_y)

    plot_sigmoid(df, sigmoid_X, sigmoid_y, inflection_x, inflection_y)

