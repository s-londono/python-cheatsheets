# import statements
import requests
from bs4 import BeautifulSoup

# fetch web page
r = requests.get("https://www.udacity.com/courses/all")

soup = BeautifulSoup(r.text, "lxml")

# Find all course summaries
summaries = soup.find_all("div", class_="card__expander--summary")
print('Number of Courses:', len(summaries))

# print the first summary in summaries
print(summaries[0].find("span").prettify())

