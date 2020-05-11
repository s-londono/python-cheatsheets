import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import pickle

if not os.getcwd().endswith("recommendation_systems"):
    os.chdir("data_science/lessons/recommendation_systems")

# MATRIX FACTORIZATION - COLLABORATIVE FILTERING WHERE POSSIBLE

# Information is available by running the code cell:
# 1. reviews - a dataframe of reviews
# 2. movies - a dataframe of movies
# 3. create_train_test - a function for creating the training and validation datasets
# 4. predict_rating - a function that takes a user and movie and gives a prediction using FunkSVD
# 5. train_df and val_df - the training and test datasets used in the previous notebook
# 6. user_mat and movie_mat - the u and v matrices from FunkSVD
# 7. train_data_df - a user-movie matrix with ratings where available. FunkSVD was performed on this matrix

# Read in the datasets
movies = pd.read_csv('data/movies_clean.csv')
reviews = pd.read_csv('data/reviews_clean.csv')

del movies['Unnamed: 0']
del reviews['Unnamed: 0']


def create_train_test(reviews, order_by, training_size, testing_size):
    """
    INPUT:
    reviews - (pandas df) dataframe to split into train and test
    order_by - (string) column name to sort by
    training_size - (int) number of rows in training set
    testing_size - (int) number of columns in the test set

    OUTPUT:
    training_df -  (pandas df) dataframe of the training set
    validation_df - (pandas df) dataframe of the test set
    """
    reviews_new = reviews.sort_values(order_by)
    training_df = reviews_new.head(training_size)
    validation_df = reviews_new.iloc[training_size:training_size + testing_size]

    return training_df, validation_df


def predict_rating(user_matrix, movie_matrix, user_id, movie_id):
    """
    INPUT:
    user_matrix - user by latent factor matrix
    movie_matrix - latent factor by movie matrix
    user_id - the user_id from the reviews df
    movie_id - the movie_id according the movies df

    OUTPUT:
    pred - the predicted rating for user_id-movie_id according to FunkSVD
    """
    # Create series of users and movies in the right order
    user_ids_series = np.array(train_data_df.index)
    movie_ids_series = np.array(train_data_df.columns)

    # User row and Movie Column
    user_row = np.where(user_ids_series == user_id)[0][0]
    movie_col = np.where(movie_ids_series == movie_id)[0][0]

    # Take dot product of that row and column in U and V to make prediction
    pred = np.dot(user_matrix[user_row, :], movie_matrix[:, movie_col])

    return pred


# Use our function to create training and test datasets
train_df, val_df = create_train_test(reviews, 'date', 8000, 2000)

# Create user-by-item matrix - this will keep track of order of users and movies in u and v
train_user_item = train_df[['user_id', 'movie_id', 'rating', 'timestamp']]
train_data_df = train_user_item.groupby(['user_id', 'movie_id'])['rating'].max().unstack()
train_data_np = np.array(train_data_df)

# Read in user and movie matrices
user_file = open("data/user_matrix", 'rb')
user_mat = pickle.load(user_file)
user_file.close()

movie_file = open("data/movie_matrix", 'rb')
movie_mat = pickle.load(movie_file)
movie_file.close()


# VALIDATING PREDICTIONS

# Unfortunately, SVD was not able to make predictions on every user-movie combination in the test set,
# as some of these users or movies were new
# However, can validate predictions for the user-movie pairs that do exist in the user_mat and movie_mat matrices

# See how far off we were on average across all of the predicted ratings

def validation_comparison(val_df, user_mat=user_mat, movie_mat=movie_mat):
    """
    INPUT:
    val_df - the validation dataset created in the third cell above
    user_mat - U matrix in FunkSVD
    movie_mat - V matrix in FunkSVD

    OUTPUT:
    rmse - RMSE of how far off each value is from it's predicted value
    perc_rated - percent of predictions out of all possible that could be rated
    actual_v_pred - a 10 x 10 grid with counts for actual vs predicted values
    """
    val_users = np.array(val_df["user_id"])
    val_movies = np.array(val_df["movie_id"])
    val_ratings = np.array(val_df["rating"])

    sse = 0
    num_rated = 0
    preds, acts = [], []
    actual_v_pred = np.zeros((10, 10))  # Will be used to create a Heat Map of how much did predictions match ratings

    for idx in range(val_df.shape[0]):
        try:
            pred = predict_rating(user_mat, movie_mat, val_users[idx], val_movies[idx])
            sse += (val_ratings[idx] - pred) ** 2
            num_rated += 1
            preds.append(pred)
            acts.append(val_ratings[idx])
            actual_v_pred[11 - int(val_ratings[idx] - 1), int(round(pred) - 1)] += 1

        except IndexError:
            continue

    rmse = np.sqrt(sse / num_rated)
    perc_rated = num_rated / len(val_users)
    return rmse, perc_rated, actual_v_pred, preds, acts


# How well did we do?
rmse, perc_rated, actual_v_pred, preds, acts = validation_comparison(val_df)
print(rmse, perc_rated)

# Render Heat Map
sns.heatmap(actual_v_pred)
plt.xticks(np.arange(10), np.arange(1,11))
plt.yticks(np.arange(10), np.arange(1,11))
plt.xlabel("Predicted Values")
plt.ylabel("Actual Values")
plt.title("Actual vs. Predicted Values")

# Render Histogram
plt.figure(figsize=(8, 8))
plt.hist(acts, normed=True, alpha=.5, label='actual')
plt.hist(preds, normed=True, alpha=.5, label='predicted')
plt.legend(loc=2, prop={'size': 15})
plt.xlabel('Rating')
plt.title('Predicted vs. Actual Rating')

# From the above, this can be calculated as follows:
print("Number not rated {}".format(int(len(val_df['rating'])*(1-perc_rated))))
print("Number rated {}.".format(int(len(val_df['rating'])*perc_rated)))

# CONTENT BASED FOR NEW MOVIES

# If all of the above went well, you will notice we still have work to do! We need to bring in a few things we picked
# up from the last lesson to use for those new users and movies. Below is the code used to make the content based
# recommendations, which found movies that were similar to one another.
# The function find_similar_movies will provide similar movies to any movie based only on content

# Subset, so movie_content is only using the dummy variables for each genre and the 3 century based year dummy columns
movie_content = np.array(movies.iloc[:, 4:])

# Take the dot product to obtain a movie x movie matrix of similarities
dot_prod_movies = movie_content.dot(np.transpose(movie_content))


def find_similar_movies(movie_id):
    """
    INPUT
    movie_id - a movie_id
    OUTPUT
    similar_movies - an array of the most similar movies by title
    """
    # Find the row of each movie id
    movie_idx = np.where(movies['movie_id'] == movie_id)[0][0]

    # Find the most similar movie indices - to start I said they need to be the same for all content
    similar_idxs = np.where(dot_prod_movies[movie_idx] == np.max(dot_prod_movies[movie_idx]))[0]

    # Pull the movie titles based on the indices
    similar_movies = np.array(movies.iloc[similar_idxs,]['movie'])

    return similar_movies


def get_movie_names(movie_ids):
    """
    INPUT
    movie_ids - a list of movie_ids
    OUTPUT
    movies - a list of movie names associated with the movie_ids
    """
    movie_lst = list(movies[movies['movie_id'].isin(movie_ids)]['movie'])

    return movie_lst


# RANK BASED FOR NEW USERS

# From the above, we have a way to make recommendations for movie-user pairs that have ratings in any
# part of our user-movie matrix. We also have a way to make ratings for movies that have never received a rating
# using movie similarities. In this last part here, we need a way to make recommendations to new users

# Following are the rank based functions

def create_ranked_df(movies, reviews):
    """
    INPUT
    movies - the movies dataframe
    reviews - the reviews dataframe

    OUTPUT
    ranked_movies - a dataframe with movies that are sorted by highest avg rating, more reviews,
                    then time, and must have more than 4 ratings
    """
    # Pull the average ratings and number of ratings for each movie
    movie_ratings = reviews.groupby('movie_id')['rating']
    avg_ratings = movie_ratings.mean()
    num_ratings = movie_ratings.count()
    last_rating = pd.DataFrame(reviews.groupby('movie_id').max()['date'])
    last_rating.columns = ['last_rating']

    # Add Dates
    rating_count_df = pd.DataFrame({'avg_rating': avg_ratings, 'num_ratings': num_ratings})
    rating_count_df = rating_count_df.join(last_rating)

    # Merge with the movies dataset
    movie_recs = movies.set_index('movie_id').join(rating_count_df)

    # Sort by top avg rating and number of ratings
    ranked_movies = movie_recs.sort_values(['avg_rating', 'num_ratings', 'last_rating'], ascending=False)

    # For edge cases - subset the movie list to those with only 5 or more reviews
    ranked_movies = ranked_movies[ranked_movies['num_ratings'] > 4]

    return ranked_movies


def popular_recommendations(user_id, n_top, ranked_movies):
    """
    INPUT:
    user_id - the user_id (str) of the individual you are making recommendations for
    n_top - an integer of the number recommendations you want back
    ranked_movies - a pandas dataframe of the already ranked movies based on avg rating, count, and time

    OUTPUT:
    top_movies - a list of the n_top recommended movies by movie title in order best to worst
    """

    top_movies = list(ranked_movies['movie'][:n_top])

    return top_movies


# The above set up everything we need to use to make predictions. The next function uses the above information
# as necessary to provide recommendations for every user in the val_df dataframe. There isn't one right way to do this,
# but using a blend between the three could be your best bet

def make_recommendations(_id, _id_type='movie', train_data=train_data_df,
                         train_df=train_df, movies=movies, rec_num=5, user_mat=user_mat, movie_mat=movie_mat):
    """
    INPUT:
    _id - either a user or movie id (int)
    _id_type - "movie" or "user" (str)
    train_data - dataframe of data as user-movie matrix
    train_df - dataframe of training data reviews
    movies - movies df
    rec_num - number of recommendations to return (int)
    user_mat - the U matrix of matrix factorization
    movie_mat - the V matrix of matrix factorization

    OUTPUT:
    rec_ids - (array) a list or numpy array of recommended movies by id
    rec_names - (array) a list or numpy array of recommended movies by name
    """
    val_users = train_data.index
    rec_ids = create_ranked_df(movies, train_df)

    # Use an appropriate recommendation technique depending on the type of entities we are asked to recommend
    if _id_type == 'user':
        # Find the index of this user
        idx = np.where(val_users == _id)[0][0]

        # Get the predicted rating given by this user for all movies
        preds = np.dot(user_mat[idx], movie_mat)

        # Grab the highest predicted ratings and set them as result
        indices = preds.argsort()[-rec_num:][::-1]
        rec_ids = train_data_df.columns[indices]
        rec_names = get_movie_names(rec_ids)

    elif _id_type == 'movie':
        rec_ids = find_similar_movies(_id)
        rec_names = get_movie_names(rec_ids)

    return rec_ids, rec_names

