# -*- coding: utf-8 -*-
"""
Created on Sat Dec 10 11:55:21 2016

@author: Michael, Zeng
"""
# This file was tested on Dec 15, 2016, Thursday. 
# It ran w/t error if csv files 'asset.csv' and 'factor.csv' are provided. 

import numpy as np
import pandas as pd
import scipy as sp
import statsmodels.api as sm
import matplotlib.pyplot as plt
# import statsmodels.formula.api as smf
# from pandas.stats.api import ols # to be removed in a future release

# Set path of modified csv files (change cell format in xlsx and save as csv)
path = 'C:\Users\zzeng\Downloads\Calculation\\'
file_asset = 'asset.csv'
file_factor = 'factor.csv'
# file_summary_each = 'rg_summary_each.txt'
# file_summary_all = 'rg_summary_all.txt'
# file_summary_prtl = 'rg_summary_prtl.txt'

# File Functions
# Create a new file
def new_file (path_file,name_file):
    _file=pd.DataFrame([])
    _file.to_csv( path_file + name_file) 
    
# Run regression & save result
def reg_save( yi, xj, f):
    # yi: dependent variable, xi: independent variable(s), f: file handle
    model_reg = sm.OLS( yi, xj)
    results = model_reg.fit()

    f.write (results.summary().as_text())
    f.write ('\n \n \n \n \n')


# Function to Calculate Performance Parameter
# Function to Calculate Sharp Ratio
def sharp (ret, bmark):
    i_ex_ret = np.mean(ret - bmark) # excess return = r(Asset) - r(BenchMark)
    i_vol = np.var(ret ) # Volatility of asset
    sr = i_ex_ret / i_vol # Sharp ratio = excess return / Volatility of asset
    return sr
    
# Function to Calculate Adjusted Sharp Ratio
def adj_sharp(ret, bmark):
    i_ex_ret = np.mean(ret - bmark) # excess return = r(Asset) - r(BenchMark)
    i_vol = np.var(ret ) # Volatility of asset
    sr = i_ex_ret / i_vol # Sharp ratio = excess return / Volatility of asset

    s = sp.stats.skew(ret) # calculate skewness
    k = sp.stats.kurtosis(ret) # calculate kurtosis
    return sr * (1 + s/6*sr - (k-3)/24*sr**2.0)
   
# Function to Calculate VaR and CVaR 
# Function to Calculate VaR, ret - NumPy array, alpha - confidence level
def valatrisk(ret, alpha): 
    if alpha > 0.5:
        alpha = 1 - alpha
    ret_size = ret.size
    loc = int(ret_size * alpha)
    ret_sort = np.sort(ret)
    return ret_sort[loc]
    
# Function to Calculate CVaR/ES, ret - NumPy array, alpha - confidence level
def cvar(ret, alpha):
    if alpha > 0.5:
        alpha = 1 - alpha
    ret_size = ret.size
    loc = int(ret_size * alpha)
    ret_sort = np.sort(ret)
    return np.mean(ret_sort[:loc])
    
# Main Script
# Read csv files into Pandas Dataframe
asset = pd.read_csv( path + file_asset, usecols=range(1,6), dtype =  np.float64) 
factor = pd.read_csv( path + file_factor, usecols = range(1,27), dtype =  np.float64)
# Fit NaN in Dataframe
asset = asset.fillna(method = 'backfill') 
factor = factor.fillna(method = 'backfill') 
# View Data Type
# asset.dtypes
# factor.dtypes

# Calculate Sharp Ratio and Adjusted Sharp Ratio
sr = [] # NumPy array containing sharp ratio of 5 assets
asr = [] # NumPy array containing adjusted sharp ratio of 5 assets
bmark = factor['S&P500'].as_matrix()
for i in range(0,5):  
    ret = asset.iloc[:, i].as_matrix()    
    sr = np.append(sr, sharp (ret, bmark))
    asr = np.append(asr, adj_sharp(ret, bmark))
# pd.DataFrame(sr, index = ['Sharp_Ratio'], columns = ['Asset1','Asset2','Asset3','Asset4','Asset5'])

# Other Performance Parameters to Be Added



# VaR and CaR
alpha5 = 0.05
alpha1 = 0.01
VaR5 = []
VaR1 = []
CVaR5 = []
CVaR1 = []
for i in range (0, 5):
    ret = asset.iloc[:, i].as_matrix() # get return numpy array 
    VaR5 = np.append (VaR5, valatrisk(ret, alpha5)) # calculate 5% VaR
    VaR1 = np.append (VaR1, valatrisk(ret, alpha1)) # calculate 1% VaR
    CVaR5 = np.append (CVaR5, cvar(ret, alpha5)) # calculate 5% CVaR
    CVaR1 = np.append (CVaR1, cvar(ret, alpha1)) # calculate 1% CVaR
    
# Variance Covariance Matrix
covvar = pd.DataFrame.cov(asset)
corr_ast = pd.DataFrame.corr(asset)
corr_fct = pd.DataFrame.corr(factor)
    
# Regression on Factors
# All factors regressed on each asset
para_val = pd.DataFrame() # parameter values
t_sta = pd.DataFrame() # t statistic
p_val = pd.DataFrame() # p-value
for i in range(0,5):
    yi = asset.ix[:,i]
    xj = factor.ix[:,:]
    model_reg = sm.OLS( yi, xj)
    results = model_reg.fit()
    
    para_val = pd.concat([para_val, results.params], axis=1)
    t_sta = pd.concat([t_sta, results.params], axis=1)
    p_val = pd.concat([p_val, results.pvalues], axis=1)

col_name_ast = ['Asset1','Asset2','Asset3','Asset4','Asset5'] 
para_val.columns = col_name_ast
t_sta.columns = col_name_ast
p_val.columns = col_name_ast

# Plot


