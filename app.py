import os
from flask import (
    Flask, flash, render_template,
    redirect, request, session, url_for)
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
if os.path.exists("env.py"):
    import env


app = Flask(__name__)

app.config["MONGO_DBNAME"] = os.environ.get("MONGO_DBNAME")
app.config["MONGO_URI"] = os.environ.get("MONGO_URI")
app.secret_key = os.environ.get("SECRET_KEY")

mongo = PyMongo(app)


@app.route("/")
@app.route("/index")
def index():
    """
    Returns user to Homepage
    """
    return render_template("index.html")


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Returns recipes based on keyword search by user
    """
    query = request.form.get("query")
    recipes = mongo.db.recipes.find({"$text": {"$search": query}})
    return render_template("searchresults.html", recipes=recipes)


@app.route("/view_recipe/<recipe_id>")
def view_recipe(recipe_id):
    """
    Displays page with a specific recipe, as chosen by the user
    """
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("view_recipe.html", recipe=recipe)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    The register route allows new users to create a user
    account, using a unique username and valid password.
    """
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            flash("Username already in use")
            return redirect(url_for("register"))

        register = {
            "username": request.form.get("username").lower(),
            "password": generate_password_hash(
                request.form.get("password"))
        }
        mongo.db.users.insert_one(register)

        session["user"] = request.form.get("username").lower()
        flash("Registration Successful")
        return redirect(url_for("account", username=session["user"]))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    """
    Login function that checks to see if username entered
    is already in the database. It also checks whether the hashed
    password matches the one entered. In both cases it will alert
    the user with flash messages to notify them of errors and/or
    success.
    """
    if request.method == "POST":
        existing_user = mongo.db.users.find_one(
            {"username": request.form.get("username").lower()})

        if existing_user:
            if check_password_hash(
                existing_user["password"], request.form.get("password")):
                session["user"] = request.form.get("username").lower()
                flash("Welcome back, {}".format(
                    request.form.get("username")))
                return redirect(url_for(
                    "account", username=session["user"]))

        else:
            flash("Username or password is incorrect")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
    Retrieves the session user's username from database
    """
    if "user" not in session:
        return redirect(url_for("login"))

    username = session["user"]

    user = mongo.db.users.find_one({"username": username})
    if not user:
        return redirect(url_for("login"))
    return render_template("profile.html", username=username)


@app.route("/category/<categories>")
def category(categories):
    """
    Displays all recipes in a given category.
    """
    if categories == "all":
        recipes = list(mongo.db.recipes.find())
    elif categories == "bread":
        recipes = list(mongo.db.recipes.find({"category_name": "Bread"}))
    elif categories == "pizza":
        recipes = list(mongo.db.recipes.find({"category_name": "Pizza"}))
    elif categories == "cakes":
        recipes = list(mongo.db.recipes.find({"category_name": "Cakes"}))
    elif categories == "cookies":
        recipes = list(mongo.db.recipes.find({"category_name": "Cookies"}))
    elif categories == "scones":
        recipes = list(mongo.db.recipes.find({"category_name": "Scones"}))
    elif categories == "muffins":
        recipes = list(mongo.db.recipes.find({"category_name": "Muffins"}))
    else:
        recipes = list(mongo.db.recipes.find())
    return render_template(
        "category.html", recipes=recipes, categories=categories)


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=True)
