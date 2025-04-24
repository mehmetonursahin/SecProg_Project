from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from db import get_db

home_bp = Blueprint("home", __name__, template_folder="../templates")

@home_bp.route("/home", methods=["GET", "POST"])
def home():
    db = get_db()
    cursor = db.cursor(dictionary=True)

    is_admin = session.get('is_admin')

    # Check if a search query was submitted
    search_query = request.args.get("search", "")

    # Base query with joins
    base_query = """
        SELECT 
            g.*, 
            home_club.name AS home_club_name, 
            away_club.name AS away_club_name
        FROM games g
        JOIN clubs home_club ON g.home_club_id = home_club.club_id
        JOIN clubs away_club ON g.away_club_id = away_club.club_id
    """

    # If there's a search query, add WHERE condition
    if search_query:
        base_query += """
            WHERE home_club.name LIKE %s OR away_club.name LIKE %s
        """
        cursor.execute(base_query + " ORDER BY g.date DESC", (f"%{search_query}%", f"%{search_query}%"))
    else:
        cursor.execute(base_query + " ORDER BY g.date DESC")

    matches = cursor.fetchall()

    return render_template("home.html", matches=matches, is_admin=is_admin, search_query=search_query)


@home_bp.route("/add_club", methods=["GET", "POST"])
def add_club():
    if request.method == "POST":
        if not session.get('is_admin'):  # If the user is not an admin
            flash("You do not have permission to add a club.", "error")
            return redirect(url_for('home.home'))
        
        club_id = request.form.get('club_id')
        club_name = request.form.get('name')
        if not club_id or not club_name:
            flash("Club ID and name is required.", "error")
            return render_template("add_club.html")
        stadium_name = request.form.get('stadium_name', '')
        stadium_seats = request.form.get('stadium_seats', '')
        coach_name = request.form.get('coach_name', '')
        url = request.form.get('url', '')

        # Insert the new club into the database
        db = get_db()
        cursor = db.cursor()
        
        cursor.execute("SELECT * FROM clubs WHERE club_id = %s", (club_id,))
        club_id_check = cursor.fetchone()
        
        if club_id_check:
            flash(f"Club ID {club_id} is used, try another ID!")
            return render_template("add_club.html")

        cursor.execute("""
            INSERT INTO clubs (club_id, name, stadium_name, stadium_seats, coach_name, url)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (club_id, club_name, stadium_name, stadium_seats, coach_name, url))

        db.commit()

        flash(f"Club '{club_name}' has been added successfully!", "success")
        return redirect(url_for('home.home'))

    return render_template("add_club.html")
