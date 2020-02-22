import os
import pandas as pd
import chardet
from encodings.aliases import aliases

if not os.getcwd().endswith("etl"):
    os.chdir("./data_science/lessons/etl")

# UTF-8 is the most common. Pandas assumes loaded files to be UTF-8 encoded by default. So no problem reading this file
df = pd.read_csv('./data/population_data.csv', skiprows=4)

# But his file is in an unknown encoding. The encoding argument specifies an encoding to read the file
df = pd.read_csv('./data/mystery.csv')

# Aliases of encodings supported in Python
encoding_alias_values = set(aliases.values())

df_mistery = None
correct_encodings = []

# Brute force: iterate through the alias_values list trying out the different encodings to see which one or ones work
for encoding_alias in encoding_alias_values:
    try:
        df_mistery = pd.read_csv('./data/mystery.csv', encoding=encoding_alias)
        correct_encodings.append(encoding_alias)
    except Exception as err:
        print(f"Encoding: '{encoding_alias}' failed ({err})")

print(f"Correct encodings: {correct_encodings}")

# Use the chardet library (pip install chardet)
# The detect method finds the encoding
with open("data/mystery.csv", 'rb') as file:
    print(chardet.detect(file.read()))
