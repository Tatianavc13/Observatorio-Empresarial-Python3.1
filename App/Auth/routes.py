from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from .. import db
from ..models import User

auth_bp = Blueprint("auth", __name__, template_folder="../templates/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        email = request.form.get("email")
        password = request.form.get("password")
        user = User.query.filter_by(email=email, active=True).first()
        if user and user.check_password(password):
            login_user(user)
            return redirect(url_for("flashes.admin_list"))
        flash("Credenciales inválidas", "danger")
    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("public.home"))


