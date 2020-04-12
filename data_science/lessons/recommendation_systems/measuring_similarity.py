import numpy as np
import pandas as pd
from scipy.stats import spearmanr, kendalltau
import matplotlib.pyplot as plt
import tests as t
# import helper as h

play_data = pd.DataFrame({'x1': [-3, -2, -1, 0, 1, 2, 3], 'x2': [9, 4, 1, 0, 1, 4, 9], 'x3': [1, 2, 3, 4, 5, 6, 7],
                          'x4': [2, 5, 15, 27, 28, 30, 31]})

# Create play data dataframe
play_data = play_data[['x1', 'x2', 'x3', 'x4']]

# 1. PEARSON'S CORRELATION
# Implemented in Numpy as: np.corrcoef

def pearson_corr(x, y):
    """
    INPUT
    x - an array of matching length to array y
    y - an array of matching length to array x
    OUTPUT
    corr - the pearson correlation coefficient for comparing x and y
    """
    # Check input types
    if type(x) != np.ndarray or type(y) != np.ndarray:
        x = np.array(x)
        y = np.array(y)

    # Compute the means and differences from the mean for x and y
    x_hat = x.mean()
    y_hat = y.mean()

    x_hat_diffs = x - x_hat
    y_hat_diffs = y - y_hat
    root_sum_x_hat_diffs_squared = np.sqrt((x_hat_diffs ** 2).sum())
    root_sum_y_hat_diffs_squared = np.sqrt((y_hat_diffs ** 2).sum())

    return (x_hat_diffs * y_hat_diffs).sum() / (root_sum_x_hat_diffs_squared * root_sum_y_hat_diffs_squared)


# 2. SPEARMAN'S CORRELATION
# Implemented in scikit.stats as spearmanr

# To get the rank of the original values use Panda's rank function
print("The ranked values for the variable x1 are: {}".format(np.array(play_data['x1'].rank())))
print("The raw data values for the variable x1 are: {}".format(np.array(play_data['x1'])))


def corr_spearman(x, y):
    """
    INPUT
    x - an array of matching length to array y
    y - an array of matching length to array x
    OUTPUT
    corr - the spearman correlation coefficient for comparing x and y
    """
    # Convert the vectors into their corresponding rangs
    x_r = x.rank()
    y_r = y.rank()

    return pearson_corr(x_r, y_r)


# 3. KENDALL'S TAU
# Implemented in scikit.stats as kendalltau

def kendalls_tau(x, y):
    """
    INPUT
    x - an array of matching length to array y
    y - an array of matching length to array x
    OUTPUT
    tau - the kendall's tau for comparing x and y
    """
    # Convert the vectors into their corresponding rangs
    x_r = np.array(x.rank().tolist())
    y_r = np.array(y.rank().tolist())

    n = x_r.shape[0]
    sum_concordants = 0

    for i in range(n - 1):
        for j in range(i + 1, n):
            sum_concordants += (np.sign(x_r[i] - x_r[j]) * np.sign(y_r[i] - y_r[j]))

    return (2 * sum_concordants) / (n * (n - 1))


kendalls_tau(play_data['x1'], play_data['x2'])
kendalls_tau(play_data['x1'], play_data['x3'])

kendalltau(play_data['x1'], play_data['x2'])

assert kendalls_tau(play_data['x1'], play_data['x3']) == kendalltau(play_data['x1'], play_data['x3'])[0], 'Oops!  The correlation between the first two columns should be 0, but your function returned {}.'.format(kendalls_tau(play_data['x1'], play_data['x2']))
