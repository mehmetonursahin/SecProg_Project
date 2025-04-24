from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from datetime import datetime

logout_bp = Blueprint("logout", __name__, template_folder="../templates")

@logout_bp.route("/logout")
def logout():
    # Handle logout (e.g., clear session, cookies)
    session.clear()
    flash("You have logged out successfully.", "success")
    return redirect(url_for("login.login"))