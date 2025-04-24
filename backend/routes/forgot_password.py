from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db
from datetime import datetime, timedelta
import secrets

forgot_password_bp = Blueprint("forgot_password", __name__, template_folder="../templates")

@forgot_password_bp.route("/forgot-password", methods=["GET", "POST"])
def forgot_password():
    if request.method == "POST":
        username = request.form.get("username")
        db = get_db()
        cursor = db.cursor(dictionary=True)

        cursor.execute("SELECT user_id FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()

        if not user:
            flash("If an account with that username exists, a reset link will be sent.")
            return redirect(url_for("login.login"))

        # Generate secure token
        token = secrets.token_urlsafe(32)
        expiry = datetime.utcnow() + timedelta(minutes=30)

        # Save token to DB
        cursor.execute("""
            INSERT INTO password_resets (user_id, token, expires_at)
            VALUES (%s, %s, %s)
        """, (user['user_id'], token, expiry))
        db.commit()

        reset_link = f"http://127.0.0.1:8080/reset-password/{token}"
        flash(f"Password reset link (send via email): {reset_link}")

        flash("If an account with that username exists, a reset link has been sent.")
        return redirect(url_for("login.login"))

    return render_template("forgot_password.html")
