import pandas as pd

old = pd.read_csv("resources/animalcrossing_reviews/user_reviews.csv")
new = pd.read_csv("resources/animalcrossing_reviews/user_reviews.csv")
alt = pd.read_csv("resources/animalcrossing_reviews/user_reviews.csv")

# https://pandas.pydata.org/pandas-docs/stable/getting_started/basics.html#iteration
# Iterating through pandas objects is generally slow. In many cases, iterating manually over the rows is not needed and
# can be avoided (using) a vectorized solution: many operations can be performed using built-in methods or
# NumPy functions, (boolean) indexing

# 1. Create column QualitativeReview, based on quantitative review

# 1.1 Bad solution. Iterate over rows
old["QualitativeRating"] = ""

for ix in old.index:
    if old.loc[ix, "grade"] < 5:
        old.loc[ix, "QualitativeRating"] = "bad"
    elif old.loc[ix, "grade"] == 5:
        old.loc[ix, "QualitativeRating"] = "ok"
    elif old.loc[ix, "grade"] > 5:
        old.loc[ix, "QualitativeRating"] = "good"

# 1.2 Better solution. Vectorized
new["QualitativeRating"] = ""
new.loc[new.grade < 5, "QualitativeRating"] = "bad"
new.loc[new.grade == 5, "QualitativeRating"] = "ok"
new.loc[new.grade > 5, "QualitativeRating"] = "good"


# 1.3 Alternative solution. Vectorized with apply function over rows
def compute_qualitative_rating(row):
    if row.grade < 5:
        return "bad"
    elif row.grade == 5:
        return "ok"
    elif row.grade > 5:
        return "good"


alt["QualitativeRating"] = alt.apply(compute_qualitative_rating, axis=1)

# 2. Create column with the length of another column

new["TextLen"] = new["text"].str.len()

# 3. Create column from computation based on several conditions

new["SuperCategory"] = "normal"
new.loc[(new["TextLen"] >= 1000) & (new["grade"] > 9), "SuperCategory"] = "super fan"
new.loc[(new["TextLen"] >= 1000) & (new["grade"] <= 1), "SuperCategory"] = "super hater"
