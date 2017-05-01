#!/usr/bin/env python2
# -*- coding: utf-8 -*-
"""
Created on Sun Apr 30 20:02:17 2017

@author: Prafull
"""

import numpy as np
import pandas as pd
Rank_District=pd.read_csv('/Users/Prafull/Desktop/SocialCops/Submission/final.csv')

data=Rank_District.loc[:,'Income greater than 10000(%)':]

# Extracting only the data values (Removing district and variable names)
data_values=np.array(data.values)

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA as sklearnPCA

# Standardizing Variables
data_values_std = StandardScaler().fit_transform(data_values)

sklearn_pca = sklearnPCA(n_components=25)

sklearn_pca.fit_transform(data_values_std)

pc_explain_percentage=sklearn_pca.explained_variance_ratio_
pc_total_explained_percentage=sum(pc_explain_percentage)

pc1=sklearn_pca.components_[0]
pc2=sklearn_pca.components_[1]
pc3=sklearn_pca.components_[2]
pc4=sklearn_pca.components_[3]
pc5=sklearn_pca.components_[4]
factor1=[]
factor2=[]
factor3=[]
factor4=[]
factor5=[]
# Terminology ''Factor scores''  used instead of 'Component Scores'
# Calculating Factor scores 1,2,3,4,5 for each District
# Multiplying standardized variable values for each district to corresponding factor loading(Principal Component)
for row in data_values_std:
    fac1=float(sum(row*pc1))
    fac2=float(sum(row*pc2))
    fac3=float(sum(row*pc3))
    fac4=float(sum(row*pc4))
    fac5=float(sum(row*pc5))
    factor1.append(fac1)
    factor2.append(fac2)
    factor3.append(fac3)
    factor4.append(fac4)
    factor5.append(fac5)
factor1=np.array(factor1)
factor2=np.array(factor2)
factor3=np.array(factor3)
factor4=np.array(factor4)
factor5=np.array(factor5)

# Calculating Non Standardized Index
proportion_explained_among_factors=pc_explain_percentage/pc_total_explained_percentage
NSI=factor1*proportion_explained_among_factors[0]+factor2*proportion_explained_among_factors[1] \
                +factor3*proportion_explained_among_factors[2]+factor4*proportion_explained_among_factors[3]+factor5*proportion_explained_among_factors[4]

max_nsi=max(NSI)
min_nsi=min(NSI)
NSI_test=NSI
NSI=NSI-min_nsi
NSI=NSI/(max_nsi-min_nsi)
SI=NSI*100  #Standardized Index

#  Processing Index , making index more interpretable
index=[]
for row in SI:
    index.append(row)

index=100-np.array(index) # Subtracting from 100 to make the index more interpretable,
                          # Higher the index, more developed the district

# Adding index to main dataframe
Rank_District['index']=pd.Series(index,Rank_District.index)
     
final_df=Rank_District.loc[:,['District','index']]

final_df=final_df.sort_values(['index'], ascending=False)

# Adding a new column Rank to the result dataframe
final_df['rank']=pd.Series(range(1,31),final_df.index)

# Changing the index of the dataframe to counter the affect of sorting
final_df.index=np.arange(1,len(final_df)+1)
final_df.loc[30,'index']=1.0  #Assigning the least index as 1 instead of 0.0 to be able to better visualize this point
final_df.to_csv('final_result.csv')
final_df






