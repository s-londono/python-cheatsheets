import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# MISSING DATA

d_1 = {'A': [1, 2, np.nan], 'B': [5, np.nan, np.nan], 'C': [1, 2, 3]}
df_1 = pd.DataFrame(d_1)

# Remove rows/columns containing one or more NaN values. The thres argument controls how many NaN values may a
# row/column have in order to be kept
print(df_1.dropna())
print(df_1.dropna(axis=1))

# Copy a DataFrame
copy_df_1 = df_1.copy()

# Fill NaNs with a specific value
print(df_1.fillna(value='BAD'))

# Fill NaNs in a column with the mean of that column
print(df_1['A'].fillna(value=df_1['A'].mean()))

# Rename columns
print(df_1.rename(columns={'A': 'a', 'B': 'b'}, inplace=False))

# Rename columns directly
df_1.columns = ['A1', 'A2', 'A3']

# GROUP-BY

df_2 = pd.DataFrame({'Company': ['GOOG', 'GOOG', 'MSFT', 'MSFT', 'APPL', 'APPL'],
                     'Person': ['Sam', 'Charlie', 'Amy', 'Vanessa', 'Carl', 'Sarah'],
                     'Sales': [200, 120, 340, 124, 243, 350]})

# Group by a specific column. Creates a group-by object
gb_1 = df_2.groupby('Company')

# Perform an aggregate operation on groups defined by the group-by object. Result is a DataFrame
print(gb_1.mean())
print(gb_1.sum())
print(gb_1.std())
print(gb_1.min())
print(gb_1.max())

# Perform aggregate operation on a particular column
print(gb_1['Sales'].mean())

# Compute common statistics on groups
gb_1.describe()
gb_1.describe().transpose()

# MERGE, JOIN, CANCATENATE

df1 = pd.DataFrame({'A': ['A0', 'A1', 'A2', 'A3'], 'B': ['B0', 'B1', 'B2', 'B3'],
                    'C': ['C0', 'C1', 'C2', 'C3'], 'D': ['D0', 'D1', 'D2', 'D3']},
                   index=[0, 1, 2, 3])

df2 = pd.DataFrame({'A': ['A4', 'A5', 'A6', 'A7'], 'B': ['B4', 'B5', 'B6', 'B7'],
                    'C': ['C4', 'C5', 'C6', 'C7'], 'D': ['D4', 'D5', 'D6', 'D7']},
                   index=[4, 5, 6, 7])

df3 = pd.DataFrame({'A': ['A8', 'A9', 'A10', 'A11'], 'B': ['B8', 'B9', 'B10', 'B11'],
                    'C': ['C8', 'C9', 'C10', 'C11'], 'D': ['D8', 'D9', 'D10', 'D11']},
                   index=[8, 9, 10, 11])

# Concatenation basically glues together DataFrames. Keep in mind that dimensions should match along the axis
# you are concatenating on. You can use pd.concat and pass in a list of DataFrames to concatenate together. By
# default concatenates on axis 0 (rows)
print(pd.concat([df1, df2, df3], axis=1))

left = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'], 'A': ['A0', 'A1', 'A2', 'A3'], 'B': ['B0', 'B1', 'B2', 'B3']})

right = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'], 'C': ['C0', 'C1', 'C2', 'C3'], 'D': ['D0', 'D1', 'D2', 'D3']})

# Merging joins DataFrames together using a logic similar to SQL joins. Can join on multiple keys (on=['key1',...])
print(pd.merge(left, right, how='inner', on='key'))

left_1 = pd.DataFrame({'A': ['A0', 'A1', 'A2'], 'B': ['B0', 'B1', 'B2']}, index=['K0', 'K1', 'K2'])

right_1 = pd.DataFrame({'C': ['C0', 'C2', 'C3'], 'D': ['D0', 'D2', 'D3']}, index=['K0', 'K2', 'K3'])

# Joining is a convenient method for combining the columns of two potentially differently-indexed DataFrames
# into a single result DataFrame. Joins DataFrames by their indices. Can also use argument 'how'
print(left_1.join(right_1))
print(left_1.join(right_1, how='outer'))

# OPERATIONS ON DATAFRAMES

df = pd.DataFrame({'col1': [1, 2, 3, 4], 'col2': [444, 555, 666, 444], 'col3': ['abc', 'def', 'ghi', 'xyz']})

# Return the first n rows of a DataFrame (5 by default)
df.head(n=3)

# Get unique values in a specific column (as a Numpy array)
print(df['col2'].unique())

# Number of unique values in a specific column (alternative to len)
print(df['col1'].nunique())

# Count how many times each value present in a column appears in the column. Very useful for categorical variables
print(df['col2'].value_counts())

# Plot proportion of values of items of a categorical column
c1_vals = df_2['C1'].value_counts()
(c1_vals/df_2.shape[0]).plot(kind="bar")
plt.title("What kind of developer are you?")

# Find columns having no NaNs
print({e for e in df_1 if not df_1[e].hasnans})

# Find columns with most of their values missing (more than 75% of values in column are NaNs)
print({c for c in df_1 if (df_1[c].count() / df_1[c].size) < 0.25})
print(set(df_1.columns[df_1.isnull().mean() > 0.75]))

# Sort a dataframe by a specific column
print(df.sort_values('col2'))
print(df.sort_values(by=['col2', 'col3'], ascending=True))

# Note that not using copy results in a strange warning. Slicing somehow causes the result to be a view and not a copy
df_copy_res = df_1[["ArrTime", "CRSArrTime", "ArrDelay"]].copy()
df_copy_res["DiffArrTime"] = (df_copy_res["ArrTime"] - df_copy_res["CRSArrTime"])

# PIVOTING
# Transform a DataFrame by taking the values of specific sets of columns as indices, columns and values.
# Useful to convert a set of points provided in tabular format to an n-dimensional representation.

df_pv_1 = pd.DataFrame({'a': ['r1', 'r1', 'r1', 'r2', 'r2', 'r2', 'r3', 'r3', 'r3'],
                        'b': ['c1', 'c2', 'c3', 'c1', 'c2', 'c3', 'c1', 'c2', 'c3'],
                        'v': [1, 2, 3, 4, 5, 6, 7, 8, 9]})

df_pv_2 = df_pv_1.pivot_table(values='v', index='a', columns='b')

# Pivot can also build multiple indexes
df_pv_3 = pd.DataFrame({'A': ['foo', 'foo', 'foo', 'bar', 'bar', 'bar'],
                        'B': ['one', 'one', 'two', 'two', 'one', 'one'], 'C': ['x', 'y', 'x', 'y', 'x', 'y'],
                        'D': [1, 3, 2, 5, 4, 1]})

df_pv_4 = df_pv_3.pivot_table(values='D', index=['A', 'B'], columns='C')

# MELTING
# Unpivot a DataFrame from wide to long format, optionally leaving identifiers set.
df_to_melt = pd.DataFrame({'Country': {0: 'US', 1: 'DE', 2: 'FR'}, '2000': {0: 0.5, 1: 0.2, 2: 0.0},
                           '2001': {0: 0.7, 1: 1.2, 2: 3.0}, 'AUX': {0: 4, 1: 1, 2: 7}})

# melt year columns  and convert year to date time
df_melt2 = df_to_melt.melt(id_vars=['Country'], value_vars=['2000', '2001'])
df_melt2.columns = ['country', 'year', 'variable']
df_melt2['year'] = df_melt2['year'].astype('datetime64[ns]').dt.year

# DROPPING ROWS AND COLUMNS

data = {'name': ['Jason', 'Molly', 'Tina', 'Jake', 'Amy'],
        'year': [2012, 2012, 2013, 2014, 2014],
        'reports': [4, 24, 31, 2, 3]}

df_drop = pd.DataFrame(data, index=['Cochice', 'Pima', 'Santa Cruz', 'Maricopa', 'Yuma'])

# Drop an observation (row)
df_drop.drop([['Choice', 'Pima']])

# Drop a variable (column)
df_drop.drop('reports', axis=1)

# Drop rows that contain a certain value
reduced_df = df_drop[df_drop.name != 'Tina']
reduced_df6 = df_drop[np.isfinite(df_drop['name'])]

# Drop rows by number
reduced_df1 = df_drop.drop(df_drop.index[2])
reduced_df2 = df_drop.drop(df_drop.index[1, 2, 4])
reduced_df3 = df_drop.drop(df_drop.index[-2])

# Relative select range (drop the rest). Here, keep top 3
reduced_df4 = df_drop[:3]

# Drop relative range (keep the rest). Here, drop bottom 3
reduced_df5 = df_drop[:-3]

# Drop all rows or columns that contain at least a null value (axis=0 rows, axis=1 columns)
reduced_df7 = df_drop.dropna(axis=0)

# Drop all rows or columns with all values null (axis=0 rows, axis=1 columns)
reduced_df7 = df_drop.dropna(axis=0, how='all')

# Drop all rows or columns with a specific column has null any values (axis=0 rows, axis=1 columns)
reduced_df8 = df_drop.dropna(subset=['name'], axis=0)

# Drop rows where several columns match a condition
reduced_df8 = df_drop.dropna(subset=['name', 'year'], axis=0)
# ...which is the same as the more convoluted way:
reduced_df9 = df_drop[(pd.isnull(df_drop.iloc[:, 0]) == False) & (pd.isnull(df_drop.iloc[:, 2]) == False)]

# IMPUTING COLUMNS

# Impute missing entries on each column using the mode of the column
fill_mode = lambda col: col.fillna(col.mode()[0])
df_drop.apply(fill_mode, axis=0)

# IMPUTING USING A COMPUTED SERIES

df_data = pd.DataFrame({"a": [100, 200, 300], "b": [2, np.nan, 3], "c": [np.nan, 4, np.nan]})
sr_fill = df_data["a"] / 5.0
df_data.apply(lambda c: c.fillna(sr_fill))

df_data["b"].fillna(sr_fill, inplace=True)

# Transform a column
df_data.loc[:, "a"] = df_data["a"].transform(lambda a: a ** 2)

# Convert data types (can use data types from np.dtypes and Python data types)
df_data = df_data.astype({"a": "str", "b": "int64", "c": "float64"})

df_melt2['year'] = df_melt2['year'].astype('datetime64[ns]').dt.year
