# Sources:
#   https://chrisalbon.com/python/basics/generating_random_numbers_with_numpy/
#   https://docs.scipy.org/doc/scipy/reference/stats.html

import numpy as np

# Generate random number from the Normal distribution
np.random.normal()

# Generate four random numbers from the Normal/Uniform distributions
np.random.normal(size=4)
np.random.uniform(size=4)

# Generate four random integers from the Discrete Uniform distribution between 1 and 100
np.random.randint(low=1, high=100, size=4)

# Generate ndarrays of random numbers from various distributions
np.random.normal(size=(5, 3))
np.random.uniform(size=(5, 3))
np.random.randint(low=1, high=100, size=(5, 3))
