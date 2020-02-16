# When the package is run, the __init__ is executed first
from flask import Flask

app = Flask(__name__)

from worldbankapp import routes