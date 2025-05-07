from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db

delete_match_bp = Blueprint("delete_match", __name__)

@delete_match_bp.route("/delete_match/<int:match_id>", methods=["GET", "POST"])
def delete_match(match_id):
    if not session.get('is_admin'):
        flash("You do not have permission to delete a match.", "error")
        return redirect(url_for('home.home'))
    db = get_db()
    cursor = db.cursor(dictionary=True)

    # Fetch match details to show in confirmation
    cursor.execute("SELECT * FROM games WHERE game_id = %s", (match_id,))
    match = cursor.fetchone()

    if not match:
        flash("Match not found.")
        return redirect(url_for("home.home"))

    if request.method == "POST":
        try:
            cursor.execute("DELETE FROM games WHERE game_id = %s", (match_id,))
            db.commit()
            flash("Match deleted successfully!")
            return redirect(url_for("home.home"))
        except Exception as e:
            db.rollback()
            flash("Error deleting match: " + str(e))
            return redirect(url_for("home.home"))

    # Display the delete confirmation page
    return render_template("delete_match.html", match=match)
