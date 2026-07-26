from flask import Flask
import sys
import os

# Project root-ஐ Python path-ல் add பண்ணு
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from browser_statistics import stats

app = Flask(__name__)


@app.route("/")
def home():
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>BrowserManager Dashboard</title>

        <meta http-equiv="refresh" content="3">

        <style>
            body{
                background:#f5f5f5;
                font-family:Arial;
                margin:30px;
            }

            h1{
                color:#333;
            }

            .card{
                background:white;
                border-radius:10px;
                padding:20px;
                margin-bottom:20px;
                box-shadow:0 2px 10px rgba(0,0,0,.15);
            }

            table{
                width:100%;
                border-collapse:collapse;
            }

            td{
                padding:6px;
                border-bottom:1px solid #eee;
            }

            .healthy{
                color:green;
                font-weight:bold;
            }
        </style>

    </head>

    <body>

    <h1>🚀 BrowserManager Web Dashboard</h1>
    <hr>
    """

    if not stats:
        html += """
        <div class="card">
            <h3>No browsers are running.</h3>
            <p>Start BrowserManager first.</p>
        </div>
        """
    else:

        for worker_id, data in stats.items():

            html += f"""
            <div class="card">

            <h2>🟢 Browser {worker_id}</h2>

            <table>

            <tr><td>Status</td><td>{data.get('status','-')}</td></tr>

            <tr><td>Health</td><td class="healthy">{data.get('health','-')}</td></tr>

            <tr><td>URL</td><td>{data.get('url','-')}</td></tr>

            <tr><td>Title</td><td>{data.get('title','-')}</td></tr>

            <tr><td>Profile</td><td>{data.get('profile','-')}</td></tr>

            <tr><td>Browser</td><td>{data.get('browser_version','-')}</td></tr>

            <tr><td>RAM</td><td>{data.get('ram','-')}</td></tr>

            <tr><td>CPU</td><td>{data.get('cpu','-')}</td></tr>

            <tr><td>Load Time</td><td>{data.get('load_time','-')}</td></tr>

            <tr><td>PID</td><td>{data.get('pid','-')}</td></tr>

            <tr><td>Started At</td><td>{data.get('started_at','-')}</td></tr>

            </table>

            </div>
            """

    html += """
    </body>
    </html>
    """

    return html


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)