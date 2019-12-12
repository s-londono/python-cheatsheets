import os
import pandas as pd

os.chdir("/home/slondono/projects/python-labs/python-cheatsheets")

# Open a CSV file
df = pd.read_csv("resources/portland-oregon-crime-data.csv")

# Get general information about the DataFrame
df.describe()

# Shuffle the DataFrame (in the shuffled DataFrame, reset indexes so that they start at 0)
shfld_df = df.sample(frac=1).reset_index(drop=True)

# Access a column (result is a Series)
df.columns
col_case_num = df["Case Number"]

# Access multiple columns (results in a DataFrame, a subset of the original)
sub_df = type(df[["Address", "Case Number", "Report Date"]])

# Access multiple columns using their indexes
col_names = df.columns[2:5]
sub_df_1 = df[col_names]

# Access a whole row
rown_5 = df.iloc[5]

# Access a specific entry of a column
entry = df["Case Number"].iloc(2)

# Access a range of rows (results in a DataFrame, a subset of the original)
rows = df[5:100]

# Access a subset of the DataFrame
sub_df_2 = df[df.columns[0:4]].iloc[100:150]
sub_df_3 = df.iloc[100:150, 0:4]




