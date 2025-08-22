from .models import Cart

def get_or_create_cart(request):
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
    else:
        session_key = request.session.session_key or request.session.save()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart
