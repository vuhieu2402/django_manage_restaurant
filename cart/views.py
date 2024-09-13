from django.shortcuts import render, get_object_or_404, redirect
from home.models import Dish
from . models import Cart, CartItems
from decimal import Decimal

# Create your views here.
def add_to_cart(request, dish_id):
    if not request.user.is_authenticated:
        return redirect('login')

    customer = request.user
    cart, created = Cart.objects.get_or_create(user_id=customer)
    dish = get_object_or_404(Dish, id=dish_id)

    cart_item, created = CartItems.objects.get_or_create(cart_id=cart, dish_id=dish)
    if not created:
        cart_item.quantity += 1
    else:
        cart_item.quantity = 1
    cart_item.save()
    return redirect('home')

def cart_view(request):
    if not request.user.is_authenticated:
        return redirect('login')

    customer = request.user

    try:
        cart = Cart.objects.get(user_id=customer)
        cart_items = CartItems.objects.filter(cart_id=cart)  # Lấy các món trong gi�� hàng
    except Cart.DoesNotExist:
        cart_items = []

    total_price = Decimal('0.00')
    for item in cart_items:
        item.total_price = Decimal(item.dish_id.price) * item.quantity
        item.total_price = item.total_price.quantize(Decimal('0.01'))
        total_price += item.total_price

    shipping_cost = Decimal(6.94).quantize(Decimal('0.01'))
    grand_total = total_price + shipping_cost

    return render(request, 'cart/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'shipping_cost': shipping_cost,
        'grand_total': grand_total
    })


def remove_from_cart(request, item_id):
    if not request.user.is_authenticated:
        return redirect('login')

    customer = request.user
    try:
        cart = Cart.objects.get(user_id=customer)
        cart_item = CartItems.objects.get(id=item_id, cart_id=cart)
        cart_item.delete()
    except (CartItems.DoesNotExist, Cart.DoesNotExist):
        pass

    return redirect('cart')
