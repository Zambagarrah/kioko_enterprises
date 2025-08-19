from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import CustomUserCreationForm
from .models import Product, Category


def register(request):
    form = CustomUserCreationForm(request.POST or None)
    if form.is_valid():
        user = form.save(commit=False)
        if user.is_of_age():
            user.save()
            return redirect('login')
        else:
            form.add_error('date_of_birth',
                           'You must be at least 18 years old to register.')
    return render(request, 'core/register.html', {'form': form})


def product_list(request):
    query = request.GET.get('q')
    products = Product.objects.all()

    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(brand__icontains=query) |
            Q(category__name__icontains=query)
        )

    return render(request, 'core/product_list.html', {'products': products})


def product_detail(request, pk):
    product = get_object_or_404(Product, pk=pk)
    return render(request, 'core/product_detail.html', {'product': product})
