# When the package is run, the __init__ is executed first
from flask import Flask
from ..worldbankapp import routes

app = Flask(__name__)
