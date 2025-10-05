def send_sms_confirmation(phone_number, message):
    # Placeholder for SMS API integration
    print(f"SMS to {phone_number}: {message}")
    
def send_delivery_sms(user, order):
    message = f"Hello {user.email}, your order #{order.id} has been shipped. Delivery to: {order.delivery_location}."
    send_sms(user.phone_number, message)
    
def send_sms(phone_number, message):
    # Placeholder for SMS API integration
    print(f"Sending SMS to {phone_number}: {message}")
