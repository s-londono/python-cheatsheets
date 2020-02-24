import os
import pandas as pd
import numpy as np

if not os.getcwd().endswith("etl"):
    os.chdir("./data_science/lessons/etl")

# read in the projects data set and do basic wrangling
gdp = pd.read_csv('data/gdp_data.csv', skiprows=4)
gdp.drop(['Unnamed: 62', 'Country Code', 'Indicator Name', 'Indicator Code'], inplace=True, axis=1)
population = pd.read_csv('data/population_data.csv', skiprows=4)
population.drop(['Unnamed: 62', 'Country Code', 'Indicator Name', 'Indicator Code'], inplace=True, axis=1)

# Reshape the data sets so that they are in long format
gdp_melt = gdp.melt(id_vars=['Country Name'],
                    var_name='year',
                    value_name='gdp')

# Use back fill and forward fill to fill in missing gdp values
gdp_melt['gdp'] = gdp_melt.sort_values('year').groupby('Country Name')['gdp'].fillna(method='ffill').fillna(
    method='bfill')

population_melt = population.melt(id_vars=['Country Name'],
                                  var_name='year',
                                  value_name='population')

# Use back fill and forward fill to fill in missing population values
population_melt['population'] = population_melt.sort_values('year').groupby('Country Name')['population'].fillna(
    method='ffill').fillna(method='bfill')

# merge the population and gdp data together into one data frame
df_country = gdp_melt.merge(population_melt, on=('Country Name', 'year'))

# filter data for the year 2016
df_2016 = df_country[df_country['year'] == '2016']

# filter out values that are not countries
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

# remove non countries from the data
df_2016 = df_2016[~df_2016['Country Name'].isin(non_countries)]

df_2016.head(10)


# NORMALIZATION

def x_min_max(data):
    """
    The input is an array of data as an input
    The outputs are the minimum and maximum of that array
    """
    minimum = np.amin(data)
    maximum = np.amax(data)
    return minimum, maximum


(gdp_min, gdp_max) = x_min_max(df_2016['gdp'])
print(f"{gdp_min} {gdp_max}")


def normalize(x, x_min, x_max):
    """
    The input is a single value
    The output is the normalized value
    """
    return (x - x_min) / (x_max - x_min)


class Normalizer:
    """
    The normalizer class receives a dataframe as its only input for initialization
    """
    def __init__(self, dataframe):
        """
        Iterate through each column of the DataFrame calculating the min and max for each column. Appends the
        results to the params attribute list
        """
        self.params = []

        for _, col_series in dataframe.iteritems():
            # Consider using Series.to_numpy() or Series.array instead of values. Introduced in Pandas 0.24
            col_min_max = self.x_min_max(col_series.values)
            self.params.append(col_min_max)

    def x_min_max(self, data):
        """
        The input is an array of data as an input
        The outputs are the minimum and maximum of that array
        """
        minimum = np.amin(data)
        maximum = np.amax(data)
        return minimum, maximum

    def normalize_data(self, x):
        """
        Receives a data point as an input and then outputs the normalized version. For example, if an input data point
        of [gdp, population] were used. Then the output would be the normalized version of the [gdp, population]
        data point. WARN: assumes that the columns in the dataframe used to initialize an object are in the same
        order as this data point x
        """
        normalized = []

        for i, x_component in enumerate(x):
            x_min = self.params[i][0]
            x_max = self.params[i][1]
            normalized.append((x_component - x_min) / (x_max - x_min))

        return normalized


gdp_normalizer = Normalizer(df_2016[['gdp', 'population']])

