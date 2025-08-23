def get_confirmation_message(method, order_id):
    messages = {
        'mpesa': f"STK push sent for Order #{order_id}. Please complete payment on your phone.",
        'airtel': f"Airtel Money payment initiated for Order #{order_id}. Please check your phone.",
        'paypal': f"Redirecting to PayPal for Order #{order_id}.",
        'bank': f"Bank transfer instructions generated for Order #{order_id}.",
    }
    return messages.get(method, "Payment method not recognized.")
