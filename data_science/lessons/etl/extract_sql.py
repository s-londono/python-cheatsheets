import os
import sqlite3
from sqlalchemy import create_engine
import pandas as pd

if not os.getcwd().endswith("etl"):
    os.chdir("./data_science/lessons/etl")

# DB ACCESS USING THE SQLITE3 CONNECTOR

# Connect to the database
conn = sqlite3.connect('./data/population_data.db')

# Run a query
df_query1 = pd.read_sql('SELECT * FROM population_data', conn)

df_query2 = pd.read_sql('SELECT "Country_Name", "Country_Code", "1960" FROM population_data', conn)

# DB ACCESS USING SQLALCHEMY

###
# Create a database engine to find the correct file path, use the python os library:
# print(os.getcwd())
###

engine = create_engine('sqlite:////home/workspace/3_sql_exercise/population_data.db')

df_query3 = pd.read_sql("SELECT * FROM population_data", engine)

filters = ["Aruba", "Population, total"]

df_aruba_populations = pd.read_sql("SELECT \"Country_Name\", (\"1961\" - \"1960\") AS Population_Change FROM " +
                                   "population_data WHERE Country_name = ? AND Indicator_Name = ?",
                                   con=engine, params=filters)

filters_1 = ["BEL", "LUX", "Population, total"]

df_bel_lux_populations = pd.read_sql("SELECT \"Country_Name\", \"1975\" FROM population_data WHERE " +
                                     "(Country_Code = ? OR Country_Code = ?) AND Indicator_Name = ?",
                                     con=engine, params=filters_1)
