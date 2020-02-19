import os
import requests
import pandas as pd

if not os.getcwd().endswith("etl"):
    os.chdir("./data_science/lessons/etl")

# Request data in JSON format via HTTP
url = 'http://api.worldbank.org/v2/countries/br;cn;us;de/indicators/SP.POP.TOTL/?format=json&per_page=1000'
r = requests.get(url)

result = r.json()

# Request rural population for Switzerland
url_swiss = 'http://api.worldbank.org/v2/country/ch/indicator/SP.RUR.TOTL?format=json&per_page=1000'
r = requests.get(url_swiss)

result_swiss = r.json()

print(f"Header: {result_swiss[0]}\n")

df_swiss_rural = pd.DataFrame(result_swiss[1])
