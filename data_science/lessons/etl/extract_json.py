import json
import pandas as pd

# OPTION 1: READ JSON USING PANDAS

# Read JSON in a 'records' representation
df_json = pd.read_json("./data/population_data.json", orient="records")

df_json.head()

# OPTION 2: READ JSON USING THE JSON LIBRARY

with open("./data/population_data.json") as f:
    json_data = json.load(f)

print(json_data[0])
print("\n")

# JSON data is essentially a dictionary
print(json_data[0]["Country Name"])
print(json_data[0]["Country Code"])
