import os
import sqlite3
import pandas as pd
import numpy as np

if not os.getcwd().endswith("etl"):
    os.chdir("./data_science/lessons/etl")


# Generator for reading in one line at a time. Generators are useful for data sets that are too large to fit in RAM
def extract_lines(file):
    while True:
        line = file.readline()
        if not line:
            break
        yield line


# Create a database and a table, called gdp, to hold the gdp data

# Connect to the database
conn = sqlite3.connect('/tmp/worldbank.db')
cur = conn.cursor()

cur.execute("DROP TABLE IF EXISTS gdp")

cur.execute(f"CREATE TABLE gdp (countryname TEXT, countrycode TEXT, year INTEGER, gdp REAL, "
            f"PRIMARY KEY (countrycode, year));")

conn.commit()
conn.close()

# TODO: fill out the code wherever you find a TODO in this cell
# This function has two inputs:
#   data, which is a row of data from the gdp csv file
#   colnames, which is a list of column names from the csv file
# The output should be a list of [countryname, countrycode, year, gdp] values
# In other words, the output would look like:
# [[Aruba, ABW, 1994, 1.330168e+09], [Aruba, ABW, 1995, 1.320670e+09], ...]


# transform the indicator data
def transform_indicator_data(data, colnames):
    """
    This function has two inputs:
    - Data, which is a row of data from the gdp csv file
    - Colnames, which is a list of column names from the csv file
    The output should be a list of [countryname, countrycode, year, gdp] values. The output would look like:
    [[Aruba, ABW, 1994, 1.330168e+09], [Aruba, ABW, 1995, 1.320670e+09], ...]
    """
    # Get rid of quote marks
    for i, datum in enumerate(data):
        data[i] = datum.replace('"', '')

    # The data variable contains a list of data in the form [countryname, countrycode, 1960, 1961, 1962,...]
    # since this is the format of the data in the csv file. Extract the countryname from the list
    # and put the result in the country variable
    country = data[0]

    # These are "countryname" values that are not actually countries
    non_countries = ['World',
                     'High income',
                     'OECD members',
                     'Post-demographic dividend',
                     'IDA & IBRD total',
                     'Low & middle income',
                     'Middle income',
                     'IBRD only',
                     'East Asia & Pacific',
                     'Europe & Central Asia',
                     'North America',
                     'Upper middle income',
                     'Late-demographic dividend',
                     'European Union',
                     'East Asia & Pacific (excluding high income)',
                     'East Asia & Pacific (IDA & IBRD countries)',
                     'Euro area',
                     'Early-demographic dividend',
                     'Lower middle income',
                     'Latin America & Caribbean',
                     'Latin America & the Caribbean (IDA & IBRD countries)',
                     'Latin America & Caribbean (excluding high income)',
                     'Europe & Central Asia (IDA & IBRD countries)',
                     'Middle East & North Africa',
                     'Europe & Central Asia (excluding high income)',
                     'South Asia (IDA & IBRD)',
                     'South Asia',
                     'Arab World',
                     'IDA total',
                     'Sub-Saharan Africa',
                     'Sub-Saharan Africa (IDA & IBRD countries)',
                     'Sub-Saharan Africa (excluding high income)',
                     'Middle East & North Africa (excluding high income)',
                     'Middle East & North Africa (IDA & IBRD countries)',
                     'Central Europe and the Baltics',
                     'Pre-demographic dividend',
                     'IDA only',
                     'Least developed countries: UN classification',
                     'IDA blend',
                     'Fragile and conflict affected situations',
                     'Heavily indebted poor countries (HIPC)',
                     'Low income',
                     'Small states',
                     'Other small states',
                     'Not classified',
                     'Caribbean small states',
                     'Pacific island small states']

    # Filter out country name values that are in the above list
    if country not in non_countries:
        # Convert the single row of data into a data frame. The advantage of converting a single row of data
        # into a data frame is that you can re-use code to clean the data

        # Convert the data variable into a 2D numpy array
        data_array = np.array(data, ndmin=2)

        # Reshape the data_array so that it is one row and 63 columns
        data_array = data_array.reshape((1, 63))

        # Convert the data_array variable into a pandas dataframe
        df = pd.DataFrame(data_array, columns=colnames)

        # Replace all empty strings in the dataframe with nan
        df.replace("", np.nan, inplace=True)
        df.replace("\n", np.nan, inplace=True)

        # Drop the 'Indicator Name' and 'Indicator Code' columns
        df.drop(["Indicator Name", "Indicator Code"], axis=1, inplace=True)

        # Reshape the data sets so that they are in long format. The id_vars should be Country Name and Country Code.
        # The variable of the melted column is year and its values will bet set in column gdp
        df_melt = df.melt(id_vars=["Country Name", "Country Code"], var_name="year", value_name="gdp")

        # For each row, extract the country, countrycode, year, and gdp values into a list.
        # If the gdp value is not null, append the row (in the form of a list) to the results variable
        results = []

        for _, row in df_melt.iterrows():
            if str(row["gdp"]) != "nan":
                results.append(row[["Country Name", "Country Code", "year", "gdp"]].to_list())

        return results


def load_indicator_data(results):
    """
    This function loads data into the gdp table of the worldbank.db database.
    The input is a list of data outputted from the transformation step that looks like this:
    [[Aruba, ABW, 1994, 1.330168e+09], [Aruba, ABW, 1995, 1.320670e+09], ...]
    The function does not return anything. Instead, the function iterates through the input and inserts each
    value into the gdp data set.
    """
    conn = sqlite3.connect("/tmp/worldbank.db")
    cur = conn.cursor()

    if results:

        # iterate through the results variable and insert each result into the gdp table
        for result in results:

            # Extract the countryname, countrycode, year, and gdp from each iteration
            countryname, countrycode, year, gdp = result

            # Prepare query to insert a countryname, countrycode, year, gdp value
            sql_string = "INSERT INTO gdp (countryname, countrycode, year, gdp) VALUES" +\
                "('{}', '{}', {}, {});".format(countryname.replace("'", "''"), countrycode, year, gdp)

            # connect to database and execute query
            try:
                cur.execute(sql_string)
            # print out any errors (like if the primary key constraint is violated)
            except Exception as e:
                print('Error occurred:', e, result)

    # commit changes and close the connection
    conn.commit()
    conn.close()

    return None


# Run the ETL pipeline
with open('data/gdp_data.csv') as f:
    # execute the generator to read in the file line by line
    for line in extract_lines(f):
        # split the comma separated values
        data = line.split(',')
        # check the length of the line because the first four lines of the csv file are not data
        if len(data) == 63:
            # check if the line represents column names
            if data[0] == '"Country Name"':
                colnames = []
                # get rid of quote marks in the results to make the data easier to work with
                for i, datum in enumerate(data):
                    colnames.append(datum.replace('"',''))
            else:
                # transform and load the line of indicator data
                results = transform_indicator_data(data, colnames)
                load_indicator_data(results)

# Output the values in the gdp table
conn = sqlite3.connect('/tmp/worldbank.db')
cur = conn.cursor()

# create the test table including project_id as a primary key
df = pd.read_sql("SELECT * FROM gdp", con=conn)

conn.commit()
conn.close()

print(df.head())
