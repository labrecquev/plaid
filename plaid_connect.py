# plaid_connect.py

import os
import datetime as dt
import json
import time
from datetime import date, timedelta
import uuid
from dotenv import load_dotenv
import plaid
import requests
from plaid.model.payment_amount import PaymentAmount
from plaid.model.payment_amount_currency import PaymentAmountCurrency
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.recipient_bacs_nullable import RecipientBACSNullable
from plaid.model.payment_initiation_address import PaymentInitiationAddress
from plaid.model.payment_initiation_recipient_create_request import PaymentInitiationRecipientCreateRequest
from plaid.model.payment_initiation_payment_create_request import PaymentInitiationPaymentCreateRequest
from plaid.model.payment_initiation_payment_get_request import PaymentInitiationPaymentGetRequest
from plaid.model.link_token_create_request_payment_initiation import LinkTokenCreateRequestPaymentInitiation
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.link_token_create_request_user import LinkTokenCreateRequestUser
from plaid.model.user_create_request import UserCreateRequest
from plaid.model.consumer_report_user_identity import ConsumerReportUserIdentity
from plaid.model.asset_report_create_request import AssetReportCreateRequest
from plaid.model.asset_report_create_request_options import AssetReportCreateRequestOptions
from plaid.model.asset_report_user import AssetReportUser
from plaid.model.asset_report_get_request import AssetReportGetRequest
from plaid.model.asset_report_pdf_get_request import AssetReportPDFGetRequest
from plaid.model.auth_get_request import AuthGetRequest
from plaid.model.transactions_sync_request import TransactionsSyncRequest
from plaid.model.identity_get_request import IdentityGetRequest
from plaid.model.investments_transactions_get_request_options import InvestmentsTransactionsGetRequestOptions
from plaid.model.investments_transactions_get_request import InvestmentsTransactionsGetRequest
from plaid.model.accounts_balance_get_request import AccountsBalanceGetRequest
from plaid.model.accounts_get_request import AccountsGetRequest
from plaid.model.investments_holdings_get_request import InvestmentsHoldingsGetRequest
from plaid.model.item_get_request import ItemGetRequest
from plaid.model.institutions_get_by_id_request import InstitutionsGetByIdRequest
from plaid.model.transfer_authorization_create_request import TransferAuthorizationCreateRequest
from plaid.model.transfer_create_request import TransferCreateRequest
from plaid.model.transfer_get_request import TransferGetRequest
from plaid.model.transfer_network import TransferNetwork
from plaid.model.transfer_type import TransferType
from plaid.model.transfer_authorization_user_in_request import TransferAuthorizationUserInRequest
from plaid.model.ach_class import ACHClass
from plaid.model.transfer_create_idempotency_key import TransferCreateIdempotencyKey
from plaid.model.transfer_user_address_in_request import TransferUserAddressInRequest
from plaid.model.signal_evaluate_request import SignalEvaluateRequest
from plaid.model.statements_list_request import StatementsListRequest
from plaid.model.link_token_create_request_statements import LinkTokenCreateRequestStatements
from plaid.model.link_token_create_request_cra_options import LinkTokenCreateRequestCraOptions
from plaid.model.statements_download_request import StatementsDownloadRequest
from plaid.model.consumer_report_permissible_purpose import ConsumerReportPermissiblePurpose
from plaid.model.cra_check_report_base_report_get_request import CraCheckReportBaseReportGetRequest
from plaid.model.cra_check_report_pdf_get_request import CraCheckReportPDFGetRequest
from plaid.model.cra_check_report_income_insights_get_request import CraCheckReportIncomeInsightsGetRequest
from plaid.model.cra_check_report_partner_insights_get_request import CraCheckReportPartnerInsightsGetRequest
from plaid.model.cra_pdf_add_ons import CraPDFAddOns
from plaid.api import plaid_api

load_dotenv()

def create_link_token():
    """Generate a link token to initialize Plaid Link."""
    url = f"https://{os.getenv('PLAID_ENV')}.plaid.com/link/token/create"
    
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "client_id": os.getenv("PLAID_CLIENT_ID"),
        "secret": os.getenv("PLAID_SECRET"),
        "user": {
            "client_user_id": "unique_user_id"
        },
        "client_name": "labrecquev",
        "products": [os.getenv("PLAID_PRODUCTS")],
        "country_codes": [os.getenv("PLAID_COUNTRY_CODES")],
        "language": "en"
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(body))
        if response.status_code == 200:
            link_token = response.json()["link_token"]
            print("Link Token:", link_token)
            return link_token
        else:
            print("Error creating link token:", response.json())
            return None
    except Exception as e:
        print("Exception occurred while creating link token:", str(e))
        return None

def exchange_public_token(public_token):
    """Exchange the public token for an access token."""
    url = f"https://{os.getenv('PLAID_ENV')}.plaid.com/item/public_token/exchange"
    headers = {
        "Content-Type": "application/json"
    }
    body = {
        "client_id": os.getenv("PLAID_CLIENT_ID"),
        "secret": os.getenv("PLAID_SECRET"),
        "public_token": public_token
    }

    try:
        response = requests.post(url, headers=headers, data=json.dumps(body))
        if response.status_code == 200:
            exchange_response = response.json()
            access_token = exchange_response.get("access_token")
            print("Access Token:", access_token)

            # Save access token to .env file
            with open(".env", "a") as f:
                f.write(f"\nPLAID_ACCESS_TOKEN={access_token}")

            print("Access token saved to .env file.")
            return access_token
        else:
            print("Error exchanging public token:", response.json())
            return None
    except Exception as e:
        print("Exception occurred while exchanging public token:", str(e))
        return None

if __name__ == "__main__":
    # Step 1: Create a Link Token
    link_token = create_link_token()

    # Step 2: Use the link token in your frontend to connect your account
    print(f"Open the following link in your browser to connect your bank account:")
    print(f"https://sandbox.plaid.com/link?token={link_token}")

    # Step 3: Get the public token from your frontend after linking
    public_token = input("\nEnter the public token obtained after linking your account: ")

    # Step 4: Exchange the public token for an access token
    exchange_public_token(public_token)