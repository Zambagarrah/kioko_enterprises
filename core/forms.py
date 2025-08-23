from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, Order


class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['email', 'date_of_birth', 'password1', 'password2']


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['shipping_address', 'payment_method']