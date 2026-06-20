from flask import Flask, request
import datetime
import requests

app = Flask(__name__)

def get_location(ip):
    try:
        # Skip location lookup for localhost
        if ip == "127.0.0.1" or ip.startswith("192.168") or ip.startswith("10."):
            return {
                "country": "Local Network",
                "region": "N/A",
                "city": "N/A",
                "isp": "N/A",
                "lat": "N/A",
                "lon": "N/A"
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
    return {
        "country": "Unknown", "region": "Unknown",
        "city": "Unknown", "isp": "Unknown",
        "lat": "N/A", "lon": "N/A"
    }

def detect_system(user_agent):
    ua = user_agent.lower()

    # OS detection
    if "windows" in ua:
        os_name = "Windows"
    elif "android" in ua:
        os_name = "Android"
    elif "iphone" in ua or "ios" in ua:
        os_name = "iPhone (iOS)"
    elif "mac" in ua:
        os_name = "MacOS"
    else:
        os_name = "Unknown"

    # Browser detection
    if "chrome" in ua and "edg" not in ua:
        browser = "Google Chrome"
    elif "edg" in ua:
        browser = "Microsoft Edge"
    elif "firefox" in ua:
        browser = "Mozilla Firefox"
    elif "safari" in ua and "chrome" not in ua:
        browser = "Safari"
    else:
        browser = "Unknown"

    return os_name, browser


@app.route('/')
def home():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent', 'Unknown')  # FIX: default if missing

    os_name, browser = detect_system(user_agent)
    location = get_location(ip)

    now = datetime.datetime.now()

    with open("visitors.txt", "a", encoding="utf-8") as f:
        f.write(f"\nTime: {now}")
        f.write(f"\nIP Address: {ip}")
        f.write(f"\nCountry: {location['country']}")
        f.write(f"\nRegion: {location['region']}")
        f.write(f"\nCity: {location['city']}")
        f.write(f"\nISP: {location['isp']}")
        f.write(f"\nCoordinates: {location['lat']}, {location['lon']}")
        f.write(f"\nOperating System: {os_name}")
        f.write(f"\nBrowser: {browser}")
        f.write(f"\nFull Device Info: {user_agent}")
        f.write("\n-------------------------\n")

    return """
    <html>
    <head>
        <title>Welcome</title>
        <style>
            body{
                background-color:black;
                color:white;
                text-align:center;
                font-family:Arial;
            }
            img{
                width:300px;
                margin-top:80px;
                border-radius:15px;
                box-shadow:0px 0px 25px cyan;
            }
        </style>
    </head>
    <body>
        <h1>Welcome 👋</h1>
        <p>Hello Welcome to my first website</p>
        <img src="https://img.freepik.com/free-vector/word-hello-typography-vector_53876-85344.jpg?semt=ais_user_personalization&w=740&q=80">
    </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)  # FIX: accessible on network
