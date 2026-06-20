from flask import Flask, request
from werkzeug.middleware.proxy_fix import ProxyFix
import datetime
from zoneinfo import ZoneInfo
import requests
import json
import os

app = Flask(__name__)
app.wsgi_app = ProxyFix(app.wsgi_app, x_for=1, x_proto=1)

# ⚠️ Change this to your own secret password!
SECRET_KEY = "chiku123"  # change this

VISITORS_FILE = "visitors.json"

def get_location(ip):
    try:
        if ip == "127.0.0.1" or ip.startswith("192.168"):
            return {
                "country": "Local Network", "region": "N/A",
                "city": "N/A", "isp": "N/A", "lat": "N/A", "lon": "N/A"
            }
        response = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
        data = response.json()
        if data["status"] == "success":
            return {
                "country": data.get("country", "Unknown"),
                "region": data.get("regionName", "Unknown"),
                "city": data.get("city", "Unknown"),
                "isp": data.get("isp", "Unknown"),
                "lat": data.get("lat", "N/A"),
                "lon": data.get("lon", "N/A")
            }
    except Exception:
        pass
    return {"country": "Unknown", "region": "Unknown", "city": "Unknown",
            "isp": "Unknown", "lat": "N/A", "lon": "N/A"}

def detect_system(user_agent):
    ua = user_agent.lower()
    if "windows" in ua: os_name = "Windows"
    elif "android" in ua: os_name = "Android"
    elif "iphone" in ua or "ios" in ua: os_name = "iPhone (iOS)"
    elif "mac" in ua: os_name = "MacOS"
    else: os_name = "Unknown"

    if "chrome" in ua and "edg" not in ua: browser = "Google Chrome"
    elif "edg" in ua: browser = "Microsoft Edge"
    elif "firefox" in ua: browser = "Mozilla Firefox"
    elif "safari" in ua and "chrome" not in ua: browser = "Safari"
    else: browser = "Unknown"

    return os_name, browser

def save_visitor(visitor):
    visitors = []
    if os.path.exists(VISITORS_FILE):
        try:
            with open(VISITORS_FILE, "r") as f:
                visitors = json.load(f)
        except:
            visitors = []
    visitors.append(visitor)
    with open(VISITORS_FILE, "w") as f:
        json.dump(visitors, f, indent=2, default=str)

def load_visitors():
    if os.path.exists(VISITORS_FILE):
        try:
            with open(VISITORS_FILE, "r") as f:
                return json.load(f)
        except:
            return []
    return []


@app.route('/')
def home():
    ip = request.headers.get("X-Forwarded-For", request.remote_addr).split(",")[0].strip()
    user_agent = request.headers.get('User-Agent', 'Unknown')
    os_name, browser = detect_system(user_agent)
    location = get_location(ip)
    now = datetime.datetime.now(ZoneInfo("Asia/Kolkata"))

    visitor = {
        "time": str(now),
        "ip": ip,
        "country": location['country'],
        "region": location['region'],
        "city": location['city'],
        "isp": location['isp'],
        "coordinates": f"{location['lat']}, {location['lon']}",
        "os": os_name,
        "browser": browser,
        "user_agent": user_agent
    }
    save_visitor(visitor)

    return """
    <html>
    <head>
        <title>Welcome</title>
        <style>
            body{ background-color:black; color:white; text-align:center; font-family:Arial; }
            img{ width:300px; margin-top:80px; border-radius:15px; box-shadow:0px 0px 25px cyan; }
        </style>
    </head>
    <body>
        <h1>Welcome 👋</h1>
        <p>Hello Welcome to my first website</p>
        <img src="https://img.freepik.com/free-vector/word-hello-typography-vector_53876-85344.jpg?semt=ais_user_personalization&w=740&q=80">
    </body>
    </html>
    """

@app.route('/logs')
def logs():
    key = request.args.get('key', '')
    if key != SECRET_KEY:
        return "<h1 style='color:red;text-align:center;margin-top:100px;font-family:Arial'>403 - Access Denied ❌</h1>", 403

    visitors = load_visitors()
    visitors_reversed = list(reversed(visitors))

    rows = ""
    for i, v in enumerate(visitors_reversed, 1):
        rows += f"""
        <tr>
            <td>{i}</td>
            <td>{v.get('time', 'N/A')[:19]}</td>
            <td>{v.get('ip', 'N/A')}</td>
            <td>🌍 {v.get('country', 'N/A')}</td>
            <td>{v.get('region', 'N/A')}</td>
            <td>{v.get('city', 'N/A')}</td>
            <td>{v.get('isp', 'N/A')}</td>
            <td>{v.get('os', 'N/A')}</td>
            <td>{v.get('browser', 'N/A')}</td>
            <td>{v.get('coordinates', 'N/A')}</td>
        </tr>
        """

    return f"""
    <html>
    <head>
        <title>Visitor Logs 👁️</title>
        <style>
            * {{ box-sizing: border-box; margin: 0; padding: 0; }}
            body {{ background: #0a0a0a; color: #fff; font-family: Arial; padding: 20px; }}
            h1 {{ text-align: center; color: cyan; margin: 20px 0 10px; font-size: 28px; }}
            p.count {{ text-align: center; color: #aaa; margin-bottom: 20px; }}
            .table-wrap {{ overflow-x: auto; }}
            table {{ width: 100%; border-collapse: collapse; font-size: 13px; }}
            th {{ background: #1a1a2e; color: cyan; padding: 12px 10px; text-align: left; position: sticky; top: 0; }}
            td {{ padding: 10px; border-bottom: 1px solid #222; vertical-align: top; }}
            tr:hover {{ background: #111; }}
            tr:nth-child(even) {{ background: #0d0d0d; }}
            .badge {{ background: #16213e; padding: 3px 8px; border-radius: 10px; font-size: 11px; }}
        </style>
    </head>
    <body>
        <h1>👁️ Visitor Logs</h1>
        <p class="count">Total Visitors: <strong style="color:cyan">{len(visitors)}</strong></p>
        <div class="table-wrap">
        <table>
            <thead>
                <tr>
                    <th>#</th>
                    <th>🕐 Time</th>
                    <th>🌐 IP</th>
                    <th>🌍 Country</th>
                    <th>📍 Region</th>
                    <th>🏙️ City</th>
                    <th>📡 ISP</th>
                    <th>💻 OS</th>
                    <th>🌏 Browser</th>
                    <th>📌 Coordinates</th>
                </tr>
            </thead>
            <tbody>
                {rows if rows else '<tr><td colspan="10" style="text-align:center;padding:40px;color:#555">No visitors yet...</td></tr>'}
            </tbody>
        </table>
        </div>
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
