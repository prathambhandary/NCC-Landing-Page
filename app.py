"""
Manipal Jnanasudha NCC Naval Sub Unit - Website
6 Kar Naval Unit NCC, Karnataka & Goa Directorate

Flask application entry point.
Run with:  python app.py
"""

import json
import os
from pathlib import Path
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_jwt_extended import JWTManager, unset_jwt_cookies
from config import Config
from auth import login
from decorators import admin_required
from github import update_json, get_json

app = Flask(__name__)
app.config.from_object(Config)

jwt = JWTManager(app)

app.add_url_rule(
    "/api/login",
    view_func=login,
    methods=["POST"]
)

DATA_DIR = Path(__file__).parent / "data"

from flask_jwt_extended import JWTManager

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_COOKIE_HTTPONLY"] = True
app.config["JWT_COOKIE_SECURE"] = False   # True on HTTPS
app.config["JWT_COOKIE_SAMESITE"] = "Lax"

jwt = JWTManager(app)

def load_json(filename):
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)

# ---------------------------------------------------------------------------
# Admin
# ---------------------------------------------------------------------------

@app.route("/admin")
@admin_required
def dashboard():
    return render_template("admin/dashboard.html")


@app.route("/admin/login")
def admin_login():
    return render_template("admin/login.html")


@app.route("/api/logout", methods=["POST"])
def logout():
    response = jsonify({"success": True})
    unset_jwt_cookies(response)
    return response


@app.route("/admin/news")
@admin_required
def admin_news():
    news = get_json("data/news.json")
    return render_template("admin/news.html", news=news)


@app.route("/admin/news/save", methods=["POST"])
@admin_required
def save_news():

    news = request.json

    update_json(
        "data/news.json",
        news,
        "Updated news"
    )

    return jsonify({
        "success": True
    })



# ---------------------------------------------------------------------------
# Context injected into every template
# ---------------------------------------------------------------------------
@app.context_processor
def inject_globals():
    return {
        "unit_name": "Manipal Jnanasudha NCC Naval Sub Unit",
        "parent_unit": "6 Kar Naval Unit NCC",
        "directorate": "Karnataka & Goa Directorate, NCC",
        "cadet_strength": 100,
    }


# ---------------------------------------------------------------------------
# Page routes
# ---------------------------------------------------------------------------
@app.route("/")
def index():
    officers = load_json("officers.json")
    news = load_json("news.json")
    news_sorted = sorted(news, key=lambda n: n["date"], reverse=True)
    return render_template("index.html", officers=officers, news=news_sorted)


@app.route("/about-ncc")
def about_ncc():
    return render_template("about_ncc.html")


@app.route("/opportunities")
def opportunities():
    return render_template("opportunities.html")


@app.route("/achievers")
def achievers():
    achievers_data = load_json("achievers.json")
    return render_template("achievers.html", achievers=achievers_data)


@app.route("/alumni")
def alumni():
    alumni_data = load_json("alumni.json")
    return render_template("alumni.html", alumni=alumni_data)


@app.route("/gallery")
def gallery():
    gallery_data = load_json("gallery.json")
    years = sorted({item["date"][:4] for item in gallery_data}, reverse=True)
    return render_template("gallery.html", years=years)


@app.route("/api/gallery")
def api_gallery():
    gallery_data = load_json("gallery.json")

    category = request.args.get("category", "all")
    year = request.args.get("year", "all")
    month = request.args.get("month", "all")

    def matches(item):
        item_year, item_month, _ = item["date"].split("-")
        if category != "all" and item["category"] != category:
            return False
        if year != "all" and item_year != year:
            return False
        if month != "all" and item_month != month:
            return False
        return True

    filtered = [item for item in gallery_data if matches(item)]
    filtered.sort(key=lambda i: i["date"], reverse=True)
    return jsonify(filtered)


if __name__ == "__main__":
    app.run(debug=True, port=5000, host="0.0.0.0")
