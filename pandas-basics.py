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

# Create a DataFrame specifying the row and column indexes
df_1 = pd.DataFrame(data=randn(5, 4), index=['A', 'B', 'C', 'D', 'E'], columns=['W', 'X', 'Y', 'Z'])


