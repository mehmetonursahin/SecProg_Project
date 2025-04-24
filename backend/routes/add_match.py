from flask import Blueprint, render_template, request, redirect, url_for, flash
from db import get_db

add_match_bp = Blueprint("add_match", __name__, template_folder="../templates")

@add_match_bp.route("/add_match", methods=["GET", "POST"])
def add_match():
    if request.method == "POST":
        # Get match details from the form
        home_club_id = request.form.get("home_club_id")
        away_club_id = request.form.get("away_club_id")
        date = request.form.get("date")
        score_home = request.form.get("score_home")
        score_away = request.form.get("score_away")
        referee = request.form.get("referee")
        
        stadium_option = request.form.get('stadium_option')
        
        db = get_db()
        cursor = db.cursor()

        try:
            if stadium_option == 'home_team':
                cursor.execute("SELECT stadium_name FROM clubs WHERE club_id = %s", (home_club_id,))
                stadium_result = cursor.fetchone()
                if not stadium_result:
                    flash(f"No club found with ID {home_club_id}.", "error")
                    return render_template("add_match.html")

                stadium = stadium_result[0]
            else:
                stadium = request.form.get('custom_stadium')
                if not stadium:
                    flash("Please enter a custom stadium name.", "error")
                    return render_template("add_match.html")

            cursor.execute("""
                INSERT INTO games (home_club_id, away_club_id, date, home_club_goals, away_club_goals, stadium, referee)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """, (home_club_id, away_club_id, date, score_home, score_away, stadium, referee))
            db.commit()
            flash("Match added successfully!")
            return redirect(url_for("home.home"))
        except Exception as e:
            db.rollback()
            flash("Error adding match: " + str(e))
            return redirect(url_for("add_match.add_match"))

    return render_template("add_match.html")
