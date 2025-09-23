from datetime import datetime
from django.conf import settings
from core.utils.payments import log_payment
import requests
import base64

# -------------------------------
# M-Pesa (Daraja API)
# -------------------------------

def get_timestamp():
    return datetime.now().strftime('%Y%m%d%H%M%S')

def generate_password():
    data_to_encode = settings.MPESA_SHORTCODE + settings.MPESA_PASSKEY + get_timestamp()
    return base64.b64encode(data_to_encode.encode()).decode()

def process_mpesa(order):
    auth_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(auth_url, auth=(settings.MPESA_CONSUMER_KEY, settings.MPESA_CONSUMER_SECRET))
    access_token = response.json().get('access_token')

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

    stk_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    stk_response = requests.post(stk_url, json=payload, headers=headers)

    if stk_response.status_code == 200:
        log_payment(order, 'mpesa', 'initiated', 'STK push sent')
        return "STK push sent. Please complete payment on your phone."
    else:
        log_payment(order, 'mpesa', 'failed', 'STK push failed', metadata=stk_response.json())
        return "Failed to initiate M-Pesa payment. Try again or contact support."

# -------------------------------
# Airtel Money (Temporarily Disabled)
# -------------------------------

# import africastalking
# africastalking.initialize(settings.AT_USERNAME, settings.AT_API_KEY)
# payment = africastalking.Payment

# def process_airtel(order):
#     try:
#         response = payment.mobile_checkout(
#             product_name="KiokoStore",
#             phone_number=order.user.phone_number,
#             currency_code="KES",
#             amount=int(order.total),
#             provider_channel="airtel",
#             metadata={
#                 "order_id": str(order.id),
#                 "description": "Airtel Money payment for Kioko Enterprises"
#             }
#         )
#         return "Airtel Money payment initiated. Please complete on your phone."
#     except Exception as e:
#         print("Airtel Money error:", str(e))
#         return "Failed to initiate Airtel Money payment. Try again or contact support."

# -------------------------------
# PayPal (REST API)
# -------------------------------

def get_paypal_access_token():
    url = f"{settings.PAYPAL_API_BASE}/v1/oauth2/token"
    response = requests.post(
        url,
        headers={"Accept": "application/json"},
        data={"grant_type": "client_credentials"},
        auth=(settings.PAYPAL_CLIENT_ID, settings.PAYPAL_SECRET)
    )
    response.raise_for_status()
    return response.json()["access_token"]

def process_paypal(order):
    access_token = get_paypal_access_token()
    url = f"{settings.PAYPAL_API_BASE}/v2/checkout/orders"
    payload = {
        "intent": "CAPTURE",
        "purchase_units": [{
            "amount": {
                "currency_code": "USD",
                "value": str(order.total)
            }
        }],
        "application_context": {
            "return_url": "https://yourdomain.com/paypal/callback/",
            "cancel_url": "https://yourdomain.com/paypal/cancel/"
        }
    }
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    response = requests.post(url, json=payload, headers=headers)
    response.raise_for_status()
    data = response.json()
    approval_url = next(link["href"] for link in data["links"] if link["rel"] == "approve")
    log_payment(order, 'paypal', 'initiated', 'Redirecting to PayPal', reference=data['id'], metadata=data)
    return approval_url

# -------------------------------
# Bank Transfer (Static)
# -------------------------------

def process_bank(order, lang='en'):
    if lang == 'sw':
        message = f"""
        Maelezo ya Uhamisho wa Benki kwa Order #{order.id}:

        Benki: Kioko Bank  
        Jina la Akaunti: Kioko Enterprises Ltd  
        Nambari ya Akaunti: 1234567890  
        Kiasi: KSh {order.total}  

        Rejea: Order#{order.id}  
        Tuma uthibitisho wa malipo kwa payments@kioko.co.ke au WhatsApp +254712345678.
        """.strip()
    else:
        message = f"""
        Bank Transfer Instructions for Order #{order.id}:

        Bank Name: Kioko Bank  
        Account Name: Kioko Enterprises Ltd  
        Account Number: 1234567890  
        Branch Code: 001  
        Amount: KSh {order.total}  

        Reference: Order#{order.id}  
        Please send proof of payment to payments@kioko.co.ke or WhatsApp +254712345678.
        """.strip()

    log_payment(order, 'bank', 'pending', message)
    return message

