import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
if os.path.exists("env.py"):
    import env

# Adds variable 'app', to store new instance of Flask

app = Flask(__name__)

# Mongo database configuration settings
app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")

# Setting variable to retrieve secret access key
app.secret_key = os.environ.get("SECRET_KEY")

# Mongo database connection
mongo = PyMongo(app)


# Home Page
@app.route("/")
@app.route("/get_recipes")
def get_recipes():

    total = mongo.db.recipes.find().count()
    recipes = mongo.db.recipes.find()
    return render_template("index.html", recipes=recipes)

if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)

# Search recipes function
@app.route("/search", methods=["GET", "POST"])
def search():
    query = request.form.get("query")
    recipes = mongo.db.recipes.find({"$text": {"$search": query}})
    return render_template("recipes.html", recipes=recipes)

