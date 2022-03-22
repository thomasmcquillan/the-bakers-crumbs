import os
from flask import Flask, flash, render_template, redirect, request, session, url_for
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


# Setting Config variables
app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
def index():
    """ Returns user to Homepage """
    return render_template("index.html")


@app.route("/get_recipes")
def get_recipes():
    """ Displays recipes from MongoDB Database """
    recipes = mongo.db.recipes.find()
    return render_template("recipes.html", recipes=recipes)


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Returns recipes based on keyword search by user
    """
    query = request.form.get("query")
    recipes = mongo.db.recipes.find({"$text": {"$search": query}})
    # recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return render_template("searchresults.html", recipes=recipes)


@app.route("/view_recipe", methods=["GET"])
def view_recipe():
    """ Displays page with a specific recipe, as chosen by the user """
    recipes = mongo.db.recipes.find()
    return render_template("view_recipe.html", recipes=recipes)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    The register route allows new users to create a user
    account, using a unique username and valid password.
    """
    if request.method == "POST":
        # Checks to see if username already exists.
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already in use")
            return redirect(url_for("register"))
        # Takes user info and places them in the database.
        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(
                request.form.get("password"))
            }
        mongo.db.users.insert_one(register)

        # Puts user into a new 'session' cookie.
        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("account", username=session["user"]))

    return render_template("register.html")


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)
