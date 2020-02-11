import numpy as np

gift_costs = np.array(["10", "20", "100", "200"]).astype(int)

# Optimize filtering elements in array using Numpy
total_price = (gift_costs[gift_costs < 25]).sum() * 1.08

# Intersection of sets if elements
longer_list = list(range(1, 100))
shorter_list = [30, 10, 22]

# Fastest: using sets
list_intersection = set(longer_list).intersection(shorter_list)

# Fast: use Numpy function
list_intersection2 = np.intersect1d(shorter_list, longer_list)


# Efficient concatenation
# https://waymoot.org/home/python_string/
def concat_man6():
    return "".join([f"{num}" for num in range(1, 1000)])


