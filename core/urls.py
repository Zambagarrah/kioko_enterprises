from django.urls import path
from .views import (
    mpesa_callback,
    airtel_callback,
    paypal_callback,
    upload_bank_proof,
)

urlpatterns = [
    path('mpesa/callback/', mpesa_callback, name='mpesa_callback'),
    path('airtel/callback/', airtel_callback, name='airtel_callback'),
    path('paypal/callback/', paypal_callback, name='paypal_callback'),
    path('upload-proof/<int:order_id>/', upload_bank_proof, name='upload_bank_proof'),
]
