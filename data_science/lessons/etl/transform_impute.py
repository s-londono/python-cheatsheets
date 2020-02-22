import os
import pandas as pd
import matplotlib.pyplot as plt

if not os.getcwd().endswith("etl"):
    os.chdir("./data_science/lessons/etl")

df = pd.read_csv('data/gdp_data.csv', skiprows=4)
df.drop('Unnamed: 62', axis=1, inplace=True)

count_null_vals = df.isnull().sum()

# put the data set into long form instead of wide
df_melt = pd.melt(df, id_vars=['Country Name', 'Country Code', 'Indicator Name', 'Indicator Code'], var_name='year',
                  value_name='GDP')

# convert year to a date time
df_melt['year'] = pd.to_datetime(df_melt['year'])


def plot_results(column_name):
    # plot the results for Afghanistan, Albania, and Honduras
    fig, ax = plt.subplots(figsize=(8, 6))

    df_melt[(df_melt['Country Name'] == 'Afghanistan') |
            (df_melt['Country Name'] == 'Albania') |
            (df_melt['Country Name'] == 'Honduras')].groupby('Country Name').plot('year', column_name,
                                                                                  legend=True, ax=ax)

    ax.legend(labels=['Afghanistan', 'Albania', 'Honduras'])


plot_results('GDP')

# Use the df_melt dataframe and fill in missing values with a country's mean GDP
df_mean_country_gdp = df_melt[['Country Name', 'GDP']].groupby(by='Country Name').mean()


def transform_country_gdp(r):
    return r.fillna(df_mean_country_gdp.loc[r.iloc[0], 'GDP'])


df_melt['GDP_filled'] = df_melt[['Country Name', 'GDP']].transform(transform_country_gdp, axis=1)['GDP']

plot_results('GDP_filled')

# The pandas fillna method has a forward fill option. E.g. df_melt['GDP'].fillna(method='ffill').
# However, there are two issues with that code.
# - Data should be first sorted by year
# - Data must be grouped by country name, so that the forward fill stays within each country
df_melt_sorted = df_melt.sort_values(by='year')
df_melt['GDP_ffill'] = df_melt_sorted[['Country Code', 'GDP']].groupby(by='Country Code').fillna(method='ffill')

# To completely fill the entire GDP data for all countries, you might have to run both forward fill and back fill.
# Note that the results will be slightly different depending on if you run forward fill first or back fill first.
# Fill null values that were not preceded by any values and thus were not filled by forward-fill
df_melt['GDP_bfill'] = df_melt_sorted[['Country Code', 'GDP']].groupby(by='Country Code').fillna(method='bfill')

# Or in a single line...
# Run forward fill and backward fill on the GDP data
df_melt['GDP_ff_bf'] = df_melt.sort_values('year').groupby('Country Name')['GDP']\
    .fillna(method='ffill').fillna(method='bfill')
