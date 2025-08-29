from django.shortcuts import render, redirect
from django.shortcuts import render, get_object_or_404
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import json
from .utils import get_or_create_cart
from .forms import (
    CustomUserCreationForm,
    CheckoutForm,
)
from .models import (
    Product,
    Category,
    CartItem,
    OrderItem,
)
from core.payment.gateways import (
    process_mpesa,
    process_airtel,
    process_paypal,
    process_bank,
)
from core.payment.messages import get_confirmation_message

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
    return render(request, 'core/signup.html', {'form': form}) #was register.html


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
        # Create order
        order = form.save(commit=False)
        order.user = request.user
        order.total = sum(item.product.price * item.quantity for item in cart.items.all())
        order.save()

        # Create order items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )
        cart.items.all().delete()

        # Dispatch payment gateway
        method = form.cleaned_data['payment_method']
        gateway_map = {
            'mpesa': process_mpesa,
            'airtel': process_airtel,
            'paypal': process_paypal,
            'bank': process_bank,
        }
        processor = gateway_map.get(method)
        if processor:
            processor(order)
            message = get_confirmation_message(method, order.id)
        else:
            message = "Invalid payment method selected."

        return render(request, 'core/payment_confirmation.html', {'message': message})

    return render(request, 'core/checkout.html', {'form': form, 'cart': cart})

def order_success(request):
    return render(request, 'core/order_success.html')



@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Extract relevant fields
        result_code = data.get('Body', {}).get('stkCallback', {}).get('ResultCode')
        result_desc = data.get('Body', {}).get('stkCallback', {}).get('ResultDesc')
        metadata = data.get('Body', {}).get('stkCallback', {}).get('CallbackMetadata', {}).get('Item', [])

        # Optional: log metadata or update order status
        print("M-Pesa Callback Received:", result_desc)

        # Respond to Safaricom
        return JsonResponse({"ResultCode": 0, "ResultDesc": "Accepted"})

    return JsonResponse({"error": "Invalid request"}, status=400)

@csrf_exempt
def airtel_callback(request):
    data = json.loads(request.body)
    print("Airtel callback received:", data)
    return JsonResponse({"status": "received"})


