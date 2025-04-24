from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime
from password_utils import hash_password
from db import get_db

login_bp = Blueprint("login", __name__, template_folder="../templates")

@login_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        username = request.form.get("username")
        password = request.form.get("password")
        
        cursor.execute("SELECT password_hash, password_salt, is_admin FROM users WHERE username = %s", (username,))
        user_data = cursor.fetchone()

        if not user_data:
            flash(f"No account with the username '{username}' is not found! Have you signed up?")
            return render_template("login.html")

        stored_hash = user_data['password_hash']
        stored_salt = user_data['password_salt']

        hashed_input_password = hash_password(password, stored_salt)

        if hashed_input_password != stored_hash:
            flash("Your account credentials are not correct, try again!")
            return render_template("login.html")
        
        session['username'] = username
        session['is_admin'] = user_data['is_admin']

        # If credentials are correct:
        return redirect(url_for("home.home"))

    return render_template("login.html")