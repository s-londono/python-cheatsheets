import os
import pandas as pd
from pycountry import countries
from collections import defaultdict

if not os.getcwd().endswith("etl"):
    os.chdir("./data_science/lessons/etl")

# Read in the population data and drop the final column
df_indicator = pd.read_csv('./data/population_data.csv', skiprows=4)
df_indicator.drop(['Unnamed: 62'], axis=1, inplace=True)

# Read in the projects data set with all columns type string
df_projects = pd.read_csv('./data/projects_data.csv', dtype=str)
df_projects.drop(['Unnamed: 56'], axis=1, inplace=True)

# Obtain unique country names
df_unique_country_names = df_indicator[['Country Name', 'Country Code']].drop_duplicates()

# Get all unique country values in the projects dataset
uq_project_country_names = df_projects['countryname'].unique()

# Series and Index are equipped with a set of string processing methods that make it easy to operate on each
# element of the array. Perhaps most importantly, these methods exclude missing/NA values automatically.
# These are accessed via the str attribute and generally have names matching the equivalent (scalar)
# built-in string methods:
# Fix column countryname
df_projects['Official Country Name'] = df_projects['countryname'].str.split(';').str.get(0)

# Try the PyCountry library
spain_1 = countries.get(name='Spain')
spain_2 = countries.lookup('Kingdom of Spain')

# Make a dictionary mapping the unique countries in 'Official Country Name' to the ISO code
project_country_abbrev_dict = defaultdict(str)
country_not_found = []  # Stores countries not found in the pycountry library

# Create a dictionary mapping the country name to the alpha_3 ISO code
for country in df_projects['Official Country Name'].drop_duplicates().sort_values():
    try:
        # TODO: look up the country name in the pycountry library
        # store the country name as the dictionary key and the ISO-3 code as the value
        project_country_abbrev_dict[country] = countries.lookup(country).alpha_3
    except Exception as err:
        # If the country name is not in the pycountry library, then print out the country name
        # And store the results in the country_not_found list
        print(country, ' not found ', err)
        country_not_found.append(country)

# Iterate through the country_not_found list and check if the country name is in the df_indicator data set
indicator_countries = df_indicator[['Country Name', 'Country Code']].drop_duplicates().sort_values(by='Country Name')

for country in country_not_found:
    if country in indicator_countries['Country Name'].tolist():
        print(country)

# Sometimes, quite a lot of manual work is still required. Define the country code for countries in country_not_found
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

# Update the project_country_abbrev_dict with the country_not_found_mapping dictionary
project_country_abbrev_dict.update(country_not_found_mapping)

# Use the project_country_abbrev_dict and the df_projects['Country Name'] column to make a new column of the alpha-3
# country codes. This new column should be called 'Country Code'
df_projects['Country Code'] = df_projects['Official Country Name'].apply(
    lambda country_name: project_country_abbrev_dict[country_name])


