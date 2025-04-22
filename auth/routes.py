from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime

auth_bp = Blueprint("auth", __name__, template_folder="../templates")

# Home route - for the matches page
@auth_bp.route("/home")
def home():
    # Placeholder for matches data (hardcoded for now)
    matches = [
        {"team1": "Team A", "team2": "Team B", "score": "1-0", "date": "2025-04-22"},
        {"team1": "Team C", "team2": "Team D", "score": "2-2", "date": "2025-04-23"},
        {"team1": "Team E", "team2": "Team F", "score": "0-3", "date": "2025-04-24"},
    ]
    
    return render_template("home.html", matches=matches)

@auth_bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        # Placeholder: handle login logic here
        username = request.form.get("username")
        password = request.form.get("password")
        # For now, directly redirect to the homepage after login
        return redirect(url_for("auth.home"))

    return render_template("login.html")

@auth_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        name = request.form.get("name")
        surname = request.form.get("surname")
        username = request.form.get("username")
        password = request.form.get("password")
        birth_date_str = request.form.get("birthdate")
        is_admin = "is_admin" in request.form  # This checks if the checkbox was checked

        try:
            # Validate birthdate
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
            today = datetime.today()
            age = (today - birth_date).days // 365

            # Check if the user is at least 18 years old
            if age < 18:
                flash("You must be at least 18 years old to register.", "error")
                return render_template("signup.html")

            # At this point, the user is valid, you would typically save to the database here
            # For now, just a placeholder success message
            if is_admin:
                flash("You have registered as an admin. Please log in.", "success")
            else:
                flash("Account created successfully! Please log in.", "success")

            # Redirect to login page after successful registration
            return redirect(url_for("auth.login"))

        except ValueError:
            # Handle invalid birthdate format
            flash("Invalid birth date format. Please use YYYY-MM-DD.", "error")
            return render_template("signup.html")

    return render_template("signup.html")


@auth_bp.route("/logout")
def logout():
    # Handle logout (e.g., clear session, cookies)
    flash("You have logged out successfully.", "success")
    return redirect(url_for("auth.login"))
