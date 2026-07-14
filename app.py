"""
Manipal Jnanasudha NCC Naval Sub Unit - Website
6 Kar Naval Unit NCC, Karnataka & Goa Directorate

Flask application entry point.
Run with:  python app.py
"""

import json
from pathlib import Path
from flask import Flask, render_template, jsonify, request, send_from_directory
import secrets
import os

ADMIN_PASSWORD = os.environ.get("ADMIN_PASSWORD") if os.environ.get("ADMIN_PASSWORD") else "admin123"  # default password
ADMIN_TOKENS = {}  # simple in-memory token store


app = Flask(__name__)

DATA_DIR = Path(__file__).parent / "data"


def load_json(filename):
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)


# ---------------------------------------------------------------------------
# ADMIN LOGIN – minimal auth (no CRUD)
# ---------------------------------------------------------------------------



# Serve the admin HTML page (place admin.html in static/)
@app.route("/admin")
def admin_panel():
    return send_from_directory("templates", "admin.html")

# Login endpoint
@app.route("/api/admin/login", methods=["POST"])
def admin_login():
    data = request.get_json()
    if not data or data.get("password") != ADMIN_PASSWORD:
        return jsonify({"success": False, "error": "Invalid password"}), 401
    token = secrets.token_urlsafe(32)
    ADMIN_TOKENS[token] = True
    return jsonify({"success": True, "token": token})

# Verify token (used by the frontend on page load)
@app.route("/api/admin/verify", methods=["GET"])
def admin_verify():
    token = request.headers.get("X-Admin-Token")
    if token and token in ADMIN_TOKENS:
        return jsonify({"valid": True})
    return jsonify({"valid": False}), 401

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


# ---------------------------------------------------------------------------
# JSON API used by the gallery page's calendar filter (static/js/gallery.js)
# ---------------------------------------------------------------------------
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
