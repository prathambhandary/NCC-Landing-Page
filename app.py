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
from auth import login, verify, logout
from decorators import admin_required
import github
from github import update_json, get_json

app = Flask(__name__)
app.config.from_object(Config)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY")
app.config["JWT_TOKEN_LOCATION"] = ["cookies"]
app.config["JWT_COOKIE_CSRF_PROTECT"] = True
app.config["JWT_COOKIE_HTTPONLY"] = True
app.config["JWT_CSRF_IN_COOKIES"] = True
app.config["JWT_COOKIE_SECURE"] = False   # True on HTTPS
app.config["JWT_COOKIE_SAMESITE"] = "Lax"

jwt = JWTManager(app)

app.add_url_rule(
    "/api/login",
    view_func=login,
    methods=["POST"]
)

DATA_DIR = Path(__file__).parent / "data"


def load_json(filename):
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)

# ---------------------------------------------------------------------------
# Admin
# ---------------------------------------------------------------------------

# ----- Admin authentication endpoints -----
@app.route('/api/admin/login', methods=['POST'])
def admin_login():
    return login()

@app.route('/api/admin/verify', methods=['GET'])
def admin_verify():
    return verify()

@app.route('/api/admin/logout', methods=['POST'])
def admin_logout():
    return logout()

@app.route('/admin/login', methods=['GET'])
def admin_login_page():
    return render_template('admin/login.html')  

# ----- Admin page routes (serve HTML) -----
@app.route('/admin')
@admin_required
def dashboard():
    return render_template('admin/dashboard.html', unit_name=Config.UNIT_NAME or "Manipal Jnanasudha NCC Naval Sub Unit")

@app.route('/admin/status')
def is_admin_logged_in():
    try:
        if verify().status_code == 200:
            return jsonify({"logged_in": True}), 200
    except Exception:
        pass
    
    return jsonify({"logged_in": False}), 401


@app.route('/admin/news')
@admin_required
def admin_news():
    news = github.get_json('data/news.json')
    return render_template('admin/news.html', unit_name=Config.UNIT_NAME or "Manipal Jnanasudha NCC Naval Sub Unit", news=news)

@app.route('/admin/gallery')
@admin_required
def admin_gallery():
    gallery = github.get_json('data/gallery.json')
    return render_template('admin/gallery.html', unit_name=Config.UNIT_NAME or "Manipal Jnanasudha NCC Naval Sub Unit", gallery=gallery)

# ----- Data API endpoints (all must use @admin_required) -----
@app.route('/api/admin/officers', methods=['GET'])
@admin_required
def get_officers():
    data = github.get_json('data/officers.json')
    return jsonify(data)

@app.route('/api/admin/news', methods=['GET'])
@admin_required
def get_news():
    data = github.get_json('data/news.json')
    return jsonify(data)

@app.route('/api/admin/achievers', methods=['GET'])
@admin_required
def get_achievers():
    data = github.get_json('data/achievers.json')
    return jsonify(data)

@app.route('/api/admin/alumni', methods=['GET'])
@admin_required
def get_alumni():
    data = github.get_json('data/alumni.json')
    return jsonify(data)

@app.route('/api/admin/gallery', methods=['GET'])
@admin_required
def get_gallery():
    data = github.get_json('data/gallery.json')
    return jsonify(data)

@app.route('/api/admin/settings', methods=['GET'])
@admin_required
def get_settings():
    # You may store settings in a separate JSON or use Config class
    return jsonify({
        "unit_name": Config.UNIT_NAME or "Manipal Jnanasudha NCC Naval Sub Unit",
        "parent_unit": Config.PARENT_UNIT or "6 Kar Naval Unit NCC",
        "directorate": Config.DIRECTORATE or "Karnataka & Goa Directorate, NCC",
        "cadet_strength": Config.CADET_STRENGTH or 100
    })

# POST/PUT/DELETE endpoints also need @admin_required
@app.route('/api/admin/officers', methods=['POST'])
@admin_required
def add_officer():
    data = request.get_json()
    item = data.get('item')
    if not item:
        return jsonify({"error": "Missing item"}), 400
    officers = github.get_json('data/officers.json')
    officers.append(item)
    github.update_json('data/officers.json', officers, "Add officer")
    return jsonify({"success": True})

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
    all_news = load_json("news.json")
    news = []
    for n in all_news:
        if n['display']:
            news.append(n)
    print(news)
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
