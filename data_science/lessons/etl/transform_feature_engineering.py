import os
import pandas as pd

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

# Remove non countries from the data
df_2016 = df_2016[~df_2016['Country Name'].isin(non_countries)]
df_2016.reset_index(inplace=True, drop=True)

# Create new feature gdppercapita, which is the gdp value divided by the population value for each country
df_2016['gdppercapita'] = df_2016['gdp'] / df_2016['population']

# CREATE NEW POLYNOMIAL FEATURES


def create_multiples(b, k):
    """
    The create_multiples function has two inputs. A floating point number and an integer.
    The output is a list of multiples of the input b starting from the square of b and ending at b^k
    """
    return [b ** i for i in range(2, k + 1)]


def column_name_generator(colname, k):
    """
    Builds a list of column names for polynomically created features.
    Has two inputs: a string representing a column name and an integer k. The 'k' variable is the same as the
    create_multiples function. The output should be a list of column names.
    """
    return [f"{colname}{i}" for i in range(2, k + 1)]


# If the input is (df_2016, 'gdp', 3), then the output will be the df_2016 dataframe with two new columns
# One new column will be 'gdp2' ie gdp^2, and then other column will be 'gdp3' ie gdp^3.
def concatenate_features(df, column, num_columns):
    """
    Uses the two previous functions to create new polynomial columns and then append these to the original data frame.
    Has inputs: a dataframe, a column name represented by a string, and an integer representing
    the maximum power to create when engineering features.
    """
    # Create the new features as columns
    new_features = df[column].apply(lambda r: create_multiples(r, num_columns))

    # Create a dataframe with a separate column for each of the new features. WARN: in Pandas < 0.24,
    # function to_list was called tolist()
    new_features_df = pd.DataFrame(new_features.to_list(), columns=column_name_generator(column, num_columns))

    # Concatenate the original date frame in df with the new_features_df dataframe
    return df.merge(new_features_df, left_index=True, right_index=True)


df_extended = concatenate_features(df_2016, 'gdp', 4)
