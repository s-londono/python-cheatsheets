# https://towardsdatascience.com/how-to-use-multiindex-in-pandas-to-level-up-your-analysis-aeac7f451fce

from numpy.random import randn
import pandas as pd

df = pd.DataFrame(data=randn(5, 4), index=['A', 'B', 'C', 'D', 'E'], columns=['W', 'X', 'Y', 'Z'])

# Check index names (for a DataFrame with a single index, returns None)
print(df.index.names)

# Create a MultiIndex from some of the columns of the DataFrame. Note: Invoking sort_index is important for performance!
df_multi = df.set_index(["W", "X", "Y"]).sort_index()
print(df_multi.index.names)

# Check index values (tuples)
print(df_multi.index.values)

# Remove MultiIndex (hierarchical index)
df_single_ix = df_multi.reset_index()
print(df_single_ix.index.names)

# Get column values at index
print(df_multi.loc[(1.2752988309794162, -0.07034473574829656, 0.35158211807537004), :])
print(df_multi.loc[1.2752988309794162, :])

# Use the slice command as a wildcard when selecting by some indexes.
# Refer to: https://docs.python.org/3.8/library/functions.html#slice
print(df_multi.loc[(1.2752988309794162, slice(None), 0.35158211807537004), :])

# Select multiple values of a specific dimension of the MultiIndex
print(df_multi.loc[(1.2752988309794162, [-0.07034473574829656, 1]), :])

# Get elements having a specific value on a dimension of the MultiIndex (xs = CrossSection)
print(df_multi.xs(-0.07034473574829656, level="X"))

# Pivot table
pivoted = df.pivot_table(index=['Race', 'Character'],
                         columns='Film',
                         aggfunc='sum',
                         margins=True,  # total column
                         margins_name='All Films',
                         fill_value=0).sort_index()

order = [('Words', 'The Fellowship Of The Ring'),
         ('Words', 'The Two Towers'),
         ('Words', 'The Return Of The King'),
         ('Words', 'All Films')]

pivoted = pivoted.sort_values(by=('Words', 'All Films'), ascending=False)
pivoted = pivoted.reindex(order, axis=1)
