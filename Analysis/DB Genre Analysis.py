#!/usr/bin/env python
# coding: utf-8

# In[1]:


import os
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import time


# In[2]:


csvpath=os.path.join("..","Resources","MovieData_Clean.csv")
movie_df=pd.read_csv(csvpath)


# In[3]:


movie_df


# In[4]:


grouped_movie_rating=movie_df.groupby(["Rating"]).min()
grouped_movie_rating


# # Determine the Highest Earning Genres NOT taking subgenres into account

# In[5]:


movie_df=movie_df[movie_df["Primary Genre"]!="Short"]
movie_df=movie_df.copy()
grouped_movie_df=movie_df.groupby(["Primary Genre"])
average_df=grouped_movie_df.mean().sort_values("Revenue (Millions)")
average_df


# In[80]:


# Plot the average revenue in millions for each primary genre
plt.bar(average_df.index.values,average_df["Revenue (Millions)"])
plt.title("Total Primary Genre Earnings")
plt.xticks(rotation=90)
plt.ylabel("Revenue (Millions $)")
imagepath=os.path.join("..","Images",f"BarPlot_TotalGenre_Revenue.png")
plt.savefig(imagepath)
plt.show()


# In[7]:


# movie_df=movie_df.sort_values("Year of Release")
# movie_df
# grouped_movie_df=movie_df.groupby(["Primary Genre","Year of Release"])
# grouped_movie_df.count()


# # Determine the Highest earning Genres taking subgenres into account

# In[8]:


# Create a dataframe that accounts for each genre a movie holds
temp_df=pd.DataFrame()
index_counter=movie_df.index.max()+1
for index,row in movie_df.iterrows():
    
    for genre in row["Genre"].split(", "):
        if row["Primary Genre"]!= genre:
            new_row=row
            new_row["Primary Genre"]=genre
            new_row=new_row.to_frame().T
            new_row.reset_index(drop=True,inplace=True)
            new_row["new index"]=index_counter
            temp_df=temp_df.append(new_row)
            index_counter+=1
    


# In[9]:


temp_df.set_index('new index',drop=True,inplace=True)


# In[10]:


movie_df["new index"]=movie_df.index.values
movie_df.set_index("new index", inplace=True,drop=True)


# In[11]:


#Combine the 2 dataframes
split_genre_df=movie_df.append(temp_df,sort=True)
split_genre_df=split_genre_df.loc[(split_genre_df["Primary Genre"]!="News")]
split_genre_df=split_genre_df.loc[(split_genre_df["Primary Genre"]!="Adult")]
split_genre_df=split_genre_df.loc[(split_genre_df["Primary Genre"]!="Short")]
split_genre_df.loc[split_genre_df["Primary Genre"]=="Music"]
split_genre_df


# In[12]:


split_genre_df["Revenue (Millions)"]=split_genre_df["Revenue (Millions)"].astype(float)
split_genre_df["Year of Release"]=split_genre_df["Year of Release"].astype(int)
grouped_frame=split_genre_df.groupby(["Primary Genre"]).mean().sort_values("Revenue (Millions)")
# grouped_frame=grouped_frame.drop(index=["News","Adult","Short"])
grouped_frame


# In[79]:


plt.bar(grouped_frame.index.values,grouped_frame["Revenue (Millions)"])
plt.title("Total Genre/Subgenre Earnings")
plt.xticks(rotation=90)
plt.ylabel("Revenue (Millions $)")
imagepath=os.path.join("..","Images",f"BarPlot_TotalGenreandSubs_Revenue.png")
plt.savefig(imagepath)
plt.show()


# # See if the season affects the Genre earnings

# In[56]:


# Insert a season for each row in original data frame and split genre dataframe
spring=["March","April","May"]
summer=["June","July","August"]
fall=["September","October","November"]
winter=["December","January","February"]
split_genre_df["Season"]=None
movie_df["Season"]=None
for index,row in split_genre_df.iterrows():
    if(row["Month of Release"] in summer):
        split_genre_df.loc[index,"Season"]="Summer"
    elif(row["Month of Release"] in spring):
        split_genre_df.loc[index,"Season"]="Spring"
    elif(row["Month of Release"] in winter):
        split_genre_df.loc[index,"Season"]="Winter"
    elif(row["Month of Release"] in fall):
        split_genre_df.loc[index,"Season"]="Fall"
        
for index,row in movie_df.iterrows():
    if(row["Month of Release"] in summer):
        movie_df.loc[index,"Season"]="Summer"
    elif(row["Month of Release"] in spring):
        movie_df.loc[index,"Season"]="Spring"
    elif(row["Month of Release"] in winter):
        movie_df.loc[index,"Season"]="Winter"
    elif(row["Month of Release"] in fall):
        movie_df.loc[index,"Season"]="Fall"


# In[87]:


# Function to plot the seasonal genre earnings. Takes the season and the dataframe you are working with.
def seasonalPlot(season,split=False):
    subtitle=""
    if split:
        subtitle='andSub'
        var_df=split_genre_df
    else:
        var_df=movie_df
    df=var_df[var_df["Season"]==season]
    df=df.sort_values("Revenue (Millions)")
    df=df.groupby(["Primary Genre"])["Revenue (Millions)"].median().sort_values()
#     df.drop("Year of Release",axis=1,inplace=True)
    bar=df.plot.bar()
    plt.title(f"Genre vs. Median Revenue in the {season}")
    plt.ylabel("Revenue (Millions)")
    plt.xlabel("Genre")
    plt.show()
    
    
    imagepath=os.path.join("..","Images",f"BarPlot_{season}_Genre{subtitle}_Revenue.png")
    fig = bar.get_figure()
    fig.savefig(imagepath)


# In[88]:


seasonalPlot("Fall")
seasonalPlot("Summer")
seasonalPlot("Spring")
seasonalPlot("Winter")
print("All genres included Below")
seasonalPlot("Fall",True)
seasonalPlot("Summer",True)
seasonalPlot("Spring",True)
seasonalPlot("Winter",True)


# In[ ]:





# In[ ]:




