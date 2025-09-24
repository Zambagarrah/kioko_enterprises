from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from allauth.account.forms import SignupForm
from .models import (
    User,
    Order,
    BankPaymentProof,
)


class CustomUserCreationForm(UserCreationForm):
    phone_number = PhoneNumberField(region='KE')
    class Meta:
        model = User
        fields = ['email','phone_number', 'date_of_birth', 'password1', 'password2']
        


# class CustomSignupForm(SignupForm):
#     date_of_birth = forms.DateField(
#         required=True,
#         widget=forms.DateInput(attrs={'type': 'date'})
#     )

#     def save(self, request):
#         user = super().save(request)
#         user.date_of_birth = self.cleaned_data['date_of_birth']
#         user.save()
#         return user

class CustomSignupForm(SignupForm):
    date_of_birth = forms.DateField(
        required=True,
        widget=forms.DateInput(attrs={'type': 'date'})
    )


class CheckoutForm(forms.ModelForm):
    PAYMENT_CHOICES = [
        ('mpesa', 'M-Pesa'),
        ('airtel', 'Airtel Money'),
        ('paypal', 'PayPal'),
        ('bank', 'Bank Transfer'),
    ]

    payment_method = forms.ChoiceField(choices=PAYMENT_CHOICES)

    class Meta:
        model = Order
        fields = ['shipping_address', 'payment_method']
        
class BankPaymentProofForm(forms.ModelForm):
    class Meta:
        model = BankPaymentProof
        fields = ['proof_file', 'notes']
        
class OrderFilterForm(forms.Form):
    status = forms.ChoiceField(
        choices=[('', 'All')] + Order.STATUS_CHOICES,
        required=False
    )
    start_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    product_name = forms.CharField(required=False)

