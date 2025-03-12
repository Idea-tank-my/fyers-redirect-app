import os
print("FYERS_CLIENT_ID:", os.environ.get("FYERS_CLIENT_ID"))
print("FYERS_CLIENT_SECRET:", os.environ.get("FYERS_CLIENT_SECRET"))
from flask import Flask, request

app = Flask(__name__)

@app.route('/callback')
def callback():
    code = request.args.get('code')  # Get the authorization code
    return f"Authorization code: {code}", 200

if __name__ == '__main__':
    app.run(debug=True)