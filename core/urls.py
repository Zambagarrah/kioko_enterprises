from django.urls import path
from .views import (
    mpesa_callback,
    airtel_callback,
)

urlpatterns = [
    path('mpesa/callback/', mpesa_callback, name='mpesa_callback'),
    path('airtel/callback/', airtel_callback, name='airtel_callback')
    path('paypal/callback/', views.paypal_callback, name='paypal_callback'),
]
