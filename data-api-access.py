import requests
import matplotlib.pyplot as plt
from collections import defaultdict

# Get request for data hosted in the WorldBank API. With static parameters. Uses the requests library:
# https://requests.readthedocs.io/en/master/
r = requests.get('http://api.worldbank.org/v2/countries/br/indicators/NY.GDP.MKTP.CD?format=xml')
print(r.text)

# Request with dynamic parameters. Decode results as JSON
payload = {'format': 'json', 'per_page': '500', 'date':'1990:2015'}
r = requests.get('http://api.worldbank.org/v2/countries/br/indicators/NY.GDP.MKTP.CD', params=payload)
res_json = r.json()

print(f"Metadata: \n{res_json[0]}\n\nData: \n{res_json[1]}")

# get the World Bank GDP data for Brazil, China and the United States
payload = {'format': 'json', 'per_page': '500', 'date': '1990:2016'}
r = requests.get('http://api.worldbank.org/v2/countries/br;cn;us/indicators/NY.GDP.MKTP.CD', params=payload)

# Put the results in a dictionary where each country contains a list of all the x values and all the y values
# this will make it easier to plot the results
data = defaultdict(list)

for entry in r.json()[1]:
    # check if country is already in dictionary. If so, append the new x and y values to the lists
    if entry['country']['value'] not in data:
        # if country not in dictionary, then initialize the lists that will hold the x and y values
        data[entry['country']['value']] = [[], []]

    data[entry['country']['value']][0].append(int(entry['date']))
    data[entry['country']['value']][1].append(float(entry['value']))

# Show the results contained in the data dictionary
for country in data:
    print(country)
    print(data[country][0])
    print(data[country][1])
    print('\n')

# create a plot for each country
for country in data:
    plt.plot(data[country][0], data[country][1], label=country)

# label the plot
plt.title('GDP for Brazil, China, and USA 1990 to 2015')
plt.legend()
plt.xlabel('year')
plt.ylabel('GDP')
plt.show()


payload = {'format': 'json', 'date': '2013:2016', 'per_page': '500'}

r = requests.get("http://api.worldbank.org/v2/countries/cn;in;co/indicators/SP.POP.GROW", params=payload)
res_popul_growth = r.json()

popul_growth_meta = res_popul_growth[0]
popul_growth_data = res_popul_growth[1]

data = defaultdict(list)
for entry in popul_growth_data:
    cur_country = entry['country']['value']

    if cur_country not in data:
        data[cur_country] = [[], []]

    data[cur_country][0].append(int(entry['date']))
    data[cur_country][1].append(float(entry['value']))

print(data)
