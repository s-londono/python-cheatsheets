import math
from random import random
import numpy as np

str_1 = "The quick red fox"
clt_1 = [i for i in range(0, 10)]
lst_words_1 = ["The", "sands", "of", "time", "have", "run", "out"]
lst_dicts_1 = [{"id": 5, "name": "A"}, {"id": 2, "name": "B"}, {"id": 31, "name": "C"}, {"id": 7, "name": "D"}]

# Reverse a string or collection
print(str_1[::-1])
print(clt_1[::-1])

# Get the unicode point for a character
[print(ord(c), end="\t") for c in str_1]

# Join a list of words into a string separated by a specific character or string
"|-|".join(lst_words_1)

# List comprehensions with conditional
[math.pow(i, 2) for i in range(0, 10) if (i % 2 == 0)]

# Sort list of dictionaries/objects by a specific attribute
print(
    sorted(lst_dicts_1, key=lambda x: x["id"]))

# Use map to apply function receiving n parameters to the elements of n iterables
print(
    [r for r in map(lambda x, y, z: x * y + z, [1, 2, 3], [4, 5, 6], [7, 8, 9])])

# If-elif-else one-liner
r = random()
print(
    str(r) + " is " + ("Tiny" if r < 0.2 else "Small" if r < 0.5 else "Big" if r < 0.75 else "Huge"))

# Use zip to aggregate iterables into one iterable of tuples
lst_nums_1 = [i for i in range(1, 51)]
lst_sines = [math.sin(x) for x in np.arange(0, 5, 0.1)]
lst_cosns = [math.cos(x) for x in np.arange(0, 5, 0.1)]

print(["{0:2d} {1:.4f} {2:.4f}".format(*a) for a in zip(lst_nums_1, lst_sines, lst_cosns)])
