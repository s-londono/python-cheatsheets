import os
import re
import pandas as pd
import numpy as np

if not os.getcwd().endswith("etl"):
    os.chdir("./data_science/lessons/etl")

# Read in the projects data set and do basic wrangling
projects = pd.read_csv('data/projects_data.csv', dtype=str)
projects.drop('Unnamed: 56', axis=1, inplace=True)

projects['totalamt'] = pd.to_numeric(projects['totalamt'].str.replace(',', ''))
projects['countryname'] = projects['countryname'].str.split(';', expand=True)[0]
projects['boardapprovaldate'] = pd.to_datetime(projects['boardapprovaldate'])

# Keep the project name, lending, sector and theme data
sector = projects.copy()
sector = sector[['project_name', 'lendinginstr', 'sector1', 'sector2', 'sector3', 'sector4', 'sector5', 'sector',
                 'mjsector1', 'mjsector2', 'mjsector3', 'mjsector4', 'mjsector5',
                 'mjsector', 'theme1', 'theme2', 'theme3', 'theme4', 'theme5', 'theme ',
                 'goal', 'financier', 'mjtheme1name', 'mjtheme2name', 'mjtheme3name',
                 'mjtheme4name', 'mjtheme5name']]

# Output percentage of values that are missing
print(100 * sector.isnull().sum() / sector.shape[0])

# Create a list of the unique values in sector1. Use the sort_values() and unique() pandas methods.
# Then convert those results into a Python list
uniquesectors1 = sector['sector1'].sort_values().unique().tolist()
print('Number of unique values in sector1: ', len(uniquesectors1))

# There are some issues with this 'sector1' variable:
# - There are values labeled '!$!0'. These should be substituted with NaN.
# - Each sector1 value ends with a ten or eleven character string like '! !49! !EP'.
# - Some sectors show up twice in the list, but differ just in the suffix (e.g. !70! !YZ').
# - Many values in the sector1 variable start with the term '(Historic)'.
# Remove everything past the exclamation point and remove the phrase (Historic).

# Replace the string '!$10' with nan
sector['sector1'] = sector['sector1'].replace("!$!0", np.nan)

# In the sector1 variable, remove the last 10 or 11 characters from the sector1 variable.
sector['sector1'].replace(to_replace=r"!.+$", value="", regex=True, inplace=True)

# Remove the string '(Historic)' from the sector1 variable
sector['sector1'] = sector['sector1'].str.replace(r"\(Historic\)\s*", "")

print('Number of unique sectors after cleaning:', len(list(sector['sector1'].unique())))
print('Percentage of null values after cleaning:', 100 * sector['sector1'].isnull().sum() / sector['sector1'].shape[0])

# If you make dummy variables including NaN values, then you could consider a feature with all zeros to represent NaN.
# Or you could delete these records from the data set. Pandas will ignore NaN values by default.
# That means, for a given row, all dummy variables will have a value of 0 if the sector1 value was NaN.

# Create dummy variables from the sector1 data. Put the results into a dataframe called dummies.
# Remember, argument drop_first is particularly important. Also consider using dummy_na and dtype
dummies = pd.get_dummies(sector['sector1'], prefix="sector1", prefix_sep="_", drop_first=True)

# Create a new dataframe called df by filtering the projects data for the totalamt and the year from boardapprovaldate
projects['year'] = projects['boardapprovaldate'].dt.year
df = projects[['year', 'totalamt']]

# Concatenate the results of dummies and projects into a single data frame
df_final = pd.concat([df, dummies], axis=1)
df_final.head()

# AGGREGATING SIMILAR CATEGORIES

# Create a new variable called sector1_aggregates. Then find all the rows in sector1_aggregates with the term 'Energy'
# in them. For all of these rows, replace whatever is the value is with the term 'Energy'. The idea is to simplify
# the category names by combining various categories together. Do the same for the term 'Transportation
sector.loc[:, 'sector1_aggregates'] = sector['sector1']

sel_energy_sectors = sector['sector1_aggregates'].str.contains(re.compile("energy", flags=re.IGNORECASE), regex=True)
sel_energy_sectors.fillna(False, inplace=True)

# Use loc to avoid warning: "A value is trying to be set on a copy of a slice from a DataFrame"
# https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html
sector.loc[sel_energy_sectors, 'sector1_aggregates'] = 'Energy'

print('Number of unique sectors after cleaning:', len(list(sector['sector1_aggregates'].unique())))
