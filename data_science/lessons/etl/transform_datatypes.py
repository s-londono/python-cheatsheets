import os
import pandas as pd

if not os.getcwd().endswith("etl"):
    os.chdir("./data_science/lessons/etl")

# When using pd.read_csv(), you could specify the column type for every column in the data set. The pd.read_csv()
# dtype option can accept a dictionary mapping each column name to its data type. You could also specify the
# thousands option with thousands=','. This specifies that thousands are separated by a comma in the data set

# Read in the population data and drop the final column. Let Pandas guess the datatypes
df_indicator = pd.read_csv('./data/population_data.csv', skiprows=4)
df_indicator.drop(['Unnamed: 62'], axis=1, inplace=True)

# Read in the projects data set with all columns type string
df_projects = pd.read_csv('./data/projects_data.csv', dtype=str)
df_projects.drop(['Unnamed: 56'], axis=1, inplace=True)

# Get the data types
print(df_indicator.dtypes)

# Calculate the population sum by year for Canada, the United States, and Mexico.

# the keepcol variable makes a list of the column names to keep. You can use this if you'd like
keepcol = ['Country Name']
for i in range(1960, 2018, 1):
    keepcol.append(str(i))

# Store a data frame that only contains the rows for Canada, United States, and Mexico.
df_nafta = df_indicator[df_indicator['Country Code'].isin(['CAN', 'USA', 'MEX'])]

df_sums = df_nafta[keepcol].sum()

# It might be faster to read in the entire data set with string types and then convert individual columns as needed.
# Convert the totalamt column from a string to an integer type
df_projects['totalamt'] = df_projects['totalamt'].str.replace(',', '')
df_projects['totalamt'] = pd.to_numeric(df_projects['totalamt'])

print(df_projects.dtypes)

# Pandas has a few different methods for converting between data types:
# astype
# to_datetime
# to_numeric
# to_timedelta

# The dtypes of a dataframe, generally are:
# float64
# int64
# bool
# datetime64
# timedelta
# object


