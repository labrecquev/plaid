from flask import Flask, jsonify
from flask_cors import CORS  # Import the CORS package
from plaid_config import client  # Use your existing plaid_config.py

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/get_link_token', methods=['GET'])
def get_link_token():
    try:
        response = client.link_token_create({
            'user': {'client_user_id': 'user-id'},
            'client_name': 'My Finance App',
            'products': ['transactions'],
            'country_codes': ['CA'],
            'language': 'en',
        })
        return jsonify({'link_token': response['link_token']})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(port=5000, debug=True)