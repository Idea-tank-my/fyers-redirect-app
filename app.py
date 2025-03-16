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
    code = request.args.get('code')  # Get the authorization code
    return f"Authorization code: {code}", 200

if __name__ == '__main__':
    app.run(debug=True)