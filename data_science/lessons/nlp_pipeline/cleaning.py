import requests
from bs4 import BeautifulSoup

# fetch web page
r = requests.get("https://www.udacity.com/courses/all")

soup = BeautifulSoup(r.text, "lxml")

# Find all course summaries
summaries = soup.find_all("div", class_="course-summary-card")
print('Number of Courses:', len(summaries))

# Print the first summary in summaries. Use prettify to display HTML in an easy to read format
print(summaries[0].prettify())

# Extract course title
print(summaries[1].select_one("h3.card-heading a").get_text())

# Extract school
print(summaries[1].select_one("h4.category").get_text())

# Extract the name and school from every course
courses = []
for summary in summaries:
    # append name and school of each summary to courses list
    course_name = summary.select_one("h3.card-heading a")
    school_name = summary.select_one("h4.category")

    if course_name is not None and school_name is not None:
        courses.append((course_name.get_text(), school_name.get_text()))

# Display results
print(len(courses), "course summaries found. Sample:")
courses[:20]

