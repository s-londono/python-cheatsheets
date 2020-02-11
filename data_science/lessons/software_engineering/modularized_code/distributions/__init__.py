# This file makes the distributions folder a Python Package
# This code is run every time the package get imported in a program

# The . is required in Python 3!
# This line allows importing the Gaussian class directly from the package (e.g. from distributions import Gaussian)
from .GaussianDistribution import Gaussian

# conda create --name=environmentname --clone=base
# source activate environmentname
# conda install numpy

# python -m venv venvname
# source venvname/bin/activate

# To install the package, check ../setup.py
