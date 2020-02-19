import os
import pandas as pd

if not os.getcwd().endswith("etl"):
    os.chdir("./data_science/lessons/etl")

df_electricity = pd.read_csv("./data/electricity_access_percent.csv", dtype="str", skiprows=4)
df_rural_popul = pd.read_csv("./data/rural_population_percent.csv", dtype="str", skiprows=4)

df_electricity.drop(columns="Unnamed: 62", inplace=True)
df_rural_popul.drop(columns="Unnamed: 62", inplace=True)

# Combine the two data sets together using the concat method. In other words, all of the rows of df_rural
# will come first followed by all the rows in df_electricity. This is possible to do because they both
# have the same column names
df_rural_and_elect = pd.concat([df_rural_popul, df_electricity])

df_elec_unpvt = df_electricity.melt(id_vars=df_electricity.columns[:4], var_name="Year", value_name="Electricity Value")
df_rural_popl_unpvt = df_rural_popul.melt(id_vars=df_rural_popul.columns[:4], var_name="Year", value_name="Rural Value")

df_elec_unpvt.drop(columns=["Indicator Name", "Indicator Code"], inplace=True)
df_rural_popl_unpvt.drop(columns=["Indicator Name", "Indicator Code"], inplace=True)

df_merged = pd.merge(df_rural_popl_unpvt, df_elec_unpvt, how="outer", on=['Country Name', 'Country Code', 'Year'])

df_merged.sort_values(by=["Country Code", "Year"], inplace=True)
