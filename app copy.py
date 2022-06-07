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
    Returns user to homepage.
    """
    return render_template("index.html")


@app.route("/all_recipes")
def all_recipes():
    """
    Displays all recipes in database.
    """
    recipes = list(mongo.db.recipes.find().sort("recipe_name", 1))
    return render_template("recipes.html", recipes=recipes)


@app.route("/all_categories")
def all_categories():
    """
    Displays all categories of recipes.
    """
    categories = list(mongo.db.categories.find().sort("category_name", 1))
    return render_template("categories.html", categories=categories)


@app.route("/search", methods=["GET", "POST"])
def search():
    """
    Returns recipes based on keyword search by user
    """
    query = request.form.get("query")
    recipes = list(mongo.db.recipes.find({"$text": {"$search": query}}))
    return render_template("recipes.html", recipes=recipes)


@app.route("/register", methods=["GET", "POST"])
def register():
    """
    Allows new users to create a user account, using a unique
    username and valid password. If successful, puts user into
    a new session.
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
        return redirect(url_for("profile", username=session["user"]))

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
                return redirect(url_for("profile", username=session["user"]))
        else:
            flash("Invalid username and/or password")
            return redirect(url_for("login"))

    return render_template("login.html")


@app.route("/profile/<username>", methods=["GET", "POST"])
def profile(username):
    """
    Retrieves the session user's username from database
    """
    username = mongo.db.users.find_one(
        {"username": session["user"]})["username"]
    
    if session["user"]:
        recipes = list(mongo.db.recipes.find({"created_by": username}))
        return render_template(
            "profile.html", username=username, recipes=recipes)
    else:
        return redirect(url_for("login"))


@app.route("/logout")
def logout():
    """
    Removes a user from their session.
    """
    if not session.get("user"):
        return render_template("templates/404.html")

    flash("Goodbye for now. Happy baking!")
    session.pop("user")
    return redirect(url_for("index"))


@app.route("/delete_user/<username>")
def delete_user(username):
    """
    This function allows deletion of a user account.
    """
    mongo.db.users.remove({"username": username})
    flash("Your account has been deleted")
    session.pop("user")
    return redirect(url_for("register"))


@app.route("/get_category/<category_id>")
def get_category(category_id):
    """
    Displays all recipes in a given category.
    """
    category = mongo.db.categories.find_one({"_id": ObjectId(category_id)})
    recipes = list(mongo.db.recipes.find(
        {"category_name": category["category_name"]}))
    return render_template(
        "recipes.html", recipes=recipes)


@app.route("/view_recipe/<recipe_id>")
def view_recipe(recipe_id):
    """
    Displays full recipe, as selected by user.
    """
    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    return render_template("view_recipe.html", recipe=recipe)


@app.route("/add_recipe", methods=["GET", "POST"])
def add_recipe():
    """
    Enables user to add a recipe of their own to the db
    """
    if request.method == "POST":
        recipe = {
            "recipe_name": request.form.get("recipe_name"),
            "recipe_description": request.form.get("description"),
            "category_name": request.form.get("category_name"),
            "image_url": request.form.get("image_url"),
            "ingredients": request.form.getlist("ingredients"),
            "directions": request.form.getlist("directions"),
            "created_by": session["user"]
        }
        mongo.db.recipes.insert_one(recipe)
        flash("Recipe successfully added!")
        return redirect(url_for("profile", username=session["user"]))

    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template("add_recipe.html", categories=categories)


@app.route("/edit_recipe/<recipe_id>", methods=["GET", "POST"])
def edit_recipe(recipe_id):
    """
    Allows user to update their previously submitted recipes
    """
    if request.method == "POST":
        submit = {
            "recipe_name": request.form.get("recipe_name"),
            "recipe_description": request.form.get("description"),
            "category_name": request.form.get("category_name"),
            "image_url": request.form.get("image_url"),
            "ingredients": request.form.getlist("ingredients"),
            "directions": request.form.getlist("directions"),
            "created_by": session["user"]
        }
        mongo.db.recipes.update({"_id": ObjectId(recipe_id)}, submit)
        flash("Recipe successfully updated!")
        return redirect(url_for("profile", username=session["user"]))

    recipe = mongo.db.recipes.find_one({"_id": ObjectId(recipe_id)})
    categories = mongo.db.categories.find().sort("category_name", 1)
    return render_template(
        "edit_recipe.html", recipe=recipe, categories=categories)


@app.route("/delete_recipe/<recipe_id>")
def delete_recipe(recipe_id):
    """
    Deletes recipe from the database. The recipe deletion can
    be performed by the user who submitted it or site admin.
    """
    mongo.db.recipes.delete_one({"_id": ObjectId(recipe_id)})
    flash("recipe deleted!")
    return redirect(url_for("index"))


@app.errorhandler(403)
def forbidden(e):
    """
    404 Error Page - Forbidden
    """
    return render_template('403.html'), 403


@app.errorhandler(404)
def page_not_found(e):
    """
    404 Error page - page not found
    """
    return render_template('404.html'), 404


@app.errorhandler(500)
def internal_server_error(e):
    """
    500 Error page - server error
    """
    return render_template('500.html'), 500


if __name__ == "__main__":
    app.run(host=os.environ.get("IP"),
            port=int(os.environ.get("PORT")),
            debug=False)