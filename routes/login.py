from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime

login_bp = Blueprint("login", __name__, template_folder="../templates")

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Placeholder: handle login logic here
        username = request.form.get("username")
        password = request.form.get("password")
        # For now, directly redirect to the homepage after login
        return redirect(url_for("home.home"))

    return render_template("login.html")