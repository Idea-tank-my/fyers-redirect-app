from flask import Flask, request

app = Flask(__name__)

@app.route('/callback')
def callback():
    code = request.args.get('code')  # Get the authorization code
    return f"Authorization code: {code}", 200

if __name__ == '__main__':
    app.run(debug=True)