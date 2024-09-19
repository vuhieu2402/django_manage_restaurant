from django.urls import path
from .views import HomePageView, product_view, add_product
from. import views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('menu/', views.menu_view, name='menu'),
    path('products/', product_view, name='products'),
    path('add_product/', add_product, name='add_product')
]