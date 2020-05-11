import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy import sparse

if not os.getcwd().endswith("recommendation_systems"):
    os.chdir("data_science/lessons/recommendation_systems")

# Read in the datasets
movies = pd.read_csv('data/movies_clean.csv')
reviews = pd.read_csv('data/reviews_clean.csv')

del movies['Unnamed: 0']
del reviews['Unnamed: 0']

# Create user-by-item matrix
user_items = reviews[['user_id', 'movie_id', 'rating', 'timestamp']]
user_by_movie = user_items.groupby(['user_id', 'movie_id'])['rating'].max().unstack()

# Create data subset
user_movie_subset = user_by_movie[[73486, 75314,  68646, 99685]].dropna(axis=0)
ratings_mat = np.matrix(user_movie_subset)
print(ratings_mat)

# Setting up a matrix of the first 1000 users with movie ratings
first_1000_users = np.matrix(user_by_movie.head(1000).copy())

# Free some memory. These two variables are no longer needed
reviews = None
user_items = None
user_by_movie = None


def FunkSVD(ratings_mat, latent_features=4, learning_rate=0.0001, iters=100):
    """
    This function performs matrix factorization using a basic form of FunkSVD with no regularization

    INPUT:
    ratings_mat - (numpy array) a matrix with users as rows, movies as columns, and ratings as values
    latent_features - (int) the number of latent features used
    learning_rate - (float) the learning rate
    iters - (int) the number of iterations

    OUTPUT:
    user_mat - (numpy array) a user by latent feature matrix
    movie_mat - (numpy array) a latent feature by movie matrix
    """

    # Set up useful values to be used through the rest of the function
    n_users = ratings_mat.shape[0]
    n_movies = ratings_mat.shape[1]
    num_ratings = np.count_nonzero(~np.isnan(ratings_mat))

    # Initialize the user and movie matrices with random values
    # helpful link: https://docs.scipy.org/doc/numpy/reference/generated/numpy.random.rand.html
    user_mat = np.random.rand(n_users, latent_features)
    movie_mat = np.random.rand(latent_features, n_movies)

    # Initialize SSE (Squared Standard Error) at 0 for first iteration
    sse_accum = 0

    # Header for running results
    print("Optimization Statistics")
    print("Iterations | Mean Squared Error ")

    # For each iteration
    for i in range(iters):
        # Update our sse
        old_sse = sse_accum
        sse_accum = 0

        # For each user-movie pair
        for u in range(n_users):

            for m in range(n_movies):
                y = ratings_mat[u, m]

                # If the rating exists
                if y is not None and not np.isnan(y):
                    # Compute the error as the actual minus the dot product of the user and movie latent features
                    err = y - np.dot(user_mat[u, :], movie_mat[:, m])

                    # Keep track of the total sum of squared errors for the matrix
                    sse_accum += (err ** 2)

                    # Update the values in each matrix in the direction of the gradient
                    user_mat[u, :] = user_mat[u, :] + 2 * learning_rate * err * movie_mat[:, m]
                    movie_mat[:, m] = movie_mat[:, m] + 2 * learning_rate * err * user_mat[u, :]

        # Print results for iteration
        print(f"Iteration: {i}. MSE Old: {old_sse}. MSE: {sse_accum/num_ratings}")

    return user_mat, movie_mat


# Try out your function on the user_movie_subset dataset. First try 4 latent features, a learning rate of 0.005, and
# 10 iterations. When you take the dot product of the resulting U and V matrices, how does the resulting user_movie
# matrix compare to the original subset of the data?

user_mat, movie_mat = FunkSVD(ratings_mat, latent_features=4, learning_rate=0.005, iters=10)

#Compare the predicted and actual results
print("Predicted: \n")
print(np.dot(user_mat, movie_mat))
print("Actual: \n")
print(ratings_mat)
print("Difference: \n")
print(np.dot(user_mat, movie_mat) - ratings_mat)

# Let's try out the function again on the user_movie_subset dataset. This time we will again use 4 latent features
# and a learning rate of 0.005. However, let's bump up the number of iterations to 250. When you take the dot product
# of the resulting U and V matrices, how does the resulting user_movie matrix compare to the original subset of the
# data? What do you notice about your error at the end of the 250 iterations?

user_mat, movie_mat = FunkSVD(ratings_mat, latent_features=4, learning_rate=0.005, iters=250)

#Compare the predicted and actual results
print("Predicted: \n")
print(np.dot(user_mat, movie_mat))
print("Actual: \n")
print(ratings_mat)
print("Difference: \n")
print(np.dot(user_mat, movie_mat) - ratings_mat)

# The last time, when we placed an np.nan value into this matrix the entire svd algorithm in python broke. Let's see if
# that is still the case using your FunkSVD function. In the below cell, I have placed a nan into the first cell
# of your numpy array

# Here we are placing a nan into our original subset matrix
ratings_mat[0, 0] = np.nan

# Use 4 latent features, a learning rate of 0.005, and 250 iterations. Are you able to run your SVD without it
# breaking (something that was not true about the python built in)? Do you get a prediction for the nan value?
# What is your prediction for the missing value? Use the cells below to answer these questions

# Run SVD on the matrix with the missing value
user_mat, movie_mat = FunkSVD(ratings_mat, latent_features=4, learning_rate=0.005, iters=250)

# Run this cell to see if you were able to predict for the missing value
preds = np.dot(user_mat, movie_mat)
print("The predicted value for the missing rating is {}:".format(preds[0,0]))
print("The actual value for the missing rating is {}:".format(ratings_mat[0,0]))
assert np.isnan(preds[0,0]) == False

# Now let's extend this to a more realistic example. Unfortunately, running this function on your entire user-movie
# matrix is still not something you likely want to do on your local machine. However, we can see how well this
# example extends to 1000 users. In the above portion, you were using a very small subset of data with
# no missing values

# Given the size of this matrix, this will take quite a bit of time. Consider the following hyperparameters:
# 4 latent features, 0.005 learning rate, and 20 iterations. Grab a snack, take a walk, and this should be done
# running in a bit

# perform funkSVD on the matrix of the top 1000 users
# Setting up a matrix of the first 1000 users with movie ratings
first_1000_users = np.matrix(user_by_movie.head(1000))
user_mat, movie_mat = FunkSVD(first_1000_users, latent_features=4, learning_rate=0.005, iters=20)

# Now that you have a set of predictions for each user-movie pair, let's answer a few questions about your results.
# Provide the correct values for each of the variables below, and check your solutions using the tests below

# Replace each of the comments below with the correct values
num_ratings = np.count_nonzero(~np.isnan(first_1000_users))
print("The number of actual ratings in the first_1000_users is {}.".format(num_ratings))
print()

ratings_for_missing = np.count_nonzero(~np.isnan(np.dot(user_mat, movie_mat))) - num_ratings
print("The number of ratings made for user-movie pairs that didn't have ratings is {}".format(ratings_for_missing))


