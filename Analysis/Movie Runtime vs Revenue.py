# To add a new cell, type '# %%'
# To add a new markdown cell, type '# %% [markdown]'
# %%
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os


# %%
# Read csv data file
file_path = "../Resources/MovieData_Clean.csv"
movie_data = pd.read_csv(file_path)
movie_data


# %%
# Drop blanks (Runtime) and TV movies (Rating)
# Sort movie runtime from shortest to longest
movie_data = movie_data.dropna(subset=['Runtime (Min)'])
movie_data = movie_data[~movie_data['Rating'].isin(['TV'])]
sort_time = movie_data.sort_values("Runtime (Min)")

# Identify how I want cut the bins
max = sort_time["Runtime (Min)"].max()
min = sort_time["Runtime (Min)"].min()
print(f"The longest movie runtime is {max} mins.")
print(f"The shortest movie runtime is {min} mins.")


# %%
# Identify runtime outliers
Q1 = np.percentile(sort_time['Runtime (Min)'], 25)
print("(Q1) Lower Quartile: %s"%(Q1))

Q2 = np.percentile(sort_time['Runtime (Min)'], 50)
print("(Q2) Median: %s"%(Q2))

Q3 = np.percentile(sort_time['Runtime (Min)'], 75)
print("(Q3) Upper Quartile: %s"%(Q3))

IQR = Q3 - Q1
print("Interquartile Range: %s"%(IQR))

upper_boundary = Q3 + (1.5 * IQR)
print("Upper Boundary: %s"%(upper_boundary))

lower_boundary = Q1 - (1.5 * IQR)
print("Lower Boundary: %s"%(lower_boundary))

# Remove any outliers (lower boundary)
sort_time = sort_time[sort_time['Runtime (Min)']>= lower_boundary]
sort_time


# %%
# Organize movie runtimes to bins
bins = [0, 60, 90, 120, 180, 240]
group_names = ["0-60mins", "60-90mins", "90-120mins", "120-180mins", "180-240mins"]
colors = ["red", "yellow", "blue", "green", "orange"]
sort_time["Movies Runtime Grouped(Mins)"] = pd.cut(sort_time["Runtime (Min)"], bins, labels=group_names)
sort_time
                                            


# %%
# Create a bar plot to show most common movie run time
time_counts = sort_time["Movies Runtime Grouped(Mins)"].value_counts(sort=False)
df_val_counts = pd.DataFrame(time_counts)
df_val_counts = df_val_counts.reset_index()
df_val_counts.columns = ['Runtime Grouped', 'Counts']
print(df_val_counts)


colors = ["red", "orange", "green", "blue", "yellow"]
explode = (0.5, 0, 0.2, 0, 0)
fig = plt.figure()
plt.pie(df_val_counts["Counts"], explode=explode, labels=group_names, colors=colors,
        autopct="%1.1f%%", shadow=True, startangle=140, radius=1)
plt.title("Movie Runtime (2008-2018)")
plt.tight_layout()

plt.show()

save_file = os.path.join("..", "Images", "Movie Runtime Pie Chart.png")
fig.savefig(save_file)


# %%
# Create a Scatter plot to show correlation between movie runtime and revenue
x = sort_time["Runtime (Min)"]
y = sort_time["Revenue (Millions)"]

fig = plt.figure()
plt.scatter(x, y)
plt.xlabel("Movie Runtime (Mins)")
plt.ylabel("Movie Revenue (Millions)")
plt.title("Movie Runtime vs. Movie Revenue (2008-2018)")
plt.xticks(np.arange(0, 300, 60))
plt.yticks(np.arange(0, 3500, 500))
plt.show()

save_file = os.path.join("..", "Images", "Movie Runtime vs Rev Scatter.png")
fig.savefig(save_file)


# %%



