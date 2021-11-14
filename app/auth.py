from flask import Blueprint, render_template, redirect, url_for, request, flash
from . import db
from .models import User
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import re

auth = Blueprint("auth", __name__)
regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'

@auth.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")

        user = User.query.filter_by(email=email).first()
        if user:
            if check_password_hash(user.password, password):
                flash("¡Conectado!", category="success")
                login_user(user, remember=True)
                return redirect(url_for("views.home"))
            else:
                flash("Usuario o contraseña son incorrectas.", category="error")
        else:
                flash("Usuario o contraseña son incorrectas.", category="error")

    return render_template("login.html", user=current_user)

@auth.route("/sign-up", methods=["GET", "POST"])
def sign_up():
    if request.method == "POST":
        email = request.form.get("email")
        username  = request.form.get("username")
        password  = request.form.get("password")
        confirm_password = request.form.get("confirm-password")
        errors = []

        email_exists = User.query.filter_by(email=email).first()
        username_exists = User.query.filter_by(username=username).first()
        if email_exists:
            flash("El correo electrónico ya existe, use otro.", category="error")
            errors.append(1)
        if username_exists:
            flash("El usuario ya existe, use otro.", category="error")
            errors.append(1)
        print(f'User: -- {username} --')
        if username.strip() == "":
            flash("El campo de usuario está vacío.", category="error")
            errors.append(1)
        elif len(username) <= 3:
            flash("El usuario es muy corto.", category="error")
            errors.append(1)
        if password.strip() == "":
            flash("El campo de contraseña está vacío.", category="error")
            errors.append(1)
        elif len(password) < 8:
            flash("La contraseña es muy corta, use al menos 8 caracteres.", category="error")
            errors.append(1)
        elif password != confirm_password:
            flash("Las contraseñas no coinciden.", category="error")
            errors.append(1)
        if email.strip() == "":
            flash("El campo de correo electrónico está vacío.", category="error")
            errors.append(1)
        elif not validEmail(email):
            flash("El correo electrónico no es valido, ejemplo: nombre@ejemplo.com", category="error")
            errors.append(1)

        if not errors:
            new_user = User(email=email, username=username, password=generate_password_hash(password, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(new_user, remember=True)
            flash("¡Usuario creado!", category="success")
            return redirect(url_for("views.home"))

    return render_template("signup.html", user=current_user)

@auth.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("views.login"))

def validEmail(email):
    if(re.fullmatch(regex, email)):
       return True
    else:
        return