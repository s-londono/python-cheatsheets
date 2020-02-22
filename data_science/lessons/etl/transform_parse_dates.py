import os
import pandas as pd

if not os.getcwd().endswith("etl"):
    os.chdir("./data_science/lessons/etl")

# Parse a date literal
parsed_date = pd.to_datetime('January 1st, 2017')

print(f"A {type(parsed_date)}: {parsed_date.year} {parsed_date.month} {parsed_date.second}")

# Formats: follow the Python standard date formatting conventions:
# https://strftime.org/

# Default expected format: US date
parsed_date = pd.to_datetime('5/3/2017 5:30')
print(f"In US format: {parsed_date.month}")

parsed_date = pd.to_datetime('3/5/2017 5:30', format='%d/%m/%Y %H:%M')
print(f"In EU format: {parsed_date.month}")

# Read in the projects data set with all columns type string
df_projects = pd.read_csv('./data/projects_data.csv', dtype=str)
df_projects.drop(['Unnamed: 56'], axis=1, inplace=True)

# Columns that contain dates
df_projects_dates = df_projects.head(15)[['boardapprovaldate', 'board_approval_month', 'closingdate']]

# Use the pandas to_datetime method to convert these two columns (boardapprovaldate, closingdate) into date times
df_projects['boardapprovaldate'] = pd.to_datetime(df_projects['boardapprovaldate'])
df_projects['closingdate'] = pd.to_datetime(df_projects['closingdate'])

# Access the different parts of the datetime objects. Series.dt gives access to the datetime object as explained here:
# https://pandas.pydata.org/pandas-docs/stable/generated/pandas.Series.dt.html
# https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#basics-dt-accessors
df_projects['approvalyear'] = df_projects['boardapprovaldate'].dt.year
df_projects['approvalday'] = df_projects['boardapprovaldate'].dt.day
df_projects['approvalweekday'] = df_projects['boardapprovaldate'].dt.weekday
df_projects['closingyear'] = df_projects['closingdate'].dt.year
df_projects['closingday'] = df_projects['closingdate'].dt.day
df_projects['closingweekday'] = df_projects['closingdate'].dt.weekday

# Convert the totalamt column to numeric
df_projects['totalamt'] = pd.to_numeric(df_projects['totalamt'].str.replace(',', ''))

df_project_year_amounts = df_projects[['approvalyear', 'totalamt']]

# Total amounts per year
df_sums = df_project_year_amounts.groupby(by='approvalyear').sum()

df_sums.plot.bar()
df_sums.plot.line()
