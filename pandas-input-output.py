# REQUIREMENTS
# sqlalchemy
# lxml
# html5lib
# BeautifulSoup4
# xlrd
import pandas as pd
from sqlalchemy import create_engine

# Read CSV file
df_csv = pd.read_csv('resources/example', skiprows=0)

# Write CSV file (use index=False to avoid writing the sequential index introduced by Pandas)
df_csv.to_csv('resources/my_output', index=False)

# Read Excel file. Pandas interprets each sheet as a DataFrame
df_xls = pd.read_excel('resources/Excel_Sample.xlsx', sheet_name='Sheet1')

# Write Excel file
df_xls.to_excel('resources/Excel_Output.xlsx', sheet_name='Sheet1')

# Read HTML. Result is not necessarily a DataFrame. Usually is a list, with tables from the HTML page as DataFrames
out_html = pd.read_html('http://www.fdic.gov/bank/individual/failed/banklist.html')
df_html = out_html[0]
print(f"Type of first HTML result element: {type(out_html)}. Data:\n{df_html.head()}")

# SQL DEMO
# Normally, would have to use an appropriate driver to connect to and read from a DB

# Create a simple in-memory database for testing purposes
im_sql_engine = create_engine('sqlite:///:memory:')

# Write a DataFrame to a DB engine, as a table
df_html.to_sql('failed_banks', im_sql_engine)

# Read from an SQL table
df_sql = pd.read_sql('failed_banks', con=im_sql_engine)
