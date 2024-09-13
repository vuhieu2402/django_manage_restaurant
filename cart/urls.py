from .views import cart_view, add_to_cart, remove_from_cart
from django.urls import path




urlpatterns = [
    path('cart/', cart_view, name='cart'),
    path('add-to-cart/<int:dish_id>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<int:item_id>/', remove_from_cart, name='remove-from-cart'),
]