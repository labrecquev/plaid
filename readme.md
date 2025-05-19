## 2025-05-18
To make a connection work, I had to:

In plaid_connect.py:
1. create_link_token()
2. run the python server
3. open the plaid_link.html file in browser
4. click the button to obtain the public_token
5. exchange_public_token(public_token)

With the public token, I could then obtain the access_token. It worked for sandbox.
With the access_token, I was able to make a test call on test data and retrieve dummy transactions.

I am now awaiting for the limited production access. I think it's called "development" env.

---