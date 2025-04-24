from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db
from datetime import datetime
from password_utils import hash_password
import secrets

reset_password_bp = Blueprint("reset_password", __name__, template_folder="../templates")

@reset_password_bp.route("/reset-password/<token>", methods=["GET", "POST"])
def reset_password(token):
    db = get_db()
    cursor = db.cursor(dictionary=True)

    cursor.execute("""
        SELECT pr.user_id, u.username, pr.expires_at
        FROM password_resets pr
        JOIN users u ON pr.user_id = u.user_id
        WHERE pr.token = %s
    """, (token,))
    reset_request = cursor.fetchone()

    if not reset_request or datetime.utcnow() > reset_request['expires_at']:
        flash("This password reset link is invalid or has expired.")
        return redirect(url_for("login.login"))

    if request.method == "POST":
        new_password = request.form.get("new_password")
        confirm_password = request.form.get("confirm_password")

        if new_password != confirm_password:
            flash("Passwords do not match.")
            return render_template("reset_password.html", token=token)

        salt = secrets.token_hex(16)
        hashed_password = hash_password(new_password, salt)

        cursor.execute("""
            UPDATE users
            SET password_hash = %s, password_salt = %s
            WHERE user_id = %s
        """, (hashed_password, salt, reset_request['user_id']))

        cursor.execute("DELETE FROM password_resets WHERE user_id = %s", (reset_request['user_id'],))
        db.commit()

        flash("Your password has been reset successfully. Please log in.")
        return redirect(url_for("login.login"))

    return render_template("reset_password.html", token=token)
