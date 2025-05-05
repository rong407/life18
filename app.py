# app.py
from flask import Flask, request, redirect, render_template
import requests

app = Flask(__name__)

CLIENT_ID = "1651234567"
CLIENT_SECRET = "abc123456xyz"
REDIRECT_URI = "https://yourdomain.com/callback"

@app.route("/callback")
def callback():
    code = request.args.get("code")

    # 1. Request access token
    token_url = "https://api.line.me/oauth2/v2.1/token"
    headers = {'Content-Type': 'application/x-www-form-urlencoded'}
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI,
        "client_id": CLIENT_ID,
        "client_secret": CLIENT_SECRET
    }

    res = requests.post(token_url, headers=headers, data=data).json()
    access_token = res.get("access_token")

    # 2. Get user profile
    profile_url = "https://api.line.me/v2/profile"
    headers = {"Authorization": f"Bearer {access_token}"}
    profile = requests.get(profile_url, headers=headers).json()

    return render_template("register.html", name=profile["displayName"], userId=profile["userId"])

# หน้าแรก
@app.route("/")
def index():
    return render_template("login.html")
