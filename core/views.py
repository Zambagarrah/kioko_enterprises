from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import Q
from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
import json
from core.utils.cart import get_or_create_cart
from core.payment.messages import get_confirmation_message
from core.utils.sms import send_sms_confirmation
from core.utils.email import send_order_email
from core.utils.payments import log_payment
from .forms import (
    CustomUserCreationForm,
    CheckoutForm,
    BankPaymentProofForm,
    OrderFilterForm,
)
from .models import (
    Product,
    Category,
    CartItem,
    OrderItem,
    Order,
)
from core.payment.gateways import (
    process_mpesa,
    process_paypal,
    process_bank,
)


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


@login_required
def checkout(request):
    cart = get_or_create_cart(request)
    form = CheckoutForm(request.POST or None)

    if request.method == 'POST' and form.is_valid():
        # Create order
        order = form.save(commit=False)
        order.user = request.user
        order.total = sum(item.product.price *
                          item.quantity for item in cart.items.all())
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

        # Dispatch payment processor
        method = form.cleaned_data['payment_method']
        gateway_map = {
            'mpesa': process_mpesa,
            'paypal': process_paypal,
            'bank': process_bank,
            # 'airtel': process_airtel,  # Temporarily disabled
        }

        processor = gateway_map.get(method)
        if processor:
            result = processor(order)

            # Log payment attempt
            log_payment(order, method, 'initiated',
                        f"{method.capitalize()} payment triggered.")

            # Send SMS confirmation
            send_sms_confirmation(
                order.user.phone_number,
                f"Order #{order.id} received. Payment method: {method.capitalize()}."
            )

            # Send order confirmation email
            send_order_email(order.user, order)

            # Handle gateway-specific response
            if method == 'paypal':
                return redirect(result)

            elif method == 'bank':
                return render(request, 'core/payment_confirmation.html', {'message': result})

            else:
                message = get_confirmation_message(method, order.id)
                return render(request, 'core/payment_confirmation.html', {'message': message})
        else:
            return render(request, 'core/payment_confirmation.html', {'message': "Invalid payment method selected."})

    return render(request, 'core/checkout.html', {'form': form, 'cart': cart})


def order_success(request):
    return render(request, 'core/order_success.html')


@csrf_exempt
def mpesa_callback(request):
    if request.method == 'POST':
        data = json.loads(request.body)

        # Extract relevant fields
        result_code = data.get('Body', {}).get(
            'stkCallback', {}).get('ResultCode')
        result_desc = data.get('Body', {}).get(
            'stkCallback', {}).get('ResultDesc')
        metadata = data.get('Body', {}).get('stkCallback', {}).get(
            'CallbackMetadata', {}).get('Item', [])

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


@csrf_exempt
def paypal_callback(request):
    order_id = request.GET.get('token')  # PayPal returns token as order ID
    access_token = get_paypal_access_token()
    url = f"{settings.PAYPAL_API_BASE}/v2/checkout/orders/{order_id}/capture"
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.post(url, headers=headers)
    response.raise_for_status()
    data = response.json()

    # Optional: update order status
    return render(request, 'core/payment_confirmation.html', {
        'message': "PayPal payment completed successfully."
    })


def upload_bank_proof(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    form = BankPaymentProofForm(request.POST or None, request.FILES or None)

    if request.method == 'POST' and form.is_valid():
        proof = form.save(commit=False)
        proof.order = order
        proof.uploaded_by = request.user
        proof.save()
        return redirect('proof_success')

    return render(request, 'core/upload_bank_proof.html', {'form': form, 'order': order})


@login_required
def printable_receipt(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    return render(request, 'core/printable_receipt.html', {'order': order})

@staff_member_required
def update_order_status(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        new_status = request.POST.get('status')
        if new_status in dict(Order.STATUS_CHOICES):
            order.status = new_status
            order.save()
    return render(request, 'core/update_order_status.html', {'order': order, 'choices': Order.STATUS_CHOICES})

@login_required
def order_history(request):
    form = OrderFilterForm(request.GET or None)
    orders = Order.objects.filter(user=request.user)

    if form.is_valid():
        status = form.cleaned_data.get('status')
        start = form.cleaned_data.get('start_date')
        end = form.cleaned_data.get('end_date')
        product = form.cleaned_data.get('product_name')

        if status:
            orders = orders.filter(status=status)
        if start:
            orders = orders.filter(created_at__gte=start)
        if end:
            orders = orders.filter(created_at__lte=end)
        if product:
            orders = orders.filter(orderitem__product__name__icontains=product)

    orders = orders.distinct().order_by('-created_at')
    return render(request, 'core/order_history.html', {'orders': orders, 'form': form})

@login_required
def request_order_support(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)
    # Stub: log or email support request
    print(f"Support requested for Order #{order.id} by {request.user.username}")
    return render(request, 'core/support_requested.html', {'order': order})

