import os
import numpy as np
import pandas as pd
import datetime

if not os.getcwd().endswith("etl"):
    os.chdir("./data_science/lessons/etl")

# read in the projects data set and do some basic wrangling
projects = pd.read_csv('./data/projects_data.csv', dtype=str)
projects.drop('Unnamed: 56', axis=1, inplace=True)
projects['totalamt'] = pd.to_numeric(projects['totalamt'].str.replace(',', ''))
projects['countryname'] = projects['countryname'].str.split(';', expand=True)[0]
projects['boardapprovaldate'] = pd.to_datetime(projects['boardapprovaldate'])

# Filter the data frame for projects over 1 billion dollars
df_billion_projects = projects[projects['totalamt'] > 1000000000]

# Count the number of unique countries in the results
df_billion_projects['countryname'].nunique()

# Get all projects for the 'Socialist Federal Republic of Yugoslavia'
df_yugoslavia_projects = projects[projects['countryname'].str.contains('Yugoslavia')]

# Filter the projects data set for project boardapprovaldate prior to April 27th, 1992 AND with countryname
# either 'Bosnia and Herzegovina', 'Croatia', 'Kosovo', 'Macedonia', 'Serbia', or 'Slovenia'
projs_red = projects[['regionname', 'countryname', 'lendinginstr', 'totalamt', 'boardapprovaldate',
                      'location', 'GeoLocID', 'GeoLocName', 'Latitude', 'Longitude', 'Country', 'project_name']]

republics = projs_red[(projs_red['boardapprovaldate'] <= '1992-04-27 00:00:00+00:00') &
                      (projs_red['countryname'].isin(['Bosnia and Herzegovina', 'Republic of Croatia', 'Kosovo',
                                                      'Macedonia', 'Serbia', 'Republic of Slovenia']))]\
    .sort_values(by='boardapprovaldate')

# Filter the projects data for Yugoslavia projects between February 1st, 1980 and May 23rd, 1989
yugoslavia = projs_red[(projs_red['countryname'].str.contains('Yugoslavia')) &
                       (projs_red['boardapprovaldate'] >= '1980-02-01 00:00:00+00:00') &
                       (projs_red['boardapprovaldate'] <= '1989-05-23 00:00:00+00:00')]\
    .sort_values(by='boardapprovaldate')

# Find the unique dates in the republics variable
republic_unique_dates = republics['boardapprovaldate'].unique()

# Find the unique dates in the yugoslavia variable
yugoslavia_unique_dates = yugoslavia['boardapprovaldate'].unique()

# Make a list of the results appending one list to the other
dates = np.append(yugoslavia_unique_dates, republic_unique_dates)

# Print out the dates that appeared twice in the results
observed_dates = set()
duplicate_dates = []

for approval_date in dates:
    if approval_date not in observed_dates:
        observed_dates.add(approval_date)
    else:
        duplicate_dates.append(approval_date)

print(duplicate_dates)

# See the duplicate data
pd.concat([yugoslavia[yugoslavia['boardapprovaldate'] == datetime.date(1983, 7, 26)],
           republics[republics['boardapprovaldate'] == datetime.date(1983, 7, 26)]])
