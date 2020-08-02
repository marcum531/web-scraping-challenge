from flask import Flask, render_template
from flask_pymongo import PyMongo
import Mission_to_Mars.py

app = Flask (__name__)
mongo = PyMongo(app, url="mongodb://localhost:27017")

