import os
import pandas as pd
import sqlite3
from pycountry import countries
from collections import defaultdict

if not os.getcwd().endswith("etl"):
    os.chdir("./data_science/lessons/etl")

# EXTRACT - TRANSFORM

# Read in the projects data set and do basic wrangling
gdp = pd.read_csv('data/gdp_data.csv', skiprows=4)
gdp.drop(['Unnamed: 62', 'Indicator Name', 'Indicator Code'], inplace=True, axis=1)
population = pd.read_csv('data/population_data.csv', skiprows=4)
population.drop(['Unnamed: 62', 'Indicator Name', 'Indicator Code'], inplace=True, axis=1)

# Reshape the data sets so that they are in long format
gdp_melt = gdp.melt(id_vars=['Country Name', 'Country Code'],
                    var_name='year',
                    value_name='gdp')

# Use back fill and forward fill to fill in missing gdp values
gdp_melt['gdp'] = gdp_melt.sort_values('year').groupby(['Country Name', 'Country Code'])['gdp'].fillna(
    method='ffill').fillna(method='bfill')

population_melt = population.melt(id_vars=['Country Name', 'Country Code'],
                                  var_name='year',
                                  value_name='population')

# Use back fill and forward fill to fill in missing population values
population_melt['population'] = population_melt.sort_values('year').groupby('Country Name')['population'].fillna(
    method='ffill').fillna(method='bfill')

# Merge the population and gdp data together into one data frame
df_indicator = gdp_melt.merge(population_melt, on=('Country Name', 'Country Code', 'year'))

# Filter out values that are not countries
non_countries = ['World',
                 'High income',
                 'OECD members',
                 'Post-demographic dividend',
                 'IDA & IBRD total',
                 'Low & middle income',
                 'Middle income',
                 'IBRD only',
                 'East Asia & Pacific',
                 'Europe & Central Asia',
                 'North America',
                 'Upper middle income',
                 'Late-demographic dividend',
                 'European Union',
                 'East Asia & Pacific (excluding high income)',
                 'East Asia & Pacific (IDA & IBRD countries)',
                 'Euro area',
                 'Early-demographic dividend',
                 'Lower middle income',
                 'Latin America & Caribbean',
                 'Latin America & the Caribbean (IDA & IBRD countries)',
                 'Latin America & Caribbean (excluding high income)',
                 'Europe & Central Asia (IDA & IBRD countries)',
                 'Middle East & North Africa',
                 'Europe & Central Asia (excluding high income)',
                 'South Asia (IDA & IBRD)',
                 'South Asia',
                 'Arab World',
                 'IDA total',
                 'Sub-Saharan Africa',
                 'Sub-Saharan Africa (IDA & IBRD countries)',
                 'Sub-Saharan Africa (excluding high income)',
                 'Middle East & North Africa (excluding high income)',
                 'Middle East & North Africa (IDA & IBRD countries)',
                 'Central Europe and the Baltics',
                 'Pre-demographic dividend',
                 'IDA only',
                 'Least developed countries: UN classification',
                 'IDA blend',
                 'Fragile and conflict affected situations',
                 'Heavily indebted poor countries (HIPC)',
                 'Low income',
                 'Small states',
                 'Other small states',
                 'Not classified',
                 'Caribbean small states',
                 'Pacific island small states']

# Remove non countries from the data
df_indicator = df_indicator[~df_indicator['Country Name'].isin(non_countries)]
df_indicator.reset_index(inplace=True, drop=True)

df_indicator.columns = ['countryname', 'countrycode', 'year', 'gdp', 'population']

# Output the first few rows of the data frame
df_indicator.head()

# Read in the countries data set. This will create a data frame called df_projects containing the World Bank
# projects data. The data frame only has the 'id', 'countryname', 'countrycode', 'totalamt', and 'year' columns

# Read in the projects data set with all columns type string
df_projects = pd.read_csv('data/projects_data.csv', dtype=str)
df_projects.drop(['Unnamed: 56'], axis=1, inplace=True)

df_projects['countryname'] = df_projects['countryname'].str.split(';').str.get(0)

country_not_found = []  # stores countries not found in the pycountry library
project_country_abbrev_dict = defaultdict(str)  # set up an empty dictionary of string values

# iterate through the country names in df_projects.
# Create a dictionary mapping the country name to the alpha_3 ISO code
for country in df_projects['countryname'].drop_duplicates().sort_values():
    try:
        # look up the country name in the pycountry library
        # store the country name as the dictionary key and the ISO-3 code as the value
        project_country_abbrev_dict[country] = countries.lookup(country).alpha_3
    except:
        # If the country name is not in the pycountry library, then print out the country name
        # And store the results in the country_not_found list
        country_not_found.append(country)

# run this code cell to load the dictionary

country_not_found_mapping = {'Co-operative Republic of Guyana': 'GUY',
                             'Commonwealth of Australia': 'AUS',
                             'Democratic Republic of Sao Tome and Prin': 'STP',
                             'Democratic Republic of the Congo': 'COD',
                             'Democratic Socialist Republic of Sri Lan': 'LKA',
                             'East Asia and Pacific': 'EAS',
                             'Europe and Central Asia': 'ECS',
                             'Islamic  Republic of Afghanistan': 'AFG',
                             'Latin America': 'LCN',
                             'Caribbean': 'LCN',
                             'Macedonia': 'MKD',
                             'Middle East and North Africa': 'MEA',
                             'Oriental Republic of Uruguay': 'URY',
                             'Republic of Congo': 'COG',
                             "Republic of Cote d'Ivoire": 'CIV',
                             'Republic of Korea': 'KOR',
                             'Republic of Niger': 'NER',
                             'Republic of Kosovo': 'XKX',
                             'Republic of Rwanda': 'RWA',
                             'Republic of The Gambia': 'GMB',
                             'Republic of Togo': 'TGO',
                             'Republic of the Union of Myanmar': 'MMR',
                             'Republica Bolivariana de Venezuela': 'VEN',
                             'Sint Maarten': 'SXM',
                             "Socialist People's Libyan Arab Jamahiriy": 'LBY',
                             'Socialist Republic of Vietnam': 'VNM',
                             'Somali Democratic Republic': 'SOM',
                             'South Asia': 'SAS',
                             'St. Kitts and Nevis': 'KNA',
                             'St. Lucia': 'LCA',
                             'St. Vincent and the Grenadines': 'VCT',
                             'State of Eritrea': 'ERI',
                             'The Independent State of Papua New Guine': 'PNG',
                             'West Bank and Gaza': 'PSE',
                             'World': 'WLD'}

project_country_abbrev_dict.update(country_not_found_mapping)

df_projects['countrycode'] = df_projects['countryname'].apply(lambda x: project_country_abbrev_dict[x])

df_projects['boardapprovaldate'] = pd.to_datetime(df_projects['boardapprovaldate'])

df_projects['year'] = df_projects['boardapprovaldate'].dt.year.astype(str).str.slice(stop=4)

df_projects['totalamt'] = pd.to_numeric(df_projects['totalamt'].str.replace(',', ""))

df_projects = df_projects[['id', 'countryname', 'countrycode', 'totalamt', 'year']]

df_projects.head()


# LOAD
# At this point there are two extracted-transformed DataFrames. They have both country codes:
# - df_projects, which contain data from the projects data set
# - df_indicator, which contain population and gdp data for various years

# Merge the two data sets together using country code and year as common keys. When joining the data sets,
# keep all of the data in the df_projects DataFrame even if there is no indicator data for that country code.
df_merged = df_projects.merge(df_indicator[df_indicator.columns.drop('year')], how='left', on='countrycode')

print(df_merged[(df_merged['year'] == '2017') & (df_merged['countryname_y'] == 'Jordan')])

# Export to JSON
df_merged.to_json('/tmp/df_merged.json', orient='records')

# Export to CSV
df_merged.to_csv('/tmp/df_merged.csv', index=False)

# Connect to the database. Note that sqlite3 will create this database file if it does not exist already
conn = sqlite3.connect('/tmp/worldbank.db')

# Export to SQLite3
df_merged.to_sql('merged', con=conn, if_exists='replace')
df_indicator.to_sql('indicator', con=conn, if_exists='replace')
df_projects.to_sql('projects', con=conn, if_exists='replace')

# Query the database
print(pd.read_sql('SELECT * FROM merged WHERE year = "2017" AND countrycode = "BRA"', con=conn).head())

print(pd.read_sql('SELECT * FROM projects LEFT JOIN indicator ON \
 projects.countrycode = indicator.countrycode AND \
 projects.year = indicator.year WHERE \
 projects.year = "2017" AND projects.countrycode = "BRA"', con=conn).head())

# commit any changes to the database and close the connection to the database
conn.commit()
conn.close()

# SQLite, as its name would suggest, is somewhat limited in its functionality. For example, the Alter Table command
# only allows you to change a table name or to add a new column to a table. You can't, for example, add a primary key
# to a table once the table is already created. If you want more control over a sqlite3 database, it's better to use
# the sqlite3 library directly. Here is an example of how to use the sqlite3 library to create a table in the database,
# insert a value, and then run a SQL query on the database:

# Connect to the data base. WARN: with blocks do not close the connection automatically!
conn = sqlite3.connect('/tmp/worldbank.db')

# Get a cursor
cur = conn.cursor()

# Drop the test table in case it already exists
cur.execute("DROP TABLE IF EXISTS test")

# Create the test table including project_id as a primary key
cur.execute(f"CREATE TABLE test (project_id TEXT PRIMARY KEY, countryname TEXT, "
            f"countrycode TEXT, totalamt REAL, year INTEGER);")

# Insert a value into the test table
cur.execute(f"INSERT INTO test (project_id, countryname, countrycode, totalamt, year) "
            f"VALUES ('a', 'Brazil', 'BRA', '100,000', 1970);")

# Commit changes made to the database
conn.commit()

# Select all from the test table
cur.execute("SELECT * FROM test")
print(cur.fetchall())

# Close connection.
conn.close()


try:
    # Connect to the data base. WARN: with blocks do not close the connection automatically!
    conn = sqlite3.connect('/tmp/worldbank.db')
    cur = conn.cursor()

    # drop tables created previously to start fresh
    cur.execute("DROP TABLE IF EXISTS test")
    cur.execute("DROP TABLE IF EXISTS indicator")
    cur.execute("DROP TABLE IF EXISTS projects")
    cur.execute("DROP TABLE IF EXISTS gdp")
    cur.execute("DROP TABLE IF EXISTS population")

    cur.execute(f"CREATE TABLE projects (project_id TEXT PRIMARY KEY, countryname TEXT, countrycode TEXT, "
                f"totalamt REAL, year INTEGER);")

    cur.execute(f"CREATE TABLE gdp (countryname TEXT, countrycode TEXT, year INTEGER, gdp REAL, "
                f"PRIMARY KEY (countrycode, year));")

    cur.execute(f"CREATE TABLE population (countryname TEXT, countrycode TEXT, year INTEGER, population INTEGER, "
                f"PRIMARY KEY (countrycode, year));")

    for ix, row in df_projects.iterrows():
        cur.execute("INSERT INTO projects (project_id, countryname, countrycode, totalamt, year) VALUES (" +
                    "'{}', '{}', '{}', {}, {});".format(row['id'],
                                                        row['countryname'].replace("'", "''"),
                                                        row['countrycode'],
                                                        row['totalamt'] if row['totalamt'] != "nan" else 0,
                                                        row['year'] if row['year'] != "nan" else 0))

    for dx, row in df_indicator.iterrows():
        cur.execute("INSERT INTO gdp (countryname, countrycode, year, gdp) VALUES (" +
                    "'{}', '{}', {}, {});".format(row['countryname'].replace("'", "''"),
                                                  row['countrycode'],
                                                  row['year'] if row['year'] != "nan" else 0,
                                                  row['gdp'] if row['gdp'] != "nan" else 0))

        cur.execute("INSERT INTO population (countryname, countrycode, year, population) VALUES (" +
                    "'{}', '{}', {}, {});".format(row['countryname'].replace("'", "''"),
                                                  row['countrycode'],
                                                  row['year'] if row['year'] != "nan" else 0,
                                                  row['population'] if row['population'] != "nan" else 0))

    conn.commit()

    # run this command to see if your tables were loaded as expected
    sqlquery = (f"SELECT * FROM projects JOIN gdp JOIN population ON projects.year = gdp.year AND "
                f"projects.countrycode = gdp.countrycode AND projects.countrycode = population.countrycode AND "
                f"projects.year=population.year;")

    result = pd.read_sql(sqlquery, con=conn)
    print(result.shape)

except Exception as err:
    print(f"Error! {err}")
    conn.rollback()

finally:
    conn.close()
