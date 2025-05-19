import os
import json
import requests
from dotenv import load_dotenv
from datetime import datetime, timedelta

# Load environment variables from .env file
load_dotenv()

def get_transactions():
    try:
        # Define the API URL
        env = os.getenv('PLAID_ENV')
        if env == 'sandbox':
            url = "https://sandbox.plaid.com/transactions/get"
        elif env == 'development':
            url = "https://development.plaid.com/transactions/get"
        elif env == 'production':
            url = "https://production.plaid.com/transactions/get"
        else:
            raise ValueError("Invalid environment specified.")
        
        # Calculate dates (last 30 days)
        end_date = datetime.today().strftime('%Y-%m-%d')
        start_date = (datetime.today() - timedelta(days=30)).strftime('%Y-%m-%d')

        # Define the headers and body
        headers = {"Content-Type": "application/json"}
        body = {
            "client_id": os.getenv("PLAID_CLIENT_ID"),
            "secret": os.getenv("PLAID_SECRET"),
            "access_token": os.getenv("PLAID_ACCESS_TOKEN"),
            "start_date": start_date,
            "end_date": end_date,
            "options": {
                "count": 100,  # Adjust the number of transactions to fetch
                "offset": 0    # For pagination
            }
        }

        # Make the API request
        response = requests.post(url, headers=headers, data=json.dumps(body))

        # Check the response status
        if response.status_code == 200:
            data = response.json()
            transactions = data.get("transactions", [])
            print(f"Retrieved {len(transactions)} transactions from {start_date} to {end_date}.\n")

            # Print transactions
            for txn in transactions:
                print(f"{txn['date']} - {txn['name']} - ${txn['amount']}")
            return transactions
        else:
            # Print error response
            print("Error:", response.json())
            return None

    except Exception as e:
        print("Exception occurred while retrieving transactions:", str(e))
        return None

if __name__ == "__main__":
    get_transactions()
