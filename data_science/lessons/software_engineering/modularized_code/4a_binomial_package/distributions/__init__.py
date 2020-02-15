# This file makes the distributions folder a Python Package
# This code is run every time the package get imported in a program

# The . is required in Python 3!
# This line allows importing the Gaussian class directly from the package (e.g. from distributions import Gaussian)
from .BinomialDistribution import Binomial
from .GaussianDistribution import Gaussian

# conda create --name=environmentname --clone=base
# source activate environmentname
# conda install numpy

# python -m venv venvname
# source venvname/bin/activate

# To install the package, check ../setup.py

# UPLOADING TO TEST PYPI

# - Create package dist/tar:
# python setup.py sdist
#
# - Install Twine:
# pip install twine
#
# - Upload package to the Test Pypi repo (update version in setup.py if necessary):
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*
#
# - Check the package exists in your testpypi account
#
# - Test installing the package from Test Pypi:
# pip install --index-url https://test.pypi.org/simple/ {package_name}

# UPLOADING TO PYPY
#
# twine upload dist/*
#
# - Uninstall previously installed from Test Pypi:
# pip uninstall {package_name}
#
# - Reinstall from Pypi:
# pip install {package_name}
#
# * NOTE: Dashes (-) should be replaced with underscores (_) when using the package in Python code

# UPLOADING TO TEST PYPI

# - Create package dist/tar:
# python setup.py sdist
#
# - Install Twine:
# pip install twine
#
# - Upload package to the Test Pypi repo (update version in setup.py if necessary):
# twine upload --repository-url https://test.pypi.org/legacy/ dist/*
#
# - Check the package exists in your testpypi account
#
# - Test installing the package from Test Pypi:
# pip install --index-url https://test.pypi.org/simple/ {package_name}
# UPLOADING TO PYPY
#
# twine upload dist/*
#
# - Uninstall previously installed from Test Pypi:
# pip uninstall {package_name}
#
# - Reinstall from Pypi:
# pip install {package_name}
#
# * NOTE: Dashes (-) should be replaced with underscores (_) when using the package in Python code
