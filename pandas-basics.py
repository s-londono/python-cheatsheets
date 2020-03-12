import numpy as np
from numpy.random import randn
import pandas as pd

# SERIES
# Are like numpy arrays that can be indexed by label

labels_1 = ['a', 'b', 'c']
np_data_1 = np.array([10, 20, 30])

# Create a Series with elements indexed by sequential numbers (default indexes)
se_num_ix = pd.Series(data=np_data_1)
print(se_num_ix)

# Create a Series with elements indexed by labels
se_lbl_ix = pd.Series(data=np_data_1, index=labels_1)
print(se_lbl_ix)

# Can also create a Series providing a Python array as data
se_lbl_ix_2 = pd.Series([5, 7, 9], labels_1)
print(se_lbl_ix_2)

# Creating a Series from a dictionary takes keys as labels and values as data
se_lbl_ix_3 = pd.Series({'a': 1, 'b': 2, 'c': 3})
print(se_lbl_ix_3)

# Series can hold virtually any kind of object! even functions
se_lbl_ix_4 = pd.Series(data=[sum, print, len])
print(se_lbl_ix_4)

# Data can be extracted from Series using the indexes
print(se_lbl_ix['b'])

# Series operations are performed on the data, element by element, matching them by index
se_lbl_ix_5 = pd.Series(data=[10, 10, 10, 10], index=['a', 'x', 'c', 'd'])
print(se_lbl_ix + se_lbl_ix_5)

# Sort a series by indices/values
print(se_lbl_ix.sort_index())
print(se_lbl_ix.sort_values(ascending=False))

# DATAFRAMES
# Main tool of Pandas

# Ensures repeatability of results
np.random.seed(101)

# A DataFrame is a bunch of Series sharing indexes (each column is a Series, each row is also a series)
# Create a DataFrame specifying the row and column indexes
df_1 = pd.DataFrame(data=randn(5, 4), index=['A', 'B', 'C', 'D', 'E'], columns=['W', 'X', 'Y', 'Z'])

# Can create a DataFrame from a dictionary. Each key is interpreted as a column
d_2 = {'A': [1, 2, 3], 'B': [5, 6, 7], 'C': [8, 9, 10], 'D': [11, 12, 13], 'E': [14, 15, 16]}
df_2 = pd.DataFrame(d_2)

# General information about a DataFrame
df_1.info()

# Size of a DataFrame (tuple of rows and columns)
print(df_1.shape)

# Retrieve column by label (as a Series)
# se_col_x = df_1.X
se_col_x = df_1['X']
print(f"Type: {type(se_col_x)}. As string: \n{se_col_x}")

# Add column to a DataFrame, as a sum of existing columns
df_1['SumXY'] = df_1['X'] + df_1['Y']

# Use loc to avoid warning: "A value is trying to be set on a copy of a slice from a DataFrame"
# https://pandas.pydata.org/pandas-docs/stable/user_guide/indexing.html
sector.loc[sel_energy_sectors, 'sector1_aggregates'] = 'Energy'

# Remove a row (axis by default is 0). Does not modify the DataFrame
df_1.drop('E')

# Remove a column. Does not modify the DataFrame
df_1.drop('Z', axis=1)

# To modify the DataFrame use inplace (applies to many methods in Pandas)
df_1.drop('Z', axis=1, inplace=True)

# Dimensions of a DataFrame
print(df_1.shape)

# Print columns and indices
print(df_1.columns)
print(df_1.index)

# Reset index (convert to numerical). Does not occur in place by default. Use inplace argument to do so
df_1.reset_index()

# Switch index to a specific column
new_index = 'CA NY WY OR CO'.split()
df_1['State'] = new_index
print(df_1.set_index('State'))


# THE APPLY METHOD

# Given a function (or Lambda expression)...
def times2(x):
    return x * 2


# It can be applied to all elements of a DataFrame
print(df_1.apply(times2))

# Also works with Series
print(df_1['X'].apply(lambda x: x ** 2))

# RENAME LABELS

labels = list(df_1.columns)

for label in labels:
    label = label.replace(' ', '_')

df_1.columns = labels

# ACCESSORS
# Pandas provides dtype-specific methods under various accessors.
# These are separate namespaces within Series that only apply to specific data types.
# https://pandas.pydata.org/pandas-docs/stable/reference/series.html#accessors

# String methods
df_strs = pd.DataFrame({"A": ["a1 (suffix)", "a2 (suffix)", "a3 (suffix)"], "B": ["b1", "b2", "b3"]})

df_strs["A"] = df_strs["A"].str.replace(r" \([a-zA-Z]+\)", "")
df_strs["A"] = df_strs["A"].str.upper()
df_strs["A"] = df_strs["A"].str[-1:]

# DateTime methods
df_dates = pd.DataFrame({"C": ["1990-12-30 00:00:00-05:00", "1992-05-14 19:20:00-05:00"], "D": [32, 45]})
# Convert string (object) column to datetime
df_dates["C"] = pd.to_datetime(df_dates["C"])

df_dates["Y"] = df_dates.C.dt.year
