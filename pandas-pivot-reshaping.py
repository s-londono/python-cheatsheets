import pandas as pd

df = pd.DataFrame({"Seqnc": [0, 0, 0, 1, 1, 1, 2, 2, 2, 3, 3],
                   "Varia": ["x", "y", "z", "x", "y", "z", "x", "y", "z", "x", "z"],
                   "Value": [0.1, 0.2, 0.3, 0.4, 0.5, 0.6, 0.7, 0.8, 0.9, 1.0, 1.1]})

# Convert from 'Record Format' to 'Time Series Format'
# Reshape table by making columns from the different variable values
simple_pivot = df.pivot(index="Seqnc", columns="Varia", values="Value")

# Pivot is highly memory consuming. Alternative:
# https://stackoverflow.com/questions/39648991/pandas-dataframe-pivot-memory-error
light_pivot = df.groupby(["Seqnc", "Varia"])["Value"].max().unstack()

