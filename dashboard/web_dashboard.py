import json
import os
import sys

from flask import Flask, jsonify, render_template, request

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from browser_statistics import get_summary, stats
from notification_manager import get_notifications

CONFIG_FILE = os.path.join(PROJECT_ROOT, "config.json")

app = Flask(__name__, template_folder="templates", static_folder="static")


DEFAULT_SETTINGS = {
    "browser_count": 2,
    "url": "https://example.com",
    "refresh_interval": 5,
    "auto_refresh": True,
}


def load_settings():
    if os.path.exists(CONFIG_FILE):
        try:
            with open(CONFIG_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return DEFAULT_SETTINGS.copy()


def save_settings(data):
    settings = DEFAULT_SETTINGS.copy()
    settings.update(data)

    with open(CONFIG_FILE, "w", encoding="utf-8") as f:
        json.dump(settings, f, indent=4)

    return settings


@app.route("/")
def dashboard():
    return render_template(
        "index.html",
        stats=stats,
        summary=get_summary(),
    )


@app.route("/api/stats")
def api_stats():
    return jsonify({
        "summary": get_summary(),
        "stats": stats,
    })


@app.route("/api/settings", methods=["GET"])
def get_settings():
    return jsonify(load_settings())


@app.route("/api/settings", methods=["POST"])
def update_settings():
    data = request.get_json(force=True)
    settings = save_settings(data)
    return jsonify({
        "success": True,
        "settings": settings,
    })



@app.route("/api/notifications")
def api_notifications():
    return jsonify({
        "notifications": get_notifications()
    })

@app.route("/health")
def health():
    return jsonify({
        "status": "ok",
        "dashboard": "running",
    })


def start_dashboard():
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        threaded=True,
        use_reloader=False,
    )


if __name__ == "__main__":
    start_dashboard()
