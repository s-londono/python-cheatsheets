import os
import numpy as np
import pandas as pd

if not os.getcwd().endswith("recommendation_systems"):
    os.chdir("data_science/lessons/recommendation_systems")

# Read in the datasets
movies = pd.read_csv('data/movies_clean.csv')
reviews = pd.read_csv('data/reviews_clean.csv')

del movies['Unnamed: 0']
del reviews['Unnamed: 0']


def create_train_test(reviews, order_by, training_size, testing_size):
    """
    Using the reviews dataframe, create a training and validation set of data to test the performance of the SVD
    algorithm using off-line validation techniques
    INPUT:
    reviews - (pandas df) dataframe to split into train and test
    order_by - (string) column name to sort by
    training_size - (int) number of rows in training set
    testing_size - (int) number of columns in the test set

    OUTPUT:
    training_df -  (pandas df) dataframe of the training set
    validation_df - (pandas df) dataframe of the test set
    """
    # Order the reviews dataframe from earliest to most recent
    reviews_sorted = reviews.sort_values(by=order_by)

    # Make the first 8000/10000 reviews the training data
    training_df = reviews_sorted.head(training_size)

    # Make the last 2000/10000 the test data
    validation_df = reviews_sorted.iloc[training_size:(training_size + testing_size)]

    # Return the training and test datasets
    return training_df, validation_df


# Use our function to create training and test datasets
train_df, val_df = create_train_test(reviews, 'date', 8000, 2000)

# In the real world, we might have all of the data up to this final date in the training data.
# Then we want to see how well we are doing for each of the new ratings, which show up in the test data


# 2. Fit the function to the training data with the following hyperparameters: 15 latent features, a learning rate
# of 0.005, and 250 iterations. This will take some time to run, so you may choose fewer latent features,
# a higher learning rate, or fewer iteratios if you want to speed up the process

def FunkSVD(ratings_mat, latent_features=12, learning_rate=0.0001, iters=100):
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

    # initialize the user and movie matrices with random values
    user_mat = np.random.rand(n_users, latent_features)
    movie_mat = np.random.rand(latent_features, n_movies)

    # initialize sse at 0 for first iteration
    sse_accum = 0

    # keep track of iteration and MSE
    print("Optimizaiton Statistics")
    print("Iterations | Mean Squared Error ")

    # for each iteration
    for iteration in range(iters):

        # update our sse
        old_sse = sse_accum
        sse_accum = 0

        # For each user-movie pair
        for i in range(n_users):
            for j in range(n_movies):

                # if the rating exists
                if ratings_mat[i, j] > 0:

                    # compute the error as the actual minus the dot product of the user and movie latent features
                    diff = ratings_mat[i, j] - np.dot(user_mat[i, :], movie_mat[:, j])

                    # Keep track of the sum of squared errors for the matrix
                    sse_accum += diff ** 2

                    # update the values in each matrix in the direction of the gradient
                    for k in range(latent_features):
                        user_mat[i, k] += learning_rate * (2 * diff * movie_mat[k, j])
                        movie_mat[k, j] += learning_rate * (2 * diff * user_mat[i, k])

        # print results
        print("%d \t\t %f" % (iteration + 1, sse_accum / num_ratings))

    return user_mat, movie_mat


# Create user-by-item matrix - nothing to do here
train_user_item = train_df[['user_id', 'movie_id', 'rating', 'timestamp']]
train_data_df = train_user_item.groupby(['user_id', 'movie_id'])['rating'].max().unstack()
train_data_np = np.array(train_data_df)

# Fit FunkSVD with the specified hyper parameters to the training data
user_mat, movie_mat = FunkSVD(train_data_np, latent_features=15, learning_rate=0.005, iters=250)


# Now that you have created the user_mat and movie_mat, we can use this to make predictions for how users would
# rate movies, by just computing the dot product of the row associated with a user and the column associated
# with the movie

# 3. Implement the predict_rating function.

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
    # Use the training data to create a series of users and movies that matches the ordering in training data
    user_series = {user_id: i for i, user_id in enumerate(train_data_df.index)}
    movie_series = {movie_id: i for i, movie_id in enumerate(train_data_df.columns)}

    user_ix = user_series[user_id]
    movie_ix = movie_series[movie_id]

    # User row and Movie Column
    user_row = user_matrix[user_ix, :]
    movie_column = movie_matrix[:, movie_ix]

    # Take dot product of that row and column in U and V to make prediction
    pred = np.dot(user_row, movie_column)

    return pred


# Test your function with the first user-movie in the user-movie matrix (notice this is a nan)
pred_val = predict_rating(user_mat, movie_mat, 8, 2844)


# Get a little phrase back about the user, movie, and rating
def print_prediction_summary(user_id, movie_id, prediction):
    """
    INPUT:
    user_id - the user_id from the reviews df
    movie_id - the movie_id according the movies df
    prediction - the predicted rating for user_id-movie_id

    OUTPUT:
    None - prints a statement about the user, movie, and prediction made
    """
    print(f"Predicted rating of user: {user_id} for movie: {movie_id} is: {prediction}")


# Test your function the the results of the previous function
print_prediction_summary(8, 2844, pred_val)


# Now that we have the ability to make predictions, let's see how well our predictions do on the test ratings we
# already have. This will give an indication of how well we have captured the latent features, and our ability
# to use the latent features to make predictions in the future!

# 5. For each of the user-movie rating in the val_df dataset, compare the actual rating given to the prediction
# you would make. How do your predictions do? Do you run into any problems? If yes, what is the problem?
# Use the document strings and comments below to assist as you work through these questions

def validation_comparison(val_df, num_preds):
    """
    INPUT:
    val_df - the validation dataset created in the third cell above
    num_preds - (int) the number of rows (going in order) you would like to make predictions for

    OUTPUT:
    Nothing returned - print a statement about the prediciton made for each row of val_df from row 0 to num_preds
    """
    made_preds = 0

    for ix, row in val_df.iterrows():
        cur_user_id = row.iloc[0]
        cur_movie_id = row.iloc[1]
        real_val = row.iloc[2]

        pred_val = predict_rating(user_mat, movie_mat, cur_user_id, cur_movie_id)

        print(f"Predicted: {pred_val} vs. Actual: {real_val}. Diff: {real_val - pred_val}")

        made_preds += 1

        if made_preds >= num_preds:
            break


# Perform the predicted vs. actual for the first 6 rows. How does it look?
validation_comparison(val_df, 6)

# Perform the predicted vs. actual for the first 7 rows. What happened?
validation_comparison(val_df, 7)
