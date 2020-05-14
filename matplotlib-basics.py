# REQUIREMENTS:
# conda install matplotlib
# pip install matplotlib

import matplotlib.pyplot as plt
import numpy as np

x = np.linspace(0, 5, 11)
y = x ** 2

# Two ways to use Matplotlib: functional and object-oriented

# 1. FUNCTIONAL METHOD

plt.plot(x, y)
plt.xlabel('X Label')
plt.ylabel('Y Label')
plt.title('Title')
plt.show()

# Multiple plots. Arguments are: number of rows, number of columns, plot number
plt.subplot(1, 2, 1)
plt.plot(x, y, 'r')

# Must call subplot again for each plot added, but inccreasing the plot number
plt.subplot(1, 2, 2)
plt.plot(x, y, 'b')

plt.show()

# 2. OBJECT ORIENTED METHOD

# The object-oriented method is based on a figure object, which acts as a canvas
fig = plt.figure()

# Add axes to the canvas. The argument defines the position and size of the axes as ratios with respect to the canvas:
# [left-pos-wrt-canvas-left, left-pos-wrt-canvas-bottom, width-wrt-canvas, height-wrt-canvas]
axes1 = fig.add_axes([0.10, 0.10, 0.87, 0.85])
axes2 = fig.add_axes([0.20, 0.55, 0.28, 0.30])

# Plot on the axes independently
axes1.plot(x, y, 'b')
axes1.set_xlabel('X Label 1')
axes1.set_ylabel('Y Label 1')
axes1.set_title('Title 1')

axes2.plot(y, x, 'r')
axes2.set_xlabel('X Label 2')
axes2.set_ylabel('Y Label 2')
axes2.set_title('Title 2')

fig.show()

# Subplots in the OO method use similar to plt.figure() except use tuple unpacking to grab fig and axes.
# Act as an "axes manager". Automatically adds axes arranged in rows and columns
# Empty canvas of 1 by 2 subplots
fig, axes = plt.subplots(nrows=1, ncols=2)

fig.subplots_adjust(hspace=.5)

# Now use the axes object to add stuff to plot. Axes is an array. Can be iterated and indexed
axes[0].plot(x, y, 'r')
axes[0].set_xlabel('x')
axes[0].set_ylabel('y')
axes[0].set_title('Title 0')

axes[1].plot(y, x, 'b')
axes[1].set_xlabel('x')
axes[1].set_ylabel('y')
axes[1].set_title('Title 1')

# Take care of any overlapping
# plt.tight_layout()

fig.show()

# FIGURE SIZE AND DPI

# Figure size is a tuple of width x height in inches
fig_2 = plt.figure(figsize=(8, 5), dpi=100)
ax = fig_2.add_axes([0, 0, 1, 1])
ax.plot(x, y)
fig_2.show()

fig_3, axes_2 = plt.subplots(nrows=2, ncols=1, figsize=(8, 5))

for i, cur_ax in enumerate(axes_2):
    cur_ax.plot(x + i, y * i)

fig_3.show()

# LEGEND

# Can add several plots to the same axis
fig_4 = plt.figure()
ax = fig_4.add_axes([0, 0, 1, 1])

# For each plot, use the label argument to name it in the legend
ax.plot(x, x * 2, 'b', label='Linear')
ax.plot(x, x ** 2, 'r', label='Quadratic')

# Add the legend. Use the loc argument to specify the position of the legend (auto-location by default)
# http://matplotlib.org/users/legend_guide.html#legend-location
ax.legend(loc=(0.05, 0.85))

fig_4.show()

# SAVE FIGURE TO A FILE

# Extension determines type of file. Can also specify DPI here
fig_3.savefig('fig_3.jpg')
fig_3.savefig('fig_3.png')
fig_3.savefig('fig_3.png', dpi=200)

