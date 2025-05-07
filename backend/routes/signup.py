from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from password_utils import generate_salt, hash_password
from db import get_db
import re

signup_bp = Blueprint("signup", __name__, template_folder="../templates")

def is_strong_password(password):
    if len(password) < 8:
        return False
    if not re.search(r"\d", password):  # Check for digits
        return False
    if not re.search(r"[A-Za-z]", password):  # Check for letters
        return False
    if not re.search(r"[@$!%*?&]", password):  # Check for special characters
        return False
    return True

@signup_bp.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        db = get_db()
        cursor = db.cursor(dictionary=True)
        
        name = request.form.get("name")
        surname = request.form.get("surname")
        username = request.form.get("username")
        password = request.form.get("password")
        birth_date_str = request.form.get("birthdate")
        
        # Validate birthdate
        birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
        today = datetime.today()
        age = (today - birth_date).days // 365
        
        if birth_date > today:
            flash("Birthdate cannot be in the future.", "error")
            return render_template("signup.html")

        # Check if the user is at least 18 years old
        if age < 18:
            flash("You must be at least 18 years old to register.", "error")
            return render_template("signup.html")
        
        if not is_strong_password(password):
            flash("Password must be at least 8 characters long, contain a number, a letter, and a special character.", "error")
            return render_template("signup.html")
        
        salt = generate_salt()
        hashed_password = hash_password(password, salt)

        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            username_check = cursor.fetchall()
            if username_check:
                flash(f"Username {username} is taken, try another one", 'error')
                return render_template("signup.html")

            cursor.execute("""
                INSERT INTO users (username, name, surname, birth_date, password_hash, password_salt, is_admin)
                VALUES (%(username)s, %(name)s, %(surname)s, %(birth_date)s, %(password_hash)s, %(password_salt)s, False)
                """, {
                'username': username,
                'name': name,
                'surname': surname,
                'birth_date': birth_date,
                'password_hash': hashed_password,
                'password_salt': salt,
            })

            db.commit()


            # At this point, the user is valid, you would typically save to the database here
            # For now, just a placeholder success message
            flash("Account created successfully! Please log in.", "success")

            # Redirect to login page after successful registration
            return redirect(url_for("login.login"))

        except ValueError:
            # Handle invalid birthdate format
            flash("Invalid birth date format. Please use YYYY-MM-DD.", "error")
            return render_template("signup.html")
        except Exception as e:
            db.rollback()
            return jsonify({'error': str(e)}), 400
        finally:
            cursor.close()
            db.close()
            
    return render_template("signup.html")
