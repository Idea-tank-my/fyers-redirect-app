import requests
import urllib.parse
from flask import Flask, request
import os
client_id = os.environ.get("FYERS_CLIENT_ID")

redirect_uri = "https://fyers-redirect-app.onrender.com/callback"  # Replace with your actual redirect URI
response_type = "code"
state = "your_state_value"  # You can use any string here

base_url = "https://api.fyers.in/api/v2/generate-authcode"
query_params = {
    "client_id": client_id,
    "redirect_uri": redirect_uri,
    "response_type": response_type,
    "state": state
}
auth_url = f"{base_url}?{urllib.parse.urlencode(query_params)}"

app = Flask(__name__)

@app.route('/login')
def login():
    return auth_url

@app.route('/callback')
def callback():
    code = request.args.get('code')
    if not code:
        return "Authorization code not provided.", 400

    token_url = "https://api.fyers.in/api/v2/generate-token"
    data = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "code": code,
        "redirect_uri": redirect_uri,
        "client_secret": os.environ.get("FYERS_CLIENT_SECRET")
    }
    try:
        response = requests.post(token_url, data=data)
        response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
        token_data = response.json()
        access_token = token_data.get("access_token")

        if access_token:
            return f"Access Token: {access_token}", 200
        else:
            return "Access token not found in response.", 500

    except requests.exceptions.RequestException as e:
        return f"Error exchanging code for token: {e}", 500

if __name__ == '__main__':
    app.run(debug=True)