from .models import Cart, CartItem
from .views import _cart_id

def cart(request):
    try:
        cart = Cart.objects.get(cart_id=_cart_id(request))
        cart_items = CartItem.objects.filter(cart=cart, active=True)
        cart_count = cart_items.count()
    except Cart.DoesNotExist:
        cart_count = 0
    return dict(cart_count=cart_count)