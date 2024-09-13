from django.shortcuts import render
from .models import Order, OrderDetails
# Create your views here.

def order_history(request):
    customer = request.user  # Nếu bạn sử dụng hệ thống auth
    orders = Order.objects.filter(user_id=customer).order_by('-order_date')

    return render(request, 'order/order_history.html', {'orders': orders})
