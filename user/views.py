from encodings.punycode import adapt

from django.shortcuts import render
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
from .models import  Customer
from django.contrib.auth.hashers import make_password
from django.contrib.auth.decorators import login_required
from django.utils.encoding import force_str
from django.utils.encoding import force_bytes



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
            return redirect('home')
            # return JsonResponse({'refresh': str(refresh), 'access': str(refresh.access_token)})

        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)
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