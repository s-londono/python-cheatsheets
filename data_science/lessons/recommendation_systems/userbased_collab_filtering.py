import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import tests as t
from scipy.sparse import csr_matrix
from IPython.display import HTML

if not os.getcwd().endswith("recommendation_systems"):
    os.chdir("data_science/lessons/recommendation_systems")

# Read in the datasets
movies = pd.read_csv('data/movies_clean.csv')
reviews = pd.read_csv('data/reviews_clean.csv')

del movies['Unnamed: 0']
del reviews['Unnamed: 0']

# 1. CREATE A USER-ITEM MATRIX

user_items = reviews[['user_id', 'movie_id', 'rating']]
user_items.head()

# 1.1 Create a matrix where the users are the rows, the movies are the columns, and the ratings exist in each cell,
# or a NaN exists in cells where a user hasn't rated a particular movie. In case of memory error, refer to:
# https://stackoverflow.com/questions/39648991/pandas-dataframe-pivot-memory-error

user_by_movie = user_items.groupby(["user_id", "movie_id"])["rating"].max().unstack()


# 1.2 Use the User-Movie matrix to create a dictionary where the key is each user and the value is an array of
# the movies each user has rated

def movies_watched(user_id):
    """
    INPUT:
    user_id - the user_id of an individual as int
    OUTPUT:
    movies - an array of movies the user has watched
    """
    indic_movies_rated = user_by_movie.loc[user_id, :].notna()
    return user_by_movie.loc[user_id, indic_movies_rated].index.to_list()


def create_user_movie_dict():
    """
    INPUT: None
    OUTPUT: movies_seen - a dictionary where each key is a user_id and the value is an array of movie_ids

    Creates the movies_seen dictionary
    """
    rated_movies_by_user = {}

    for user_id in user_by_movie.index:
        rated_movies_by_user[user_id] = movies_watched(user_id)

    return rated_movies_by_user


# Use your function to return dictionary
movies_seen = create_user_movie_dict()

# 1.3 If a user hasn't rated more than 2 movies, we consider these users "too new". Create a new dictionary
# that only contains users who have rated more than 2 movies. This dictionary will be used for all the final
# steps of this workbook


def create_movies_to_analyze(movies_seen, lower_bound=2):
    """
    Remove individuals who have watched 2 or fewer movies - don't have enough data to make recs
    INPUT:
    movies_seen - a dictionary where each key is a user_id and the value is an array of movie_ids
    lower_bound - (an int) a user must have more movies seen than this bound to be added to the result

    OUTPUT:
    movies_to_analyze - a dictionary where each key is a user_id and the value is an array of movie_ids
    """
    return {user_id: movie_ids for (user_id, movie_ids) in movies_seen.items() if len(movie_ids) > lower_bound}


# Use your function to return your updated dictionary
movies_to_analyze = create_movies_to_analyze(movies_seen)

# 2. CALCULATE USER SIMILARITIES
# To prevent memory issues, rather than creating a dataframe with all possible pairings of users in our data,
# look at a few specific examples of the Correlation between ratings given by two users

# 2.1 Using the movies_to_analyze dictionary and user_by_movie dataframe, create a function that computes the
# correlation between the ratings of similar movies for two users


def compute_correlation(user1, user2):
    """
    INPUT
    user1 - int user_id
    user2 - int user_id
    OUTPUT
    the correlation between the matching ratings between the two users
    """
    # Find the movies rated by both users
    movies_rated_user_1 = set(movies_to_analyze[user1])
    movies_rated_user_2 = set(movies_to_analyze[user2])
    movies_rated_both = [rating for rating in movies_rated_user_1.intersection(movies_rated_user_2)]

    # If not enough ratings of the same movies deem users as not correlated at all
    if len(movies_rated_both) < 1:
        return 0.0

    # Build the vectors of movie ratings for each user, made up of the ratings each user gave to the movies both rated
    df_ratings = pd.DataFrame({"user1": user_by_movie.loc[user1, movies_rated_both].tolist(),
                               "user2": user_by_movie.loc[user2, movies_rated_both].tolist()})

    # Compute the Correlation between the ratings vectors. Note that Pandas computes a Correlation Matrix
    corr_matrix = df_ratings.corr(method="pearson")
    return corr_matrix.iloc[0, 1]


# Note that this results in NaN because ratings for user_1 have Std. Deviation 0!
compute_correlation(2, 104)


# The aforesaid occurs for many users, thus making the correlation coefficient less than optimal for relating
# user ratings to one another, we could instead calculate the euclidean distance between the ratings
# For that reason, could instead calculate the euclidean distance between the ratings

def compute_euclidean_dist(user1, user2):
    """
    INPUT
    user1 - int user_id
    user2 - int user_id
    OUTPUT
    the euclidean distance between user1 and user2
    """
    # Find the movies rated by both users
    movies_rated_user_1 = set(movies_to_analyze[user1])
    movies_rated_user_2 = set(movies_to_analyze[user2])
    movies_rated_both = [rating for rating in movies_rated_user_1.intersection(movies_rated_user_2)]

    # If not enough ratings of the same movies deem users as not correlated at all
    if len(movies_rated_both) < 1:
        return 0.0

    # Build the vectors of movie ratings for each user, made up of the ratings each user gave to the movies both rated
    ratings_vector1 = np.array(user_by_movie.loc[user1, movies_rated_both].tolist())
    ratings_vector2 = np.array(user_by_movie.loc[user2, movies_rated_both].tolist())

    return np.linalg.norm(ratings_vector1 - ratings_vector2)


compute_euclidean_dist(2, 417)

# 3. USE THE NEAREST NEIGHBORS TO MAKE RECOMMENDATIONS

# Read in solution euclidean distances
df_dists = pd.read_pickle("data/dists.p")

# DataFrame df_dists measures the Euclidean Distance between each user and every other user.
# Use df_dists to find the users that are 'nearest' each user. Then find the movies the closest neighbors have
# liked, to recommend to each user

def find_closest_neighbors(user):
    """
    INPUT:
        user - (int) the user_id of the individual you want to find the closest users
    OUTPUT:
        closest_neighbors - an array of the id's of the users sorted from closest to farthest away
    """
    # I treated ties as arbitrary and just kept whichever was easiest to keep using the head method
    # You might choose to do something less hand wavy - order the neighbors

    return closest_neighbors


def movies_liked(user_id, min_rating=7):
    """
    INPUT:
    user_id - the user_id of an individual as int
    min_rating - the minimum rating considered while still a movie is still a "like" and not a "dislike"
    OUTPUT:
    movies_liked - an array of movies the user has watched and liked
    """

    return movies_liked


def movie_names(movie_ids):
    """
    INPUT
    movie_ids - a list of movie_ids
    OUTPUT
    movies - a list of movie names associated with the movie_ids

    """

    return movie_lst


def make_recommendations(user, num_recs=10):
    """
    INPUT:
        user - (int) a user_id of the individual you want to make recommendations for
        num_recs - (int) number of movies to return
    OUTPUT:
        recommendations - a list of movies - if there are "num_recs" recommendations return this many
                          otherwise return the total number of recommendations available for the "user"
                          which may just be an empty list
    """

    return recommendations


def all_recommendations(num_recs=10):
    """
    INPUT
        num_recs (int) the (max) number of recommendations for each user
    OUTPUT
        all_recs - a dictionary where each key is a user_id and the value is an array of recommended movie titles
    """

    # Make the recommendations for each user

    return all_recs


all_recs = all_recommendations(10)



