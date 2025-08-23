import requests
import base64
from datetime import datetime
from django.conf import settings

def get_timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')

def generate_password():
    data_to_encode = settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + get_timestamp()
    return base64.b64encode(data_to_encode.encode()).decode()

def process_mpesa(order):
    # Step 1: Get access token
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(auth_url, auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
    access_token = response.json().get('access_token')

    # Step 2: Prepare payment payload
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "BusinessShortCode": settings.MPESA_SHORTCODE,
        "Password": generate_password(),
        "Timestamp": get_timestamp(),
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(order.total),
        "PartyA": order.user.phone_number,
        "PartyB": settings.MPESA_SHORTCODE,
        "PhoneNumber": order.user.phone_number,
        "CallBackURL": settings.MPESA_CALLBACK_URL,
        "AccountReference": f"Order{order.id}",
        "TransactionDesc": "Payment for order"
    }

    # Step 3: Send STK Push
    stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    stk_response = requests.post(stk_url, json=payload, headers=headers)

    if stk_response.status_code == 200:
        return "STK push sent. Please complete payment on your phone."
    else:
        return "Failed to initiate M-Pesa payment. Try again or contact support."

def process_airtel(order):
    return f"Simulated Airtel Money payment for Order #{order.id}"

def process_paypal(order):
    return f"Redirect to PayPal for Order #{order.id}"

def process_bank(order):
    return f"Bank transfer instructions for Order #{order.id}"
