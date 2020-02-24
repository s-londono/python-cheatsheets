import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

if not os.getcwd().endswith("etl"):
    os.chdir("./data_science/lessons/etl")

# Read in the projects data set and do basic wrangling
gdp = pd.read_csv('data/gdp_data.csv', skiprows=4)
gdp.drop(['Unnamed: 62', 'Country Code', 'Indicator Name', 'Indicator Code'], inplace=True, axis=1)
population = pd.read_csv('data/population_data.csv', skiprows=4)
population.drop(['Unnamed: 62', 'Country Code', 'Indicator Name', 'Indicator Code'], inplace=True, axis=1)

# Reshape the data sets so that they are in long format
gdp_melt = gdp.melt(id_vars=['Country Name'], var_name='year', value_name='gdp')

population_melt = population.melt(id_vars=['Country Name'],
                                  var_name='year',
                                  value_name='population')

# Use back fill and forward fill to fill in missing values
gdp_melt['gdp'] = gdp_melt.sort_values('year').groupby('Country Name')['gdp']\
    .fillna(method='ffill').fillna(method='bfill')

population_melt['population'] = population_melt.sort_values('year').groupby('Country Name')['population']\
    .fillna(method='ffill').fillna(method='bfill')

# Merge the population and gdp data together into one data frame
df_country = gdp_melt.merge(population_melt, on=('Country Name', 'year'))

# Filter data for the year 2016
df_2016 = df_country[df_country['year'] == '2016']

# See what the data looks like
print(df_2016.head(10))

# Make a boxplot of the population data for the year 2016
df_2016.boxplot('population')

# Make a boxplot of the gdp data for the year 2016
df_2016.boxplot('gdp')

# Print info about the mean, std, quartiles, min, max, count
df_2016.describe()

# IDENTIFY OUTLIERS USING THE TUKEY RULE

# The Tukey rule finds outliers in one-dimension. The steps are:

# Find the first quartile (ie .25 quantile)
Q1 = df_2016.quantile(0.25)

# Find the third quartile (ie .75 quantile)
Q3 = df_2016.quantile(0.75)

# Calculate the inter-quartile range (Q3 - Q1)
IQR = Q3.sub(Q1)

# Any value that is greater than Q3 + 1.5 * IQR is an outlier. Same for those less than Qe - 1.5 * IQR
# Same as: max_value = Q3.add(IQR.mul(1.5))
max_value = Q3 + (IQR * 1.5)
min_value = Q1 - (IQR * 1.5)

population_outliers = df_2016[(df_2016['population'] >= max_value['population']) |
                              (df_2016['population'] <= min_value['population'])]

gdp_outliers = df_2016[(df_2016['gdp'] >= max_value['gdp']) |
                       (df_2016['gdp'] <= min_value['gdp'])]

# Names of regions that are not countries. Remove those
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

df_2016 = df_2016[df_2016['Country Name'].isin(non_countries) == False]

# Re-run Tukey after removin non-countries
Q1 = df_2016.quantile(0.25)
Q3 = df_2016.quantile(0.75)
IQR = Q3.sub(Q1)
max_value = Q3 + (IQR * 1.5)
min_value = Q1 - (IQR * 1.5)

population_outliers = df_2016[(df_2016['population'] >= max_value['population']) |
                              (df_2016['population'] <= min_value['population'])]

gdp_outliers = df_2016[(df_2016['gdp'] >= max_value['gdp']) |
                       (df_2016['gdp'] <= min_value['gdp'])]

# Find country names that are in both the population_outliers and the gdp_outliers. These have both relatively high
# populations and high GDPs. That might be an indication that although these countries have high values for both
# gdp and population, they're not true outliers when looking at these values from a two-dimensional perspective.
in_both_outliers = list(set(population_outliers['Country Name']).intersection(set(gdp_outliers['Country Name'])))

# Find country names that are in the population outliers list but not the gdp outliers list
population_outliers_only = list(set(population_outliers['Country Name']).difference(set(gdp_outliers['Country Name'])))

# Find country names that are in the gdp outliers list but not the gdp outliers list
gdp_outliers_only = list(set(gdp_outliers['Country Name']).difference(set(population_outliers['Country Name'])))

# 2-DIMENSIONAL ANALYSIS OF OUTLIERS

# Plots the GDP vs Population data including the country name of each point
x = list(df_2016['population'])
y = list(df_2016['gdp'])
text = df_2016['Country Name']

fig, ax = plt.subplots(figsize=(15,10))
ax.scatter(x, y)
plt.title('GDP vs Population')
plt.xlabel('population')
plt.ylabel('GDP')
for i, txt in enumerate(text):
    ax.annotate(txt, (x[i], y[i]))

# The United States, China, and India have such larger values that it's hard to see this data.
# Let's take those countries out for a moment and look at the data again
df_no_large = (df_2016['Country Name'] != 'United States') & \
              (df_2016['Country Name'] != 'India') & (df_2016['Country Name'] != 'China')
x = list(df_2016[df_no_large]['population'])
y = list(df_2016[df_no_large]['gdp'])
text = df_2016[df_no_large]['Country Name']

fig, ax = plt.subplots(figsize=(15, 10))
ax.scatter(x, y)
plt.title('GDP vs Population')
plt.xlabel('population')
plt.ylabel('GDP')
for i, txt in enumerate(text):
    ax.annotate(txt, (x[i], y[i]))

# Build a simple linear regression model with the population and gdp data for 2016. Fit a linear regression model
# on the population and gdp data
model = LinearRegression()
model.fit(df_2016['population'].values.reshape(-1, 1), df_2016['gdp'].values.reshape(-1, 1))

# plot the data along with predictions from the linear regression model
inputs = np.linspace(1, 2000000000, num=50)
predictions = model.predict(inputs.reshape(-1, 1))

df_2016.plot('population', 'gdp', kind='scatter')
plt.plot(inputs, predictions)

print(model.predict(1000000000))
 
# Remove the United States to see what happens with the linear regression model
df_2016[df_2016['Country Name'] != 'United States'].plot('population', 'gdp', kind='scatter')
# plt.plot(inputs, predictions)
model.fit(df_2016[df_2016['Country Name'] != 'United States']['population'].values.reshape(-1, 1),
          df_2016[df_2016['Country Name'] != 'United States']['gdp'].values.reshape(-1, 1))
inputs = np.linspace(1, 2000000000, num=50)
predictions = model.predict(inputs.reshape(-1,1))
plt.plot(inputs, predictions)

print(model.predict(1000000000))


def tukey_rule(data_frame, column_name):
    """
    Function that uses the Tukey rule to detect outliers in a dataframe column
    and then removes that entire row from the data frame. For example, if the United States
    is detected to be a GDP outlier, then remove the entire row of United States data.
    The function inputs should be a data frame and a column name.
    The output is a data_frame with the outliers eliminated
    :param data_frame: Dataframe to clear of outliers
    :param column_name: Name of the column to measure outliers on
    :return: DataFrame with outliers removed
    """
    column_data = data_frame[column_name]

    q1 = column_data.quantile(0.25)
    q3 = column_data.quantile(0.75)
    iqr = q3 - q1
    max_val = q3 + (1.5 * iqr)
    min_val = q1 - (1.5 * iqr)

    return data_frame[(data_frame[column_name] < max_val) & (data_frame[column_name] > min_val)].copy()


# Use the tukey_rule() function to make a new data frame with gdp and population outliers removed
df_outlier_removed = tukey_rule(df_2016, 'gdp')
df_outlier_removed = tukey_rule(df_outlier_removed, 'population')

# plot the data
x = list(df_outlier_removed['population'])
y = list(df_outlier_removed['gdp'])
text = df_outlier_removed['Country Name']

fig, ax = plt.subplots(figsize=(15, 10))
ax.scatter(x, y)
plt.title('GDP vs Population')
plt.xlabel('GDP')
plt.ylabel('Population')
for i, txt in enumerate(text):
    ax.annotate(txt, (x[i], y[i]))
