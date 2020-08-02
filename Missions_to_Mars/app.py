from flask import Flask, render_template
import pymongo
import Mission_to_Mars.py

app = Flask (__name__)
mongo = pymongo(app, url="mongodb://localhost:27017")

