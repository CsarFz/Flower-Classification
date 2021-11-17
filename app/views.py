from flask import Blueprint, render_template, request, jsonify
from flask.helpers import flash
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

@views.route("/acercade")
def about():
    return render_template("acercade.html", user=current_user)

@views.route("/profile")
@login_required
def profile():
    return render_template("profile.html", user=current_user)

@views.route("/classify-flower", methods=["GET", "POST"])
@login_required
def classify_flower():
    if request.method == "POST":
        if request.files:
            image = request.files["image"]
            
            if image.filename == "":
                flash("La imagen debe tener un nombre.", category="error")
            print(f'Image: {image}')
    return render_template("index.html", user=current_user)