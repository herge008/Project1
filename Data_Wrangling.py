# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import requests
import os
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time


# %%
csvpath=os.path.join("Resources","MovieData_PreCleanup.csv")
movie_df=pd.read_csv(csvpath)


# %%
movie_df


# %%
movie_df_copy=movie_df.copy()
movie_df_copy["Day of Release"]=None
movie_df_copy["Month of Release"]=None
movie_df_copy["Year of Release"]=None
for index, row in movie_df_copy.iterrows():    
    movie_df_copy.loc[index,"Day of Release"]=datetime.strptime(row["Release Date"], "%Y-%m-%d").strftime('%A')
    movie_df_copy.loc[index,"Month of Release"]=datetime.strptime(row["Release Date"], "%Y-%m-%d").strftime('%B')
    movie_df_copy.loc[index,"Year of Release"]=datetime.strptime(row["Release Date"], "%Y-%m-%d").strftime('%Y')


# %%
movie_df_copy.count()


# %%
movie_df_cleaned=movie_df_copy.loc[(movie_df_copy['Revenue']!=0)& (pd.notnull(movie_df_copy['Revenue']))]
movie_df_cleaned=movie_df_cleaned.copy()
movie_df_cleaned["Revenue (Millions)"]=movie_df_cleaned["Revenue"]/1000000
movie_df_cleaned=movie_df_cleaned.loc[movie_df_copy['Type']=='movie']
movie_df_cleaned["Release Date"]=pd.to_datetime(movie_df_cleaned["Release Date"])
movie_df_cleaned.drop(['Box Office', 'Type', 'Unnamed: 0','Rating Dictionary','Metascore'], axis=1, inplace=True)
movie_df_cleaned.sort_values(["Release Date"],inplace=True)
movie_df_cleaned["Budget"].value_counts()


# %%
movie_df_cleaned.to_csv(os.path.join("Resources","MovieData_Clean.csv"),index=False)


# %%



