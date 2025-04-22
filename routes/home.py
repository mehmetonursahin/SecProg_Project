from flask import Blueprint, render_template, request, redirect, url_for, flash
from datetime import datetime

home_bp = Blueprint("home", __name__, template_folder="../templates")

# Home route - for the matches page
@home_bp.route("/home")
def home():
    # Placeholder for matches data (hardcoded for now)
    matches = [
        {"team1": "Team A", "team2": "Team B", "score": "1-0", "date": "2025-04-22"},
        {"team1": "Team C", "team2": "Team D", "score": "2-2", "date": "2025-04-23"},
        {"team1": "Team E", "team2": "Team F", "score": "0-3", "date": "2025-04-24"},
    ]
    
    return render_template("home.html", matches=matches)