from django.core.mail import send_mail

def send_order_email(user, order):
    subject = f"Order #{order.id} Confirmation"
    message = f"Dear {user.username}, your order has been received.\nTotal: KSh {order.total}\nPayment Method: {order.payment_method}"
    send_mail(subject, message, 'noreply@kioko.co.ke', [user.email])
