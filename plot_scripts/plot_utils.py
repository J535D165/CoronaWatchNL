import pandas as pd
import numpy as np

import math

import matplotlib.pyplot as plt

from sklearn.linear_model import LinearRegression


def read_data(filename, region, boolean_region):
    
    # Read and preprocess data file
    df = pd.read_csv(filename)

    df['Datum'] = pd.to_datetime(df['Datum'])

    df = df.set_index('Datum')
        
    df['Dag'] = np.arange(len(df))

    if (boolean_region):
        # If a region is used then filter on the region first.
        df_filtered = df[(df['Provincienaam'] == region)]
        df_filtered['Dag'] = np.arange(len(df_filtered))
        return (df_filtered)
    else:
        return (df)  


def add_variables(df):
    
    # New cases
    df['New_cases'] = df['Aantal'] - df['Aantal'].shift(1)

    # Groeifactor
    df['Growth_factor'] = df['New_cases'] / df['New_cases'].shift(1)    
    
    return(df)


def analyze_growth_factor(df):

    ## regression analysis of growth factor

    df = df[~df.isin([np.nan, np.inf, -np.inf]).any(1)] # remove inf values
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

def create_growthfactor_plot(df,
                             intercepts,
                             coefficients,
                             inflection_date,
                             filename,
                             subject,
                             plot_max_bootstraps=50):

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
    plt.title("Groeifactor " + subject + "(delta nieuwe cases), maximum groei verwacht op {:%d/%m/%Y %H:00}".format(inflection_date), 
              size=20)
    plt.legend(fontsize=20)

    plt.savefig(filename)


# %%
def create_logarithmic_growth_plot(df):
    # Setup Object Oriented plot because we re-use this function
    fig, ax = plt.subplots(figsize=(15,10))
    ax.set(xscale="log", yscale="log", )
    ax.set_xlabel("Totaal cases", fontsize=15)
    ax.set_ylabel("Nieuwe cases", fontsize=15)

    ax.grid(which='major', linewidth=1)
    ax.grid(which='minor', linewidth=0.1)

    ax.plot(df['Aantal'], df["New_cases"])
    
    return fig,ax


# %%
def plot_logarithmic_growth_daily(df, subject, filename):
    fig, ax = create_logarithmic_growth_plot(df)
    ax.set(title="Nieuwe cases " + subject + "tegen totaal cases (dagelijks)")
    fig.savefig(filename)


# %%
def plot_logarithmic_growth_bi_daily(_df, subject, filename):
    df = _df.copy()
    df = df.reset_index(level=0)
    df = df[['Aantal', 'Datum', 'New_cases']]
    df = df.resample('2d', on='Datum', closed='right').sum()
    fig, ax = create_logarithmic_growth_plot(df)
    ax.set(title="Nieuwe cases " + subject +"tegen totaal cases (2-dagelijks)")

    fig.savefig(filename)

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
    if inflection_x < df['Dag'].max():

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
from numpy.random import seed

def sigmoid(t, alpha, beta, M):
    
    y = M / (1 + np.exp(-beta*(t-alpha)))
    return y

def fit_sigmoid(df):

    X = df['Dag'].values
    y = df['Aantal'].values

    popt, pcov = curve_fit(sigmoid, X, y/max(y))

    fitted_sigmoid = lambda k : sigmoid(k, *popt) * max(y)

    return (fitted_sigmoid)

def fit_sigmoid_repeated(df, no_samples=50):
    
    fitted_sigmoids = []
    
    for i in range(no_samples):
        
        df_resampled = df.sample(frac=1,
                                 replace=True,
                                 random_state=i
                                )
        
        seed(2*i) #deterministic curve fitting? 
        
        fitted_sigmoid = fit_sigmoid(df_resampled)
        
        fitted_sigmoids.append(fitted_sigmoid)
        
    return(fitted_sigmoids)


# In[104]:
def plot_sigmoids(df,
                  fitted_sigmoid,
                  fitted_sigmoids,
                  filename,
                  subject,
                  extrapolate_days=7):

    X = df['Dag'].values.reshape(-1, 1)
    y = df['Aantal'].values.reshape(-1, 1)
    
    plt.figure(figsize=(15,10))

    plt.plot(X, 
             y, 
             linestyle='', 
             marker='.',
             markersize='10',
             color='black',
             label="aantal "+ subject)
   
    X_linspace = np.linspace(X.min(), X.max()+extrapolate_days, num=100)
    
    for fs in fitted_sigmoids:
        
        y_sigmoid = fs(X_linspace)
        
        if np.std(y_sigmoid) > 10: # some sigmoids are just lines (prob because of sampling low no. of points)
        
            plt.plot(X_linspace,
                     y_sigmoid,
                     linestyle='-',         
                     color='blue', 
                     alpha=0.10
                    )    
    
    plt.plot(X_linspace,
             fitted_sigmoid(X_linspace),
             linestyle='-',         
             color='blue', 
             label='logistische fit',
            )

    plt.xlabel("Datum", size=15)
    plt.ylabel("Aantal gevallen", size=15)
    plt.title("Logistische curve " + subject, size=20)
    plt.legend(fontsize=20)

    max_x_val = X.max()+extrapolate_days
    
    labels = np.arange(max_x_val+1)
    labels = [df.index.min() + pd.Timedelta("{} day".format(l)) for l in labels]
    labels = ["{:%d/%m/%Y}".format(l) for l in labels]
    
    plt.xticks(ticks = np.arange(max_x_val+1),
               labels=labels,
               rotation=60)

    plt.ylim(0)

    plt.savefig(filename)

# In[104]:
def process_plots(subject,
                  data_filename,
                  growth_factor_plot_filename,
                  sigmoiod_plot_filename,
                  exponential_plot_filename,
                  exponential_bi_plot_filename,
                  region,
                  boolean_region
                 ):

    df = read_data(data_filename, region, boolean_region)

    df = add_variables(df)

    intercepts, coefficients = analyze_growth_factor(df)

    inflection_x, inflection_date = compute_inflection_point(df, intercepts, coefficients)

    print("Inflection expected after {:.1f} days, at date {:%d/%m/%Y %H:00}".format(inflection_x, inflection_date))

    create_growthfactor_plot(df,
                             intercepts,
                             coefficients,
                             inflection_date,
                             growth_factor_plot_filename,
                             subject)

    fitted_sigmoid = fit_sigmoid(df)

    fitted_sigmoids = fit_sigmoid_repeated(df)

    plot_sigmoids(df,
                  fitted_sigmoid,
                  fitted_sigmoids,
                  sigmoiod_plot_filename,
                  subject)

    if (not boolean_region):
        plot_logarithmic_growth_daily(df,
                                    subject,
                                    exponential_plot_filename)
        plot_logarithmic_growth_bi_daily(df,
                                        subject,
                                        exponential_bi_plot_filename)