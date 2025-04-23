from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from datetime import datetime
from db import get_db

signup_bp = Blueprint("signup", __name__, template_folder="../templates")

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
        is_admin = "is_admin" in request.form  # This checks if the checkbox was checked

        try:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            username_check = cursor.fetchall()
            if username_check:
                flash(f"Username {username} is taken, try another one", 'error')
                return render_template("signup.html")
            
            # Validate birthdate
            birth_date = datetime.strptime(birth_date_str, "%Y-%m-%d")
            today = datetime.today()
            age = (today - birth_date).days // 365

            # Check if the user is at least 18 years old
            if age < 18:
                flash("You must be at least 18 years old to register.", "error")
                return render_template("signup.html")

            cursor.execute("""
                INSERT INTO users (username, name, surname, birth_date, password_hash, password_salt, is_admin)
                VALUES (%(username)s, %(name)s, %(surname)s, %(birth_date)s, %(password_hash)s, %(password_salt)s, %(is_admin)s)
                """, {
                'username': username,
                'name': name,
                'surname': surname,
                'birth_date': birth_date,
                'password_hash': password,
                'password_salt': "",
                'is_admin' : is_admin
            })

            db.commit()


            # At this point, the user is valid, you would typically save to the database here
            # For now, just a placeholder success message
            if is_admin:
                flash("You have registered as an admin. Please log in.", "success")
            else:
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
