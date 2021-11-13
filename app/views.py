from os import name
from flask import Blueprint, render_template
from flask_login import login_required, current_user

views = Blueprint("views", __name__)

@views.route("/")
@views.route("/home")
@login_required
def home():
    return render_template("index.html", user=current_user)

@views.route("/login")
def login():
    return render_template("login.html", user=current_user)