import os
import hashlib
import requests
from flask import Flask, request

app = Flask(__name__)

client_id = os.environ.get("FYERS_CLIENT_ID")
secret_key = os.environ.get("FYERS_CLIENT_SECRET")
redirect_uri = "https://fyers-redirect-app.onrender.com/callback"

def generate_app_id_hash(client_id, secret_key):
    app_id_secret = f"{client_id}:{secret_key}"
    app_id_hash = hashlib.sha256(app_id_secret.encode()).hexdigest()
    return app_id_hash

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Authorization code not provided.", 400

    app_id_hash = generate_app_id_hash(client_id, secret_key)

    token_url = "https://api-t1.fyers.in/api/v3/validate-authcode"
    payload = {
        "grant_type": "authorization_code",
        "appIdHash": app_id_hash,
        "code": code
    }

    response = requests.post(token_url, json=payload)

    if response.status_code == 200:
        access_token = response.json().get("access_token")
        return f"Access Token: {access_token}", 200
    else:
        return f"Error exchanging code for token: {response.status_code} {response.text}", 500

@app.route('/login')
def login():
    auth_url = f"https://api-t1.fyers.in/api/v3/generate-authcode?client_id={client_id}&redirect_uri={redirect_uri}&response_type=code&state=your_state_value"
    return f'<a href="{auth_url}">Login to Fyers</a>'

if __name__ == '__main__':
    app.run(debug=True)