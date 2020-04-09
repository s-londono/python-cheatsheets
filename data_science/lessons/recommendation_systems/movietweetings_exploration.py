import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tests as t

# Read in the datasets
movies = pd.read_csv('https://raw.githubusercontent.com/sidooms/MovieTweetings/master/latest/movies.dat', delimiter='::', header=None, names=['movie_id', 'movie', 'genre'], dtype={'movie_id': object}, engine='python')
reviews = pd.read_csv('https://raw.githubusercontent.com/sidooms/MovieTweetings/master/latest/ratings.dat', delimiter='::', header=None, names=['user_id', 'movie_id', 'rating', 'timestamp'], dtype={'movie_id': object, 'user_id': object, 'timestamp': object}, engine='python')

# 1. TAKE A LOOK AT THE DATA

print(f"Number of movies: {movies.shape[0]}")
print(f"Number of reviews: {reviews.shape[0]}")

# Split Genres
genres = set()


def add_all_genres(str_genres):
    if not pd.isna(str_genres):
        for str_genre in str_genres.split("|"):
            genres.add(str_genre)


movies["genre"].apply(add_all_genres)
num_genres = len(genres)
print(f"Number of unique genres: {num_genres}")

num_users = reviews["user_id"].nunique()
print(f"Number of unique users: {num_users}")

num_missing_ratings = reviews["rating"].isna().sum()
missing_ratings = reviews[reviews["rating"].isna()]
print(f"Number of missing ratings: {num_missing_ratings}")

avg_rating = reviews["rating"].mean()
min_rating = reviews["rating"].min()
max_rating = reviews["rating"].max()

print(f"Average rating {avg_rating}")
print(f"Minimum rating {min_rating}")
print(f"Maximum rating {max_rating}")
print(reviews.describe())

# 2. DATA CLEANING

# Pull the date from the title and create a new column
movies["year"] = movies["movie"].str.extract(r"^.*\(([0-9]+)\).*").astype(np.int16)

# Dummy the century column
movies["century"] = (movies["year"] / 100.0).astype(np.int16)
movies = pd.get_dummies(movies, columns=["century"], prefix=["century"], drop_first=True)

# Dummy the genre column
movie_gens = movies.apply(
    lambda r: ({gname: (not pd.isna(r["genre"]) and r["genre"].find(gname) >= 0) for gname in genres}), axis=1,
    result_type="expand")

# Reviews: create a date out of time stamp
reviews["date"] = pd.to_datetime(reviews["timestamp"], unit="s")
