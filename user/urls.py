from django.urls import path
from unicodedata import category

from .views import login_view, logout_view, forgot_password_view, register_view, profile_view, \
    reset_password_view, admin_dashboard, order_detail, delete_dish_view, delete_selected, delete_category, \
    product_detail, edit_product

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/',register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', reset_password_view, name='reset_password'),
    path('profile/', profile_view, name='profile'),
    path('dashboard/', admin_dashboard, name='admin_dashboard'),
    path('order/<int:order_id>/', order_detail, name='order_detail'),
    path('delete-dish/<int:dish_id>/', delete_dish_view, name='delete_dish_view'),
    path('delete/', delete_selected, name='delete_selected'),
    path('delete-category/', delete_category, name='delete-category'),
    path('product/<int:dish_id>/', product_detail, name='product_detail'),
    path('product/edit/<int:dish_id>', edit_product, name='edit_product'),
]