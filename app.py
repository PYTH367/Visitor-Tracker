from flask import Flask, request
import datetime

app = Flask(__name__)

def detect_system(user_agent):
    ua = user_agent.lower()

    # OS detection
    if "windows" in ua:
        os = "Windows"
    elif "android" in ua:
        os = "Android"
    elif "iphone" in ua or "ios" in ua:
        os = "iPhone (iOS)"
    elif "mac" in ua:
        os = "MacOS"
    else:
        os = "Unknown"

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

    return os, browser


@app.route('/')
def home():
    ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')

    os, browser = detect_system(user_agent)

    time = datetime.datetime.now()

    with open("visitors.txt", "a", encoding="utf-8") as f:
        f.write(f"\nTime: {time}")
        f.write(f"\nIP Address: {ip}")
        f.write(f"\nOperating System: {os}")
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
    app.run()