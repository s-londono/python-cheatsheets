import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tests as t

if not os.getcwd().endswith('recommendation_systems'):
    os.chdir('data_science/lessons/recommendation_systems')

# Read in the datasets
movies = pd.read_csv('data/movies_clean.csv')
reviews = pd.read_csv('data/reviews_clean.csv')

movies.drop(columns='Unnamed: 0', inplace=True)
reviews.drop(columns='Unnamed: 0', inplace=True)

# 1. No matter the user, we need to provide a list of the recommendations based on simply the most popular items
# For this task, we will consider what is "most popular" based on the following criteria:
# - A movie with the highest average rating is considered best
# - With ties, movies that have more ratings are better
# - A movie must have a minimum of 5 ratings to be considered among the best movies
# - If movies are tied in their average rating and number of ratings, the ranking is determined by the movie
#   that is the most recent rating
#
# With these criteria, the goal is to take a user_id and provide back the n_top recommendations. Use the function
# below as the scaffolding that will be used for all the future recommendations as well

# Compute stats by movie
movie_groups = reviews.groupby("movie_id")
movie_stats = pd.DataFrame(index=movie_groups.indices)
movie_stats["rating_avg"] = movie_groups["rating"].mean()
movie_stats["rating_count"] = movie_groups["rating"].count()
movie_stats["last_rating_time"] = movie_groups["timestamp"].max()


def popular_recommendations(user_id, n_top):
    """
    INPUT:
    user_id - the user_id of the individual you are making recommendations for
    n_top - an integer of the number recommendations you want back
    OUTPUT:
    top_movies - a list of the n_top recommended movies by movie title in order best to worst
    """
    # Do stuff
    movie_stats.loc[328107, "rating_avg"]

    top_movies = None

    return top_movies  # a list of the n_top movies as recommended

