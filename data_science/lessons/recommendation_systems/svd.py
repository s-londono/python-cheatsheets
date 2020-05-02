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

# Looking at the dimensions of the three returned objects, we can see the following:
#  1. The u matrix is a square matrix with the number of rows and columns equaling the number of users.
#  2. The v transpose matrix is also a square matrix with the number of rows and columns equaling the number of items.
#  3. The sigma matrix is actually returned as just an array with 4 values, but should be a diagonal matrix.
#
#  In order to set up the matrices in a way that they can be multiplied together, we have a few steps to perform:
#  1. Turn sigma into a square matrix with the number of latent features we would like to keep.
#  2. Change the columns of u and the rows of v transpose to match this number of dimensions.
#  If we would like to exactly re-create the user-movie matrix, we could choose to keep all of the latent features.

# 3. Use the thoughts from the above question to create u, s, and vt with four latent features
u_new = u[:, 0:4]
s_new = np.diag(s)

# Because we are using 4 latent features and there are only 4 movies, vt and vt_new are the same
vt_new = vt

print(f"Dot products equal original matrix A? {np.allclose(np.dot(np.dot(u_new, s_new), vt_new), user_movie_subset)}")

# It turns out that the sigma matrix can actually tell us how much of the original variability in the user-movie
# matrix is captured by each latent feature. The total amount of variability to be explained is the sum of the squared
# diagonal elements. The amount of variability explained by the first component is the square of the first value in
# the diagonal. The amount of variability explained by the second component is the square of
# the second value in the diagonal

# 6. Using the above information, can you determine the amount of variability in the original user-movie matrix
# that can be explained by only using the first two components? Use the cell below for your work, and then test your
# answer against the solution with the following cell

total_var = (s ** 2).sum()
var_exp_comp1_and_comp2 = (s[0:2] ** 2).sum()
perc_exp = (var_exp_comp1_and_comp2 / total_var) * 100.0

print(f"The total variance in the original matrix is {total_var}.")
print(f"The percentage of variability captured by the first two components is {perc_exp}%.")

# 7. Now change the shapes of your u, sigma, and v transpose matrices. However, this time consider only using the
# first 2 components to reproduce the user-movie matrix instead of all 4
u_2 = u[:, 0:2]
s_2 = np.diag(s[0:2])
vt_2 = vt[0:2, :]

# 8. When using all 4 latent features, we saw that we could exactly reproduce the user-movie matrix. Now that we only
# have 2 latent features, we might measure how well we are able to reproduce the original matrix by looking at the
# sum of squared errors from each rating produced by taking the dot product as compared to the actual rating.
# Find the sum of squared error based on only the two latent features

# Compute the dot product
pred_ratings = np.dot(np.dot(u_2, s_2), vt_2)

# Compute the squared error for each predicted vs. actual rating
sum_square_errs = ((user_movie_subset.values - pred_ratings) ** 2).sum(axis=None)

# At this point, you may be thinking... Why would we want to choose a k that doesn't just give us back the full
# user-movie matrix with all the original ratings. This is a good question. One reason might be for computational
# reasons - sure, you may want to reduce the dimensionality of the data you are keeping, but really this isn't
# the main reason we would want to perform reduce k to lesser than the minimum of the number of movies or users.

# Let's take a step back for a second. In this example we just went through, your matrix was very clean. That is,
# for every user-movie combination, we had a rating. There were no missing values. But what we know from the previous
# lesson is that the user-movie matrix is full of missing values

# Therefore, if we keep all k latent features it is likely that latent features with smaller values in the sigma
# matrix will explain variability that is probably due to noise and not signal. Furthermore, if we use these
# "noisey" latent features to assist in re-constructing the original user-movie matrix it will potentially (and likely)
# lead to worse ratings than if we only have latent features associated with signal

# 9. Let's try introducing just a little of the real world into this example by performing SVD on a matrix with
# missing values. Below I have added a new user to our matrix who hasn't rated all four of our movies. Try performing
# SVD on the new matrix. What happens?

# This line adds one nan value as the very first entry in our matrix
user_movie_subset.iloc[0, 0] = np.nan # no changes to this line

# Try svd with this new matrix
u, s, vt = np.linalg.svd(user_movie_subset)
