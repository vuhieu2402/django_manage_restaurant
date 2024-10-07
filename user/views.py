

from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.urls import reverse
from django.core.mail import send_mail
from django.contrib.auth import get_user_model

from chatbox.models import ChatSession
from .models import  Customer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_str
from django.utils.encoding import force_bytes
from order.models import Order, OrderDetails
from home.models import Dish, Category
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Sum
from django.utils import timezone
from datetime import timedelta
import json
from django.core.serializers.json import DjangoJSONEncoder
from django import template



from rest_framework_simplejwt.token_blacklist.models import BlacklistedToken, OutstandingToken


# Create your views here.

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request,username=username, password=password)

        if user is not None:
            login(request, user)
            refresh = RefreshToken.for_user(user)

            # Lưu token vào session hoặc gửi lại cho client
            request.session['access_token'] = str(refresh.access_token)
            request.session['refresh_token'] = str(refresh)

            # Kiểm tra nếu người dùng là dashboard (superuser)
            if user.is_superuser:
                return redirect('admin_dashboard')  # Chuyển hướng đến trang quản lý dashboard

            # Nếu là customer thì chuyển hướng đến trang home
            return redirect('home')  # Chuyển hướng đến URL 'home'

        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

        #     return redirect('home')
        #     # return JsonResponse({'refresh': str(refresh), 'access': str(refresh.access_token)})
        #
        # else:
        #     return JsonResponse({'error': 'Invalid credentials'}, status=400)
    return render(request, 'user/login.html')



User = get_user_model()


def forgot_password_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        user = User.objects.filter(email=email).first()

        if user:
            # Tạo link reset password và gửi qua email
            reset_link = request.build_absolute_uri(
                reverse('reset_password', kwargs={
                    'uidb64': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': default_token_generator.make_token(user)
                })
            )
            send_mail(
                'Reset Password',
                f'Please click the link below to reset your password: {reset_link}',
                'vuhieu24022002h@gmail.com',  # Địa chỉ email gửi
                [email],  # Địa chỉ email nhận
                fail_silently=False,
            )
            return JsonResponse({'message': 'Password reset email sent successfully'})
        else:
            return JsonResponse({'error': 'Email does not exist'}, status=400)

    return render(request, 'user/forgot_password.html')

def reset_password_view(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        if request.method == 'POST':
            new_password = request.POST.get('password')
            user.set_password(new_password)
            user.save()
            return JsonResponse({'message': 'Password reset successfully'})
        return render(request, 'user/reset_password.html', {'validlink': True})
    else:
        return render(request, 'user/reset_password.html', {'validlink': False})

def register_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        phone = request.POST['phone']
        address = request.POST['address']

        if Customer.objects.filter(username=username).exists():
            return JsonResponse({'error': 'Username already exists'}, status=400)

        if Customer.objects.filter(email=email).exists():
            return JsonResponse({'error': 'Email already exists'}, status=400)

        customer = Customer.objects.create(
            username=username,
            email=email,
            password=make_password(password),
            phone = phone,
            address = address,
        )

        refresh = RefreshToken.for_user(customer)
        # return JsonResponse({'refresh': str(refresh),
        #                      'access': str(refresh.access_token)}, status=201)
        return redirect('home')
    return render(request, 'user/login.html')


@login_required
def profile_view(request):
    customer = request.user
    context = {
        'customer': customer
    }
    return render(request, 'user/profile.html', context)

def logout_view(request):
    try:
        refresh_token = request.POST.get('refresh_token')
        token = RefreshToken(refresh_token)
        token.blacklist()
    except Exception as e:
        return JsonResponse({'error': str(e)}, status=400)

    logout(request)
    return redirect('home')



def is_admin(user):
    return user.is_superuser and user.is_authenticated

@user_passes_test(is_admin, login_url='/login/')
def admin_dashboard(request):
    # Lấy ngày hiện tại và tính toán tuần
    today = timezone.now().date()
    start_of_week = today - timedelta(days=today.weekday())
    dates_in_week = [start_of_week + timedelta(days=i) for i in range(7)]
    days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

    # Lấy doanh thu mỗi ngày trong tuần
    revenues_per_day = [
        float(Order.objects.filter(order_date__date=date).aggregate(total=Sum('total_price'))['total'] or 0)
        for date in dates_in_week
    ]

    # Chuẩn bị dữ liệu cho biểu đồ doanh thu theo ngày
    revenue_chart_data = {
        'labels': days_of_week,
        'data': revenues_per_day,
    }
    revenue_chart_data_json = json.dumps(revenue_chart_data, cls=DjangoJSONEncoder)

    # Lấy danh sách các món ăn và tính toán doanh thu, số lượng bán
    dishes = Dish.objects.all()
    dish_names = []
    dish_quantities = []
    dish_revenues = []

    for dish in dishes:
        total_quantity = OrderDetails.objects.filter(dish_id=dish).aggregate(total=Sum('quantity'))['total'] or 0
        total_revenue = (OrderDetails.objects.filter(dish_id=dish).aggregate(total=Sum('quantity'))['total'] or 0) * dish.price
        dish_quantities.append(float(total_quantity))
        dish_revenues.append(float(total_revenue))
        dish_names.append(dish.name)

    # Chuẩn bị dữ liệu cho biểu đồ doanh thu hoặc số lượng bán của từng món
    dish_chart_data = {
        'labels': dish_names,
        'quantities': dish_quantities,
        'revenues': dish_revenues,
    }
    dish_chart_data_json = json.dumps(dish_chart_data, cls=DjangoJSONEncoder)

    orders = Order.objects.all().order_by('-id')
    # context cần có thêm chat_sessions cho navbar
    chat_sessions = ChatSession.objects.select_related('customer').all()

    context = {
        'revenue_chart_data_json': revenue_chart_data_json,
        'dish_chart_data_json': dish_chart_data_json,
        'orders': orders,
        'chat_sessions': chat_sessions,
    }
    return render(request, 'dashboard/index.html', context)






def order_detail(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    order_items = OrderDetails.objects.filter(order_id=order)


    context = {
        'order': order,
        'order_items': order_items,
    }
    return render(request, 'dashboard/order_detail.html', context)


@user_passes_test(is_admin, login_url='/login/')
def delete_dish_view(request, dish_id):
    product = get_object_or_404(Dish, id=dish_id)
    product.delete()
    return redirect('products')

@user_passes_test(is_admin, login_url='/login/')
def delete_selected(request):
    if request.method == 'POST':
        selected_dishes = request.POST.getlist('selected_dishes')
        if selected_dishes is not None:
            Dish.objects.filter(id__in=selected_dishes).delete()
    return redirect('products')

@user_passes_test(is_admin, login_url='/login/')
def delete_category(request, category_id):
    category = get_object_or_404(Category, id=category_id)
    category.delete()
    return redirect('products')

@user_passes_test(is_admin, login_url='/login/')
def product_detail(request, dish_id):
    product = get_object_or_404(Dish, id=dish_id)
    categories = Category.objects.all()
    context = {
        'product': product,
        'categories': categories,
    }
    return render(request, 'dashboard/product_detail.html', context)

def edit_product(request, dish_id):
    product = get_object_or_404(Dish, id=dish_id)
    categories = Category.objects.all()
    if request.method == 'POST':
        product.name = request.POST.get('name')  # Sửa lại ở đây
        product.description = request.POST.get('description')
        product.price = request.POST.get('price')
        product.category_id = request.POST.get('category')

        if request.FILES.get('url_img'):
            product.url_img = request.FILES.get('url_img')

        product.save()
        return redirect('products')

    return render(request, 'dashboard/product_detail.html', {'product': product, 'categories': categories})
