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

# Do not consider movies with less than 5 ratings
candidate_movies = movie_stats[movie_stats["rating_count"] > 4].copy()

candidate_movies.sort_values(by=["rating_avg", "rating_count", "last_rating_time"], ascending=False, inplace=True)

# Another option is to join movies with ratings
movies.set_index("movie_id")
ranked_movies = movies.join(movie_stats)

def popular_recommendations(user_id, n_top):
    """
    INPUT:
    user_id - the user_id of the individual you are making recommendations for
    n_top - an integer of the number recommendations you want back
    OUTPUT:
    top_movies - a list of the n_top recommended movies by movie title in order best to worst
    """
    top_movies = movies[movies["movie_id"].isin(candidate_movies.iloc[0:n_top].index)]

    return top_movies  # a list of the n_top movies as recommended


popular_recommendations(1, 10)


def popular_recommendations_filtered(user_id, n_top, years=None, genres=None):
    """
    INPUT:
    user_id - the user_id of the individual you are making recommendations for
    n_top - an integer of the number recommendations you want back
    years - filter by year
    genres - filter by genre
    OUTPUT:
    top_movies - a list of the n_top recommended movies by movie title in order best to worst
    """
    fltrd_movies = movies

    if years is not None:
        fltrd_movies = movies[movies["date"].astype(np.str).isin(years)]

    if genres is not None:
        fltrd_movies = movies[movies["genre"].isin(genres)]

    fltrd_movie_groups = reviews[reviews["movie_id"].isin(fltrd_movies["movie_id"])].groupby("movie_id")
    fltrd_movie_stats = pd.DataFrame(index=fltrd_movie_groups.indices)
    fltrd_movie_stats["rating_avg"] = fltrd_movie_groups["rating"].mean()
    fltrd_movie_stats["rating_count"] = fltrd_movie_groups["rating"].count()
    fltrd_movie_stats["last_rating_time"] = fltrd_movie_groups["timestamp"].max()

    # Do not consider movies with less than 5 ratings
    fltrd_candidate_movies = fltrd_movie_stats[fltrd_movie_stats["rating_count"] > 4].copy()

    fltrd_candidate_movies.sort_values(by=["rating_avg", "rating_count", "last_rating_time"],
                                       ascending=False, inplace=True)

    top_movies = fltrd_movies[fltrd_movies["movie_id"].isin(fltrd_candidate_movies.iloc[0:n_top].index)]

    return top_movies


popular_recommendations_filtered('1', 20, years=['2015', '2016', '2017', '2018'], genres=['History'])

res = popular_recommendations_filtered('1', 20)
