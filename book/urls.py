from .views import book_table
from django.urls import path


urlpatterns = [
    path('book/', book_table, name='book'),  # Booking a table
]