# import necessary libraries
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

# create instance of Flask app
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")

# create route that renders index.html template and finds documents from mongo
@app.route("/")
def home():

    # Find data
    returndata = mongo.db.collection.find()

    # return template and data
    return render_template("index.html", returndata=returndata)


# Route that will trigger scrape functions
@app.route("/scrape")
def scrape():

    # Run scraped functions
    returndata = scrape_mars.scrape()


    # Insert forecast into database
    mongo.db.collection.drop()
    mongo.db.collection.insert_one(returndata)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
