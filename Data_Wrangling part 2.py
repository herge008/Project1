#!/usr/bin/env python
# coding: utf-8

# In[1]:


import requests
import os
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time


# In[2]:


csvpath=os.path.join("Resources","MovieData_Clean.csv")
movie_df=pd.read_csv(csvpath)


# In[3]:


movie_df


# In[4]:


movie_df["Runtime (Min)"]=None


# In[5]:


f = open(os.path.join("ErrorLogs","Data_Clean_Error_Log.txt"), "a")
for index, row in movie_df.iterrows():
    try:
        movie_df.loc[index,"Runtime (Min)"]=int(row["Runtime"].split(' min')[0])
    except:
        f.write(f"There was a problem removing minutes on movie with the TMDB ID {row['TMDB ID']}\n")
f.close()


# In[6]:


movie_df


# In[7]:


movie_df.loc[movie_df["Year of Release"]<2019]


# In[8]:


movie_df


# In[9]:


# error=pd.read_csv("ErrorLogs/Data_Clean_Error_Log.txt")
error_frame=pd.DataFrame()
with open("ErrorLogs/Data_Clean_Error_Log.txt", 'r') as file:
    for line in file:
        mid=int(line.split()[-1])
#         print(mid)        
        error_frame=error_frame.append(movie_df.loc[movie_df["TMDB ID"]==int(mid)])


# In[10]:


error_frame


# In[11]:


movie_df.loc[3004,"Runtime (Min)"]=85


# In[13]:


movie_df=movie_df[(movie_df.Rating !="12") & (movie_df.Rating !="Approved") & (movie_df.Rating !="NOT RATED") & (movie_df.Rating !="Not Rated") & (movie_df.Rating !="TV-13") & (movie_df.Rating !="TV-14") & (movie_df.Rating !="TV-G") & (movie_df.Rating !="TV-MA") & (movie_df.Rating !="TV-PG") & (movie_df.Rating !="TV-Y") & (movie_df.Rating !="TV-Y") & (movie_df.Rating !="TV-Y7") & (movie_df.Rating !="UNRATED") & (movie_df.Rating !="Unrated")]
# print(movie_df.loc[movie_df["Rating"]=="GP"])
movie_df.loc[1658,"Rating"]="PG"
grouped_movie_rating=movie_df.groupby(["Rating"]).count()
grouped_movie_rating


# In[26]:


q75,q25=np.percentile(movie_df["Revenue"],[75,25])
inf_iqr=q75-q25
upperbound=q75+(1.5*inf_iqr)
lowerbound=q25-(1.5*inf_iqr)
q25
movie_df=movie_df.loc[movie_df["Revenue"]>q25]


# In[31]:


movie_df=movie_df.copy()
movie_df["Primary Genre"]=None
for index, row in movie_df.iterrows():
    movie_df.loc[index,"Primary Genre"]=str(row["Genre"]).split(",")[0]
movie_df.loc[294,"Primary Genre"]="Drama"
movie_df.loc[2358,"Primary Genre"]="Action"


# In[32]:


movie_df


# In[33]:


movie_df.to_csv(os.path.join("Resources","MovieData_Clean.csv"),index=False)


# In[ ]:




