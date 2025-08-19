from django.shortcuts import render, redirect
from .forms import CustomUserCreationForm

def register(request):
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        if user.is_of_age():
            user.save()
            return redirect('login')
        else:
            form.add_error('date_of_birth', 'You must be at least 18 years old to register.')
    return render(request, 'core/register.html', {'form': form})
