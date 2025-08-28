from django.urls import path
from .views import (
    mpesa_callback,
    airtel_callback,
    paypal_callback,
)

urlpatterns = [
    path('mpesa/callback/', mpesa_callback, name='mpesa_callback'),
    path('airtel/callback/', airtel_callback, name='airtel_callback'),
    path('paypal/callback/', paypal_callback, name='paypal_callback'),
]
