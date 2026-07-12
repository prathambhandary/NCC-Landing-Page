import json
from pathlib import Path
from flask import Flask, render_template, jsonify, request

app = Flask(__name__)

DATA_DIR = Path(__file__).parent / "data"

def load_json(filename):
    with open(DATA_DIR / filename, encoding="utf-8") as f:
        return json.load(f)

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
# JSON API used by the gallery page's calendar filter
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