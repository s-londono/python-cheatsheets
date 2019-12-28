import numpy as np

# Create 1D array from list
np_a1 = np.array([1, 2, 9, 5, 10, 0])

# Create 2D matrix from list of lists
np_m1 = np.array([[1, 2], [3, 4]])

# Create array from range with step 2
np_a2 = np.arange(0, 100, 2)

# Create array/matrix of zeros
np_a3 = np.zeros(5)
np_m2 = np.zeros((7, 4))

# Same works with ones
np_m3 = np.ones((5, 2))

# Build range specifying the number of points to add between the start and end
np_a4 = np.linspace(0, 100, 50)

# Identity matrix
np_m4 = np.eye(5)

# Array/matrix of random numbers. Uniform, normal
np_m5 = np.random.rand(3, 7)
np_m6 = np.random.randn(5, 2)

# Get a random integer from range. Also an array/matrix of specified dimensions
i_rand = np.random.randint(1, 10)
np_m7 = np.random.randint(0, 50, (5, 7))

# Reshape an array
np_a5 = np.random.randint(0, 100, 50)
np_m8 = np.reshape(np_a5, (10, 5))

# Basic methods
np_m8.max()
np_m7.min(1)     # Finds the minimum along axis 1, scan through columns i.e. the minimum of each row
np_a5.argmax()   # Index of the max value
np_m7.argmax(0)  # Linear index of the max value in the matrix
np_m7.argmin(0)  # Index of the min value in each column (along axis 0)
np_m8.shape
np_a5.dtype

# Indexing
np_a5[3]
np_a5[1:4]
np_a5[:10]
np_a5[20:]
np_a5[:]

# Broadcasting: assign value to a range of elements
np_a5[0:10] = -2

# Warning! broadcasting on a slice modifies the original array!
slice_np_a5 = np_a5[5:10]
slice_np_a5[:] = 0

# Numpy does not create copies by default! must use copy
slice_np_a5 = np_a5[20:25].copy()
slice_np_a5[:] = -9

# Indexing matrices
np_m7[0][1]
np_m7[0, 1]    # Equivalent to previous
np_m7[1]       # Entire first row
np_m7[:2, 1:]  # Fragment of matrix

# Conditional selection
np_a6 = np_a5[np_a5 > 50]

np_m9 = np.arange(50).reshape(5, 10)
print(np_m9[1:3, 3:5])

# Scalar operations
np_a7 = np.zeros((5, 7)) + 5.25
np_a8 = np_a7 ** 2

# Array operations
np_a9 = (np.arange(0, 5) * 2) + np.arange(10, 15)

# Numpy handles errors gracefully, reports as warnings
np_10 = np.arange(0, 5) / np.arange(0, 5)

# Operations. Find in the documentation as Universal Functions
print(np.sqrt(np_a7))
print(np.exp(np_a7))
print(np.max(np_a7))
print(np.sin(np.arange(0.0, 1.0, 0.05)))

# Statistics
np_m5.sum()
np_m5.std()
