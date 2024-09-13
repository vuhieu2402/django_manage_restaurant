from django.urls import path
from .views import HomePageView
from. import views

urlpatterns = [
    path('', HomePageView.as_view(), name='home'),
    path('menu/', views.menu_view, name='menu'),

]