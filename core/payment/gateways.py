from datetime import datetime
from django.conf import settings
import requests
import base64
import africastalking

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

africastalking.initialize(settings.AT_USERNAME, settings.AT_API_KEY)
mobile = africastalking.SMS  # There was nothing like .MobilePayment it was either USSD or SMS or Airtime or Voice or Application

def process_airtel(order):
    try:
        response = mobile.checkout(
            product_name="KiokoStore",  # Must match your AT product
            phone_number=order.user.phone_number,
            currency_code="KES",
            amount=int(order.total),
            metadata={
                "order_id": str(order.id),
                "description": "Airtel Money payment for Kioko Enterprises"
            }
        )
        return "Airtel Money payment initiated. Please complete on your phone."
    except Exception as e:
        print("Airtel Money error:", str(e))
        return "Failed to initiate Airtel Money payment. Try again or contact support."
def process_paypal(order):
    return f"Redirect to PayPal for Order #{order.id}"

def process_bank(order):
    return f"Bank transfer instructions for Order #{order.id}"
