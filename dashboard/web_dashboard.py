
from flask import Flask, render_template, jsonify
import sys
import os
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from browser_statistics import stats, get_summary
app = Flask(__name__, template_folder="templates", static_folder="static")

@app.route("/")
def dashboard():
    return render_template("index.html", stats=stats, summary=get_summary())

@app.route("/api/stats")
def api_stats():
    return jsonify({"summary": get_summary(), "stats": stats})

@app.route("/health")
def health():
    return {"status":"ok"}

def start_dashboard():
    app.run(host="127.0.0.1", port=5000, debug=False, threaded=True, use_reloader=False)

if __name__=="__main__":
    start_dashboard()
