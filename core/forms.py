from django import forms
from django.contrib.auth.forms import UserCreationForm
from phonenumber_field.formfields import PhoneNumberField
from allauth.account.forms import SignupForm
from .models import (
    User,
    Order,
    BankPaymentProof,
    ROLE_CHOICES,
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
    start_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    end_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'}))
    product_name = forms.CharField(required=False)

User = get_user_model()

class ProfileEditForm(forms.ModelForm):
    phone_number = PhoneNumberField(required=True)
    date_of_birth = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'phone_number', 'date_of_birth']

    def clean_date_of_birth(self):
        dob = self.cleaned_data['date_of_birth']
        today = date.today()
        age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
        if age < 18:
            raise forms.ValidationError("You must be at least 18 years old.")
        return dob
    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.exclude(pk=self.instance.pk).filter(email=email).exists():
            raise forms.ValidationError("This email address is already in use.")
        return email
