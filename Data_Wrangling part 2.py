# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import requests
import os
import pandas as pd
from pprint import pprint
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime as date
import time
from api_keys import rapid_key, moviedb_key, omdb_key

# %% [markdown]
# # Data Pulls

# %%
# The Movie DB data pull

tmdb_url="https://api.themoviedb.org/3/discover/movie?"
params={
    "api_key":moviedb_key,
    "primary_release_date.gte":"2005-01-01",
    "sort_by":"primary_release_date.desc",
    "primary_release_date.lte":"2020-01-01",
    "region":"US",
    "with_release_type":"2,3",
    "language":"en-US"
}
movie_ids=[]
movie_titles=[]
movie_dates=[]
page=1

# set first year to pull movies from

year=2008

# open error log document

f = open(os.path.join("ErrorLogs","TMDB_Pull_Error_Log.txt"), "a")

# Repeat the api ping for each year

while year<=2019:
    start_date=f"{year}-01-01"
    end_date=f"{year+1}-01-01"
    params["primary_release_date.gte"]=start_date
    params["primary_release_date.lte"]=end_date
    
    # Repeat the api ping for each page in the query because each ping only returns 20 results
    
    if (page==1):
        params["page"]=page
        response = requests.get(tmdb_url, params=params).json()
        page_max=response["total_pages"]
      
        for movie in response["results"]:
            try:
                movie_ids.append(movie["id"])
                movie_titles.append(movie["title"])
                movie_dates.append(movie["release_date"])
                print(movie["id"])
            except(TypeError):                
                f.write(f'Missing information on page {page}\n')
        page=page+1
    while page<=page_max:
        params["page"]=page
        response = requests.get(tmdb_url, params=params).json()

        for movie in response["results"]:
            try:
                movie_ids.append(movie["id"])
                movie_titles.append(movie["title"])
                movie_dates.append(movie["release_date"])
                print(movie["id"])
            except(TypeError):                    
                f.write(f'Missing information on page {page}\n')

        page=page+1
 
    page=1
    
    year=year+1
f.close()     


# %%
# Create the Initial Data Frame to use to pull from OMDB and export the data to a csv file

Movie_df=pd.DataFrame({"TMDB ID":movie_ids,"Title":movie_titles,"Release Date":movie_dates})
export_file_path=os.path.join("Resources","MovieTitles.csv")
Movie_df.to_csv(export_file_path)


# %%
# Get budget information from TMDB for each movie in the list
Movie_df["Budget"]=None
Movie_df["Revenue"]=None
tmdb_detailed_url="https://api.themoviedb.org/3/movie/"
params={
    "api_key":moviedb_key
}
f = open(os.path.join("ErrorLogs","TMDB_BudgetPull_Error_Log.txt"), "a")
for index, row in Movie_df.iterrows():
    tmdb_id=str(row['TMDB ID'])
    response=requests.get(tmdb_detailed_url+tmdb_id+"?",params=params).json()
    try:    
        Movie_df.loc[index,"Budget"]=response["budget"]
        Movie_df.loc[index,"Revenue"]=response["revenue"]
    except:
        f.write(f'There was a problem pulling data for {tmdb_id}:{row["Title"]}\n')
#     print(row['TMDB ID'])
f.close()
Movie_df


# %%
# Add Necessary Columns to data frame in order to stor additional info
export_file_path=os.path.join("Resources","MovieTitlesAndBudgets.csv")
Movie_df.to_csv(export_file_path)
Movie_df["IMDB ID"]=None
Movie_df["Rating"]=None
Movie_df["Runtime"]=None
Movie_df["Genre"]=None
Movie_df["Director"]=None
Movie_df["Writer"]=None
Movie_df["Actors"]=None
Movie_df["Plot"]=None
Movie_df["Language"]=None
Movie_df["Country"]=None
Movie_df["Awards"]=None
Movie_df["Poster"]=None
Movie_df["IMDB Rating"]=None
Movie_df["IMDB Votes"]=None
Movie_df["Metascore"]=None
Movie_df["Rating Dictionary"]=None
Movie_df["Type"]=None
Movie_df["DVD Release Date"]=None
Movie_df["Box Office"]=None
Movie_df["Production"]=None


# %%
# OMDB API Data Pull

omdb_url="http://www.omdbapi.com/?"
params={
    "apikey":omdb_key
}

# pulls determines how many rows i want to iterate through. This is for testing purposes and will be removed in the 

i=1
pulls=100000
f = open(os.path.join("ErrorLogs","IMDB_Pull_Error_Log.txt"), "a")
for index,row in Movie_df.iterrows():
    params["t"]=row["Title"]
    try:
        response=requests.get(omdb_url, params=params).json() 

        Movie_df.loc[index,"Rating"]=response["Rated"]
        Movie_df.loc[index,"Runtime"]=response["Runtime"]
        Movie_df.loc[index,"Genre"]=response["Genre"]
        Movie_df.loc[index,"Director"]=response["Director"]
        Movie_df.loc[index,"Writer"]=response["Writer"]
        Movie_df.loc[index,"Actors"]=response["Actors"]
        Movie_df.loc[index,"Plot"]=response["Plot"]
        Movie_df.loc[index,"Language"]=response["Language"]
        Movie_df.loc[index,"Country"]=response["Country"]
        Movie_df.loc[index,"Awards"]=response["Awards"]
        Movie_df.loc[index,"Poster"]=response["Poster"]
        Movie_df.loc[index,"IMDB Rating"]=response["imdbRating"]
    #     Movie_df.loc[index,"Metascore"]=response[""]
    #     Movie_df.loc[index,"Rating Dictionary"]=response["Ratings"]
        Movie_df.loc[index,"IMDB ID"]=response["imdbID"]
        Movie_df.loc[index,"IMDB Votes"]=response["imdbVotes"]
        Movie_df.loc[index,"Type"]=response["Type"]
        Movie_df.loc[index,"DVD Release Date"]=response["DVD"]
#         Movie_df.loc[index,"Box Office"]=response["BoxOffice"]
        Movie_df.loc[index,"Production"]=response["Production"]
    except:

        f.write(f"There was a problem with movie {row['TMDB ID']}\n")

                
    #checks to see if the max number of pulls was reached and breaks out of the for loop if they have been
                
    if(i==pulls):
        break
    i=i+1

f.close()   

# %% [markdown]
# # Data Pull Complete: Data Wrangling Begins Now

# %%



# %%
# Export the file

Movie_df.to_csv(os.path.join("Resources","MovieData_PreCleanup.csv"))


# %%



