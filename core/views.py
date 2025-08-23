from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from .forms import CustomUserCreationForm
from .models import Product, Category, CartItem
from .utils import get_or_create_cart


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


def add_to_cart(request, product_id):
    cart = get_or_create_cart(request)
    product = Product.objects.get(id=product_id)
    item, created = CartItem.objects.get_or_create(cart=cart, product=product)
    if not created:
        item.quantity += 1
    item.save()
    return redirect('view_cart')


def remove_from_cart(request, item_id):
    CartItem.objects.filter(id=item_id).delete()
    return redirect('view_cart')


def view_cart(request):
    cart = get_or_create_cart(request)
    return render(request, 'core/cart.html', {'cart': cart})


def checkout(request):
    cart = get_or_create_cart(request)
    form = CheckoutForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        order = form.save(commit=False)
        order.user = request.user
        order.total = sum(item.product.price *
                          item.quantity for item in cart.items.all())
        order.save()

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart.items.all().delete()

        # Redirect to payment gateway or confirmation page
        return redirect('order_success')

    return render(request, 'core/checkout.html', {'form': form, 'cart': cart})

def order_success(request):
    return render(request, 'core/order_success.html')

