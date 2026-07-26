from flask import Flask, render_template
import sys
import os

# ---------------------------------
# Project Root
# ---------------------------------
PROJECT_ROOT = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..")
)

if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

# ---------------------------------
# Import Live Statistics
# ---------------------------------
from browser_statistics import stats

# ---------------------------------
# Flask App
# ---------------------------------
app = Flask(
    __name__,
    template_folder="templates",
    static_folder="static"
)

# ---------------------------------
# Dashboard
# ---------------------------------
@app.route("/")
def dashboard():
    return render_template(
        "index.html",
        stats=stats
    )

# ---------------------------------
# Start Flask
# ---------------------------------
def start_dashboard():
    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False,
        use_reloader=False
    )

# ---------------------------------
# Run Directly
# ---------------------------------
if __name__ == "__main__":
    start_dashboard()