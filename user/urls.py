from django.urls import path
from .views import login_view, logout_view, forgot_password_view, register_view, profile_view, reset_password_view, admin_dashboard

urlpatterns = [
    path('login/', login_view, name='login'),
    path('register/',register_view, name='register'),
    path('logout/', logout_view, name='logout'),
    path('forgot-password/', forgot_password_view, name='forgot_password'),
    path('reset_password/<uidb64>/<token>/', reset_password_view, name='reset_password'),
    path('profile/', profile_view, name='profile'),
    path('admin-dashboard/', admin_dashboard, name='admin_dashboard'),
]