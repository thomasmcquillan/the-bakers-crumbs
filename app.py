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

