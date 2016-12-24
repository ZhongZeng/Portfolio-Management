# -*- coding: utf-8 -*-
"""
Created on Sat Oct 22 22:58:56 2016
Python 2.7 - Spyder
@author: Zhong (Michael) Zeng
from Forhdam University
"""

import numpy as np
import pandas as pd
import statsmodels.api as sm
# import statsmodels.formula.api as smf
# from pandas.stats.api import ols # to be removed in a future release

# Set path of modified csv files (change cell format in xlsx and save as csv)
path = 'F:\Michael\Fordham_University\Taken\Quant_Mtd_Ptfl_Mgt\HW2\\'
file_asset = 'asset.csv'
file_factor = 'factor.csv'
file_summary_each = 'rg_summary_each.txt'
file_summary_all = 'rg_summary_all.txt'
file_summary_prtl = 'rg_summary_prtl.txt'

# Functions
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
    

# Read csv files into Pandas Dataframe
asset = pd.read_csv( path + file_asset, usecols=range(1,6), dtype =  np.float64)
factor = pd.read_csv( path + file_factor, usecols = range(1,27), dtype =  np.float64)
# Fit NaN in Dataframe
# asset = asset.fillna(method = 'ffill') 
factor = factor.fillna(method = 'backfill') 
# asset.dtypes
# factordtypes

# One-factor regressed on each asset
new_file (path, file_summary_each)
f = open( path + file_summary_each, 'w')

for i in range(0,5):
    for j in range(0,26):
        yi = asset.ix[:,i]
        xj = factor.ix[:,j]
        reg_save( yi, xj, f)

f.close()

# All factors regressed on each asset
new_file (path, file_summary_all)
f = open( path + file_summary_all, 'w')

for i in range(0,5):
    yi = asset.ix[:,i]
    xj = factor.ix[:,:]
    reg_save( yi, xj, f)

f.close()

# All factors regressed on equally weighted assets

new_file (path, file_summary_prtl)
f = open( path + file_summary_prtl, 'w')

yi = 0.2 * asset.ix[:,0]
for i in range(1,5):
    yi = yi + 0.2 * asset.ix[:,i]
xj = factor.ix[:,:]
reg_save( yi, xj, f)

f.close()
