import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

if not os.getcwd().endswith("recommendation_systems"):
    os.chdir("data_science/lessons/recommendation_systems")

# Read in the datasets
movies = pd.read_csv('data/movies_clean.csv')
reviews = pd.read_csv('data/reviews_clean.csv')

del movies['Unnamed: 0']
del reviews['Unnamed: 0']

# 1. Create user_movie_subset matrix
user_items = reviews[['user_id', 'movie_id', 'rating']]
user_by_movie = user_items.groupby(['user_id', 'movie_id'])['rating'].max().unstack()

user_movie_subset = user_by_movie[[73486, 75314,  68646, 99685]].dropna(axis=0)

# 2. SVD with Numpy:
# https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html#numpy.linalg.svd

u, s, vt = np.linalg.svd(user_movie_subset)
print(f"S: {s.shape}. U: {u.shape}. V: {vt.shape}")

