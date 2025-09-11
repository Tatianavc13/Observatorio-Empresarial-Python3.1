from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user
from .. import db
from ..models import User

auth_bp = Blueprint("auth", __name__, template_folder="../templates/auth")

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        raw_email = request.form.get("email") or ""
        email = raw_email.strip().lower()
        password = (request.form.get("password") or "")

        # Búsqueda case-insensitive por email
        user = User.query.filter(db.func.lower(User.email) == email).first()

        if not user:
            flash("Usuario no encontrado", "danger")
        elif not user.active:
            flash("El usuario está inactivo", "warning")
        elif user.check_password(password):
            login_user(user)
            return redirect(url_for("flashes.admin_list"))
        else:
            flash("Contraseña incorrecta", "danger")
    return render_template("auth/login.html")

@auth_bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("public.home"))


