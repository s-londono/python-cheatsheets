# Gathering & Wrangling
import numpy as np
import pandas as pd

df_2 = pd.DataFrame({'Company': ['GOOG', 'GOOG', 'MSFT', 'MSFT', 'APPL', 'APPL'],
                     'Person': ['Sam', 'Charlie', 'Amy', 'Vanessa', 'Carl', 'Sarah'],
                     'Sales': [200, 120, 340, 124, 243, 350]})

# Histogram
df_2['Sales'].hist(bins=10)

df_2.style.bar(subset='Sales', align='mid', color=['#d65f5f', '#5fba7d'])

df_2.to_html().disp

