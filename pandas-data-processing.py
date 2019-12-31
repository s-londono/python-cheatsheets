import numpy as np
import pandas as pd

# MISSING DATA

d_1 = {'A': [1, 2, np.nan], 'B': [5, np.nan, np.nan], 'C': [1, 2, 3]}
df_1 = pd.DataFrame(d_1)

# Remove rows/columns containing one or more NaN values. The thres argument controls how many not NaN values must
# have a row/column to be kept
print(df_1.dropna())
print(df_1.dropna(axis=1))

# Fill NaNs with a specific value
print(df_1.fillna(value='BAD'))

# Fill NaNs in a column with the mean of that column
print(df_1['A'].fillna(value=df_1['A'].mean()))

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
print(pd.concat([df1, df2, df3]))

left = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'], 'A': ['A0', 'A1', 'A2', 'A3'], 'B': ['B0', 'B1', 'B2', 'B3']})

right = pd.DataFrame({'key': ['K0', 'K1', 'K2', 'K3'], 'C': ['C0', 'C1', 'C2', 'C3'], 'D': ['D0', 'D1', 'D2', 'D3']})

# Merging joins DataFrames together using a similar logic as SQL joins. Can join on multiple keys (on=['key1',...])
print(pd.merge(left, right, how='inner', on='key'))

left_1 = pd.DataFrame({'A': ['A0', 'A1', 'A2'], 'B': ['B0', 'B1', 'B2']}, index=['K0', 'K1', 'K2'])

right_1 = pd.DataFrame({'C': ['C0', 'C2', 'C3'], 'D': ['D0', 'D2', 'D3']}, index=['K0', 'K2', 'K3'])

# Joining is a convenient method for combining the columns of two potentially differently-indexed DataFrames
# into a single result DataFrame. Joins DataFrames by their indices. Can also use argument 'how'
print(left_1.join(right_1))
print(left_1.join(right_1, how='outer'))

