def process_mpesa(order):
    # Placeholder for Daraja API integration
    return f"Simulated M-Pesa payment for Order #{order.id}"

def process_airtel(order):
    return f"Simulated Airtel Money payment for Order #{order.id}"

def process_paypal(order):
    return f"Redirect to PayPal for Order #{order.id}"

def process_bank(order):
    return f"Bank transfer instructions for Order #{order.id}"
