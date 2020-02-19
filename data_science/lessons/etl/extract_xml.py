import pandas as pd
from bs4 import BeautifulSoup

# Pandas cannot read XML directly. Use BeautifulSoup for that purpose

# Open the population_data.xml file and load into Beautiful Soup
with open("./data/population_data.xml") as fp:
    # lxml is the Parser type
    soup = BeautifulSoup(fp, "lxml")

    # Output the first 5 records in the xml file. Example of how to navigate the XML document with BeautifulSoup
    i = 0

    # Use the find_all method to get all record tags in the document
    for record in soup.find_all('record'):
        # use the find_all method to get all fields in each record
        i += 1

        for field in record.find_all('field'):
            print(f"{field['name']}: {field.text}")

        print()

        if i == 5:
            break

# Create a Pandas DataFrame from an XML document

# Build a dictionary where keys are indexes of rows and values are dictionaries with the values of columns
with open("./data/population_data.xml") as xml_file:
    xml_soup = BeautifulSoup(xml_file, "lxml")

    # Iterate through the records
    dict_indexes = {}

    for record in xml_soup.find_all("record"):
        dict_columns = {}

        for field in record.find_all("field"):
            dict_columns[field["name"]] = field.text

        dict_indexes[len(dict_indexes)] = dict_columns

df_data = pd.DataFrame.from_dict(dict_indexes, orient="index")
