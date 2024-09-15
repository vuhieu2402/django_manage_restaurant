from django.shortcuts import render, redirect
from .models import TableReservations
from django.contrib.auth.decorators import login_required

from django.contrib import messages
# Create your views here.


def book_table(request):
    if request.method == 'POST':
        user = request.user
        if not user.is_authenticated:
            messages.error(request, "Please log in to book a table.")
            return redirect('login')  # Chuyển hướng đến trang đăng nhập nếu chưa đăng nhập

        name = request.POST.get('name')
        phone_number = request.POST.get('phone_number')
        table_number = request.POST.get('table_number')
        reservation_date = request.POST.get('reservation_date')
        time = request.POST.get('time')

        # Lưu thông tin đặt bàn
        reservation = TableReservations.objects.create(
            user_id=user,
            name=name,
            phone_number=phone_number,
            table_number=table_number,
            reservation_date=reservation_date,
            time = time
        )

        messages.success(request, 'Table booked successfully!')
        return redirect('book')  # Hiển thị lại form với thông báo thành công

    return render(request, 'book/book_table.html')