import os
import pandas as pd

os.chdir("data_science/lessons/etl")

# When a column contains mixed data types, read_csv throws a pandas.errors.DtypeWarning. Use the dtype argument
# to specify the data types of each column (dict) or all columns (str with type name). For instance, to read all as str
df_projects = pd.read_csv("./data/projects_data.csv", dtype='str')

print(df_projects.shape)

# Count the number of null values in the data set
df_missing_vals = df_projects.isnull().sum()

# Skip the first 4 rows of a dataset that contains garbage on those lines
df_population = pd.read_csv("./data/population_data.csv", skiprows=4)

# Count nulls per column and per row
count_nulls_columns = df_population.isnull().sum()
count_nulls_rows = df_population.isnull().sum(axis=1)

# Drop the last column, which contains only nulls
df_population.drop(columns='Unnamed: 62', inplace=True)

# What rows still contain null data?
df_population_with_nulls = df_population[df_population.isnull().any(axis=1)]

