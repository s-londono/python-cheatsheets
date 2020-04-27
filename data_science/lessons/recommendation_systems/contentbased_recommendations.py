import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from IPython.display import HTML
import tests as t
import pickle

if not os.getcwd().endswith("recommendation_systems"):
    os.chdir("data_science/lessons/recommendation_systems")

# Dataframe of all movies in the dataset along with other content related information about the movies (genre and date)
movies = pd.read_csv('data/movies_clean.csv')

# Main DataFrame used for collaborative filtering, as it contains all of the interactions between users and movies.
reviews = pd.read_csv('data/reviews_clean.csv')

del movies['Unnamed: 0']
del reviews['Unnamed: 0']

# Dictionary where each key is a user, and value is a list of movie recommendations based on collaborative filtering
all_recs = pickle.load(open("data/all_recs.p", "rb"))

# When User-Based Recommendations cannot be made, because of lack of data about users, Content-Based Recommendations
# are a good alternative.

# 1. Find all users who didn't get all 10 ratings we would have liked them to have using collaborative filtering
users_with_all_recs = []
users_who_need_recs = []

for user_id, movie_recs in all_recs.items():
    if movie_recs is None or len(movie_recs) < 10:
        users_who_need_recs.append(user_id)
    else:
        users_with_all_recs.append(user_id)

# Do a bit of a mix of content and collaborative filtering to make recommendations for the users this time.
# This will allow to obtain recommendations in many cases where we didn't make recommendations earlier

# 2. Before finding recommendations, rank the user's ratings from highest to lowest. You will move through
# the movies in this order looking for other similar movies.
# Create a dataframe similar to reviews, but ranked by rating for each user
user_ranked_reviews = reviews.sort_values(by=["user_id", "rating"], ascending=False)

# 3. Perform the dot product on a matrix of movies with content characteristics to provide a movie by movie matrix
# where each cell is an indication of how similar two movies are to one another
# Create a numpy array that is a matrix of indicator variables related to year (by century) and movie genres by movie.
# Perform the dot product of this matrix with itself (transposed) to obtain a similarity matrix of each movie with
# every other movie

# 3.1 Subset so movie_content is only using the dummy variables for genres and the 3 century based year dummy columns
movie_content = movies.loc[:, ["movie_id"] + movies.columns[4:].to_list()]
movie_content.set_index("movie_id", drop=True, inplace=True)

# 3.2 Take the dot product to obtain a movie x movie matrix of similarities
movie_similarities = movie_content.dot(movie_content.transpose())

dot_prod_movies = movie_similarities.to_numpy()


