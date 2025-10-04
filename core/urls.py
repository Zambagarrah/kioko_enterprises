from django.urls import path
from .views import (
    mpesa_callback,
    airtel_callback,
    paypal_callback,
    upload_bank_proof,
    printable_receipt,
    update_order_status,
    order_history,
    request_order_support,
    edit_profile,
    staff_orders,
    verify_payments,
    update_delivery_status,
)

urlpatterns = [
    path('mpesa/callback/', mpesa_callback, name='mpesa_callback'),
    path('airtel/callback/', airtel_callback, name='airtel_callback'),
    path('paypal/callback/', paypal_callback, name='paypal_callback'),
    path('upload-proof/<int:order_id>/', upload_bank_proof, name='upload_bank_proof'),
    path('receipt/<int:order_id>/', printable_receipt, name='printable_receipt'),
    path('staff/update-status/<int:order_id>/', update_order_status, name='update_order_status'),
    path('my-orders/', order_history, name='order_history'),
    path('support-request/<int:order_id>/', request_order_support, name='request_order_support'),
    path('profile/edit/', edit_profile, name='edit_profile'),
    path('staff/orders/', staff_orders, name='staff_orders'),
    path('staff/verify-payments/', verify_payments, name='verify_payments'),
    path('staff/update-delivery/<int:order_id>/', update_delivery_status, name='update_delivery_status'),
]
