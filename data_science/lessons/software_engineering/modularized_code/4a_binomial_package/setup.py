from setuptools import setup

# Install a package in PIP, locally
# - Add a setup.py file beside the package folder (distributions in this case)
# - Run pip install . from the directory containing setup.py.
# - Now can use the package from anywhere!
#   E.g. from distributions import Gaussian
# - Check the package location with:
#   distributions.__file__
# To reinstall the package run: pip install --upgrade .
setup(name='distributions',
      version='0.1',
      description='Probability distributions',
      packages=['distributions'],
      zip_safe=False)
