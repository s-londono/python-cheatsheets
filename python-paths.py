import os
import sys

# The __file__ variable path of the current module file (defined only when executing the Python script externally)
print(__file__)

# Get the current working directory
print(os.getcwd())

# Set the current working directory
os.chdir("/tmp/")

# Insert a new entry into the path, at a specified position. In this example, inserts the parent of the working dir
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
