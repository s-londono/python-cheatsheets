import pandas as pd

d = pd.read_html("https://finance.yahoo.com/quote/TSLA/profile?p=TSLA")[0]

print(d.head(20))
