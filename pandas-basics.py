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

# DATAFRAMES
# Main tool of Pandas

# Ensures repeatability of results
np.random.seed(101)

# A DataFrame is a bunch of Series sharing indexes (each column is a Series, each row is also a series)
# Create a DataFrame specifying the row and column indexes
df_1 = pd.DataFrame(data=randn(5, 4), index=['A', 'B', 'C', 'D', 'E'], columns=['W', 'X', 'Y', 'Z'])

# Retrieve column by label (as a Series)
se_col_x = df_1['X']
print(f"Type: {type(se_col_x)}. As string: \n{se_col_x}")

# Add column to a DataFrame, as a sum of existing columns
df_1['SumXY'] = df_1['X'] + df_1['Y']

# Remove a row (axis by default is 0). Does not modify the DataFrame
df_1.drop('E')

# Remove a column. Does not modify the DataFrame
df_1.drop('Z', axis=1)

# To modify the DataFrame use inplace (applies to many methods in Pandas)
df_1.drop('Z', axis=1, inplace=True)

# Dimensions of a DataFrame
print(df_1.shape)

# Select a subset of columns
print(df_1[['Y', 'W']])

# Select rows by label: use loc[row, col] (location. Access a group of rows and columns by label(s) or a boolean array)
se_row_a = df_1.loc['A']
print(f"Type: {type(se_row_a)}. As string:\n{se_row_a}")
print(df_1.loc[['A', 'C']])

# With loc, the first argument specifies rows, second argument columns. Can use label slices, label arrays
print(df_1.loc['A', 'X'])
print(df_1.loc['B':'D', ['X', 'W']])
print(df_1.loc['B':'D', 'X':'Y'])
print(df_1.loc[['B', 'E'], 'X':'Y'])
print(df_1.loc[['B', 'E'], 'X':'Y'])
print(df_1.loc[['B', 'E'], 'X':'Y'])

# With loc, boolean arrays can be used to select rows
print(df_1.loc[df_1['X'] > 0])
print(df_1.loc[df_1['X'] > 0, 'Y':])

# Select rows by index: use iloc (index location)
print(df_1.iloc[3])

# With iloc, the first and second arguments specify row and column indexes respectively
print(df_1.iloc[2, 3])
print(df_1.iloc[1:3, 2:4])
print(df_1.iloc[[0, -1], -1])

# Conditional selection. Comparison operators return boolean DataFrames (or Series), that can be used as selectors
df_bool_1 = df_1 > 0
print(df_1[df_bool_1])
print(df_1['X'] < 1)

# Using a condition on a Series returns only the matching rows (no NaN values). Result is a DataFrame
# To select rows where a column matches a condition:
print(df_1[df_1['X'] < 0])
print(df_1[df_1['X'] < 0]['Y'])

# To select columns where a row matches a condition:
print(df_1.loc[:, df_1.loc['B'] < 1])

# Multiple conditions (use & instead of and, | instead of or)
print(df_1[(df_1['X'] > 0) & (df_1['Y'] > 0)])

# Reset index (convert to numerical). Does not occur in place by default. Use inplace argument to do so
df_1.reset_index()

# Switch index to a specific column
new_index = 'CA NY WY OR CO'.split()
df_1['State'] = new_index
print(df_1.set_index('State'))

# MULTIPLE INDEXES

outside = ['G1', 'G1', 'G1', 'G2', 'G2', 'G2']
inside = [1, 2, 3, 1, 2, 3]
hier_index = list(zip(outside, inside))
hier_index = pd.MultiIndex.from_tuples(hier_index)

# Build a multi-index (multi-level index, index hierarchy) DataFrame
multi_ix_df = pd.DataFrame(randn(6, 2), hier_index, ['A', 'B'])

multi_ix_df.loc['G1']
multi_ix_df.loc['G1'].iloc[1]

# Indexes have no names by default. Can assign names
print(multi_ix_df.index.names)
multi_ix_df.index.names = ['Groups', 'Num']

multi_ix_df.loc['G2'].loc[2]['B']

# Cross section. Allows to select parts of the DataFrame and skip other parts. Example: get bot rows with subindex 1
multi_ix_df.xs(1, level='Num')


