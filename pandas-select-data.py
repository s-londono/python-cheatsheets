import numpy as np
from numpy.random import randn
import pandas as pd

df_1 = pd.DataFrame(data=randn(5, 4), index=['A', 'B', 'C', 'D', 'E'], columns=['W', 'X', 'Y', 'Z'])

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
print(df_1.loc[:, 'X':'Y'])

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

# Using a condition on a Series returns only the matching rows (no NaN values). Result is a DataFrame
# To select rows where a column matches a condition:
print(df_1[df_1['X'] < 0])
print(df_1[df_1['X'] < 0]['Y'])

# To select columns where a row matches a condition:
print(df_1.loc[:, df_1.loc['B'] < 1])

# Multiple conditions (use & instead of and, | instead of or)
print(df_1[(df_1['X'] > 0) & (df_1['Y'] > 0)])

# Get boolean DataFrame marking null values
print(df_1.isnull())

# For each colum/row, get the row/column that has the maximum value
print(df_1.idxmax(axis=0))
print(df_1.idxmax(axis=1))

# MULTIPLE INDEXES

outside = ['G1', 'G1', 'G1', 'G2', 'G2', 'G2']
inside = [1, 2, 3, 1, 2, 3]
hier_index = list(zip(outside, inside))
hier_index = pd.MultiIndex.from_tuples(hier_index)

# Build a multi-index (multi-level index, index hierarchy) DataFrame
multi_ix_df = pd.DataFrame(randn(6, 2), hier_index, ['A', 'B'])

print(multi_ix_df.loc['G1'])
print(multi_ix_df.loc['G1'].iloc[1])

# Indexes have no names by default. Can assign names
print(multi_ix_df.index.names)
multi_ix_df.index.names = ['Groups', 'Num']

print(multi_ix_df.loc['G2'].loc[2]['B'])

# Cross section. Allows to select parts of the DataFrame and skip other parts. Example: get bot rows with subindex 1
print(multi_ix_df.xs(1, level='Num'))


