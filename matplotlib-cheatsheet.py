import numpy as np
import matplotlib.pyplot as plt

a = np.array([1, 2, 3, 4, 5])

print(a.dtype)
print(a)

x = np.arange(-np.pi * 3, np.pi * 3, 0.1)

y = np.sin(x) / 2

plt.plot(x, y)

plt.axis([None, None, -1, 1])
plt.xlabel("x")
plt.xlabel("y")

plt.show()

