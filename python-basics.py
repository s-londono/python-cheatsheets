import time
import timeit
import sys
import math
from random import random
import numpy as np

# Check Python version:
print(sys.version)

# Print module paths
print(sys.path)

# Get information about the float representation of the current environment:
float_info = sys.float_info

# Casting. Note that can be used to parse strings into numbers:
bool(int("1"))

# Check type:
tuple_1 = (1, 2, 3)
type(tuple_1)

# Integer division (Python 3. In this version regular division produces float):
r_div = 4 // 5

# Copy a string n times:
n = 5
str_mult = n * "The string"

# Escape a full string:
esc_str = r"A string with \ "

# Make a NEW tuple from slice of a tuple
t3 = 1, 2, 3, 4, 5, 6, 7
t4 = t3[2:4]
t5 = t3[:3]

# Create new tuple by combining two tuples
t7 = t3 + t5

# Find index of first occurrence of element in tuple
print(t7.index(2))

# Count occurrences of element in tuple
print(t7.count(2))

# Tuple unpacking
a, b, c = t5
print("Val a: {}, val b: {}, val c: {}".format(*t5))

lt = [(1, 2), (3, 4), (5, 6)]

# F strings (templates) and tuple unpacking in loop
for a, b in lt:
    print(f"A is: {a} and B is: {b}")

# Tuples are faster than lists
print(timeit.timeit('x=(1,2,3,4,5,6,7,8,9,10,11,12)', number=1000000))
print(timeit.timeit('x=[1,2,3,4,5,6,7,8,9,10,11,12]', number=1000000))

# Tuples and lists may contain mixed types
tuple_mix = (1, "a", True, ("x", 2))
lst_mix = [1, 2, "abc", [True, 'a', 1.22]]

l1 = ["a", "b", 5]
l2 = l1 + [1, 2]

l3 = l2.extend([4, "a", 1.2])  # Append each element in the arguemtn to l2. Does not build a new list
l4 = l1.append([1, 2, 3])  # Adds the argument as a whole to the list
del (l2[1])  # Remove the second element
"a list".split()  # Convert string to a list, space as separator
"a,b,c,d".split(",")
print(1 in l1)  # Check if list contains item

l4 = [*l1, *l2]  # This is the same as l4 = l1 + l2
print(l4)

# Clone a list:
l3 = l2[:]

# Iterable functions (apply to tuples, lists, sets)
l_sort = [10, 9, 8, 4]
sorted(l_sort)  # Returns a new list or tuple
l_sort.sort()  # Does not create a new list

# Sets are a type of collection. Support elements of different data types. Elements are unordered.
# An element can be contained only once.
s1 = {"b", (1, 2), ("a", True)}
sc = {str(i) for i in range(0, 10)}
s2 = set([1, 2, 3, 4, 2, 3, 1])  # Convert a list into a set
s1.add(False)  # Add an element to a set, if not there yet
s1.remove("b")
s1 & s2  # Intersection of s1 and s2
s1.intersection(s2)
su = s1 | s2  # Union of s1 and s2
s1.union(s2)
s1.difference(s2)  # Difference (elements in s1 that are not in s2)
s1.issuperset(s2)
s1.issubset(s2)
print((1, 2) in s1)  # Check if an element is in the set

# Intersection of lists using sets
longer_list = list(range(1, 100))
shorter_list = [30, 10, 22]
list_intersection = set(longer_list).intersection(shorter_list)

# Keys must be immutable and unique (e.g. can be tuples). Values can be mutable and be duplicated.
d1 = {"key1": [1, 2, 3], "key2": s1, "key3": False}
d2 = {i: str(i) for i in range(0, 10)}
d1["key4"] = 5  # Add a new element
del (d1["key2"])  # Delete element with key2
d1.keys()  # Get all keys
d1.values()  # Get all values
print("key3" in d1)  # Check if key is in the dictionary

# Get address of a variable (not 100% reliable)
hex(id(l2))
hex(id(l3))

str_1 = "The quick red fox"
clt_1 = [i for i in range(0, 10)]
lst_words_1 = ["The", "sands", "of", "time", "have", "run", "out"]
lst_dicts_1 = [{"id": 5, "name": "A"}, {"id": 2, "name": "B"}, {"id": 31, "name": "C"}, {"id": 7, "name": "D"}]

# Indexing and slicing
print(str_1[-3])
print(str_1[2:])
print(str_1[:4])
print(str_1[-6:-2])

# Slicing by jumping every two elements
print(str_1[0:8:2])

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

# Basic use of map and filter
d1 = {"a": 1, "b": (3, 5), "c": {1, 2, 3}, 5: "ccc"}
print([t for t in map(lambda i: (i[0], str(i[1])), d1.items())])
print([t for t in filter(lambda i: type(i[1]) == tuple, d1.items())])

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

# Format with arguments
print("Param A: {a}, param B: {b}, param A: {a}".format(a=11, b=22))


# Collect arguments:
def func(*names):
    for nm in names:
        print(nm)


# Declare global variable in function:
def func():
    global g
    g = 4


# Get help about a function:
help(func)

# Get all the methods of an object:
dir(d1)


# Create a class with object as parent (default):
class Rectangle(object):

    def __init__(self, attr1, attrn):
        self.calc1 = None
        self.attr1 = attr1
        self.attrn = attrn

    def method1(self, arg1, argn="defaultvaln"):
        self.calc1 = arg1 ** argn + 10
        return self.calc1


# Efficient concatenation
# https://waymoot.org/home/python_string/
def concat_man6():
    return "".join([f"{num}" for num in range(1, 1000)])


# Calculate runtime

start = time.time()
recent_coding_books = []

for i in range(1, 100):
    pass

print('Duration: {} seconds'.format(time.time() - start))

# Using timeit
print(timeit.timeit('x=(1,2,3,4,5,6,7,8,9,10,11,12)', number=1000000))


# GENERATORS

# Generators process information one at a time. Are useful for data that are too large to fit in RAM
def my_gen(x, degree):
    cur_i = 0
    while cur_i <= degree:
        yield x ** degree
        print(f"Generated degree: {cur_i}")
        cur_i += 1


for p in my_gen(5, 10):
    print(f"Ready...")
    print(f"Got {p}")
