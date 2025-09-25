from allauth.account.adapter import DefaultAccountAdapter

class CustomAccountAdapter(DefaultAccountAdapter):
    def save_user(self, request, user, form, commit=True):
        user = super().save_user(request, user, form, commit=False)
        user.date_of_birth = form.cleaned_data.get('date_of_birth')
        if commit:
            user.save()
        return user
