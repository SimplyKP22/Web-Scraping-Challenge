from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use PyMongo to establish Mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# create the home route. This will render the index.html template data from Mongo
@app.route('/')
def home():

    # Find one record of data from the mongo database
    mars_info = mongo.db.collection.find_one()

    # Return template and data
    return render_template("index.html", mars=mars_info)


# Set our path to /scrape. This will run our scrape function
@app.route("/scrape")
def scrape():

    # create a listings database
    mars = mongo.db.mars

    # call the scrape function in our scrape_mars file. This will scrape and save to mongo.
    mars_data = scrape_mars.scrape()

    # update our listings with the data that is being scraped.
    mars.insert_one(mars_data)

    # Redirect back to home page
    return redirect("/")


if __name__ == "__main__":
    app.run(debug=True)
