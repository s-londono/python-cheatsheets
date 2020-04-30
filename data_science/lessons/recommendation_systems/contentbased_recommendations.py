import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from collections import defaultdict
from IPython.display import HTML
import tests as t
import progressbar
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


# 4. Build recommendations:
# For the movies seen by each user, in descending ranking order, do:
# i. For each movie, find the movies that are most similar that the user hasn't seen
# ii. Continue through the available, rated movies until 10 recommendations or until there are no additional movies.
#     Adjust the criteria for 'most similar' aiming at obtaining 10 recommendations

# You made this function in an earlier notebook - using again here
def get_movie_names(movie_ids):
    """
    INPUT
    movie_ids - a list of movie_ids
    OUTPUT
    movies - a list of movie names associated with the movie_ids
    """
    movie_lst = list(movies[movies['movie_id'].isin(movie_ids)]['movie'])

    return movie_lst


def find_similar_movies(movie_id, required_similarity):
    """
    INPUT
    movie_id - a movie_id
    required_similarity -
    OUTPUT
    similar_movies - an array of the most similar movies by title
    """
    # find the row of each movie id
    similar_movies = movie_similarities[movie_id].drop(movie_id)

    # find the most similar movie indices - to start I said they need to be the same for all content
    most_similar_movies = similar_movies[similar_movies == required_similarity]

    # pull the movie titles based on the indices
    similar_movies = get_movie_names(most_similar_movies.index)

    return similar_movies


def make_recs():
    """
    INPUT
    None
    OUTPUT
    recs - a dictionary with keys of the user and values of the recommendations
    """
    target_num_recomms = 10
    # Minimum rating that tells liked movies from disliked movies
    liked_movie_thres = 5
    # A movie has to be at least this similar to a movie ranked by the user, in order to be recommended
    min_required_similarity = 4

    # Create dictionary to return with users and ratings
    recs = {}

    user_review_groups = user_ranked_reviews.groupby(by="user_id")

    # How many users for progress bar
    total_users = len(user_review_groups.groups)

    # Create the progressbar
    prgrss_bar = progressbar.ProgressBar(maxval=total_users)
    prgrss_bar.start()

    # Maximum similarity between two movies. The max. value is always in the diagonal, take advantage of that
    max_similarity = movie_similarities.values.diagonal().max()

    # For each user
    for user_ix, (user_id, ranked_movies) in enumerate(user_review_groups):
        # Update the progress bar
        prgrss_bar.update(user_ix)

        cur_user_recomms = set()
        recs[user_id] = cur_user_recomms

        required_similarity = max_similarity

        # Adjust required similarity level as movies are iterated through
        while required_similarity >= min_required_similarity and len(cur_user_recomms) < target_num_recomms:
            # Set of the IDs of the movies ranked by the user
            set_movie_titles_seen = set(ranked_movies["movie_id"].tolist())
            liked_movie_ids = ranked_movies[ranked_movies["rating"] > liked_movie_thres]["movie_id"].tolist()

            # Look at each of the movies (highest ranked first),
            for ranked_movie_id in liked_movie_ids:
                # Pull the movies the user hasn't seen that are most similar to the current movie ranked by the user.
                # These will be the recommendations - continue until 10 recs or the movie list or the user is depleted
                similar_movie_titles = find_similar_movies(ranked_movie_id, required_similarity)

                for similar_movie_title in similar_movie_titles:
                    # Add all movies similar to the current movie liked by the user, if not seen before
                    if len(cur_user_recomms) < target_num_recomms and similar_movie_title not in set_movie_titles_seen:
                        cur_user_recomms.add(similar_movie_title)

                if len(cur_user_recomms) < target_num_recomms:
                    break

            # We depleted all movies ranked by the user
            required_similarity -= 1

    # finish the progress bar
    prgrss_bar.finish()

    return recs


recs = make_recs()

num_recs = np.array([len(user_recs) for user_recs in recs.values()])
print(f"Total users: {len(num_recs)}. Mean recommendations per user: {num_recs.mean()}. Max: {num_recs.max()}")

# Some characteristics of my content based recommendations
users_without_all_recs = [user_id for user_id, recs in recs.items() if len(recs) < 10]
users_with_all_recs = [user_id for user_id, recs in recs.items() if len(recs) == 10]
no_recs = [user_id for user_id, recs in recs.items() if len(recs) == 0]

print(f"There were {len(users_without_all_recs)} users without all 10 recommendations we would have liked to have.")
print(f"There were {len(users_with_all_recs)} users with all 10 recommendations we would like them to have.")
print(f"There were {len(no_recs)} users with no recommendations at all!")

# Closer look at individual user characteristics - this may help it was from an earlier notebook
user_items = reviews[['user_id', 'movie_id', 'rating']]
user_by_movie = user_items.groupby(['user_id', 'movie_id'])['rating'].max().unstack()


def movies_watched(user_id):
    """
    INPUT:
    user_id - the user_id of an individual as int
    OUTPUT:
    movies - an array of movies the user has watched
    """
    movies = user_by_movie.loc[user_id][user_by_movie.loc[user_id].isnull() == False].index.values

    return movies


movies_watched(189)
