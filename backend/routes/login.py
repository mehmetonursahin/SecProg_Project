from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime
from db import get_db

login_bp = Blueprint("login", __name__, template_folder="../templates")

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        username = request.form.get("username")
        password = request.form.get("password")
        
        cursor.execute("SELECT * FROM users WHERE username = %(username)s AND password_hash = %(password)s",
                       {
                           'username': username,
                           'password': password
                       })
        is_valid_user = cursor.fetchall()
        
        if not is_valid_user:
            flash("Your account credentials are not correct, try again!")
            return render_template("login.html")
        # For now, directly redirect to the homepage after login
        return redirect(url_for("home.home"))

    return render_template("login.html")