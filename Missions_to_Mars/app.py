from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import Mission_to_Mars

app = Flask (__name__)

app.config['MONGO_URI'] = 'mongodb://localhost:27017/mars_app'
mongo = PyMongo(app)

@app.route("/")
def home():
    mars = mongo.db.mars.find_one()
    return render_template('index.html', mars=mars)

@app.route('/scrape')
def scrape():

    mars = mongo.db.mars
    mars_facts = Mission_to_Mars.scrape()
    mars.update({}, mars_facts, upsert=True)
    return redirect("http://localhost:5000/", code=302)

if __name__=='__main__':
    app.run(debug=True)
