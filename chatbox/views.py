import json

from django.http import JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone
from .models import ChatSession, Message

def send_message(request):
    if request.method == 'POST':
        content = request.POST.get('message')
        customer = request.user

        if not content or not customer.is_authenticated:
            return redirect('home')  # Chuyển hướng nếu không có nội dung hoặc người dùng không đăng nhập

        # Tạo hoặc lấy session chat của khách hàng
        chat_session, _ = ChatSession.objects.get_or_create(customer=customer)

        # Tạo tin nhắn mới
        Message.objects.create(
            chat_session=chat_session,
            sender=customer,
            content=content,
            is_admin=False,
            timestamp=timezone.now()
        )

        return redirect('home')  # Sau khi gửi tin nhắn, redirect về trang chính

def load_chatbox(request):
    customer = request.user
    if not customer.is_authenticated:
        return JsonResponse({'messages': []})  # Trả về danh sách rỗng nếu không đăng nhập

    # Lấy session chat của khách hàng
    chat_session, _ = ChatSession.objects.get_or_create(customer=customer)

    # Lấy toàn bộ tin nhắn
    messages = Message.objects.filter(chat_session=chat_session).order_by('timestamp')

    # Tạo danh sách tin nhắn để trả về
    message_list = [{'sender': msg.sender.username, 'content': msg.content} for msg in messages]

    return JsonResponse({'messages': message_list})


def admin_chat(request):
    # Lấy tất cả các session chat và liên kết với customer
    chat_sessions = ChatSession.objects.select_related('customer').all()

    # Kiểm tra nếu có session nào không
    if not chat_sessions:
       print('no')

    # Truyền dữ liệu chat sessions vào template
    print('yes')
    return render(request, 'dashboard/index.html', {'chat_sessions': chat_sessions})


def get_chat_messages(request, session_id):
    # Kiểm tra phương thức GET và đảm bảo yêu cầu là XMLHttpRequest
    if request.method == 'GET' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        chat_session = get_object_or_404(ChatSession, id=session_id)
        messages = Message.objects.filter(chat_session=chat_session).order_by('timestamp')

        # Định dạng dữ liệu phản hồi
        messages_data = [
            {'sender': msg.sender.username if msg.is_admin else 'Khách hàng', 'content': msg.content}
            for msg in messages
        ]

        return JsonResponse({'messages': messages_data})

    return JsonResponse({'error': 'Invalid request method'}, status=400)


def send_message(request):
    if request.method == 'POST':
        session_id = request.POST.get('session_id')
        message_content = request.POST.get('message')

        chat_session = get_object_or_404(ChatSession, id=session_id)
        Message.objects.create(
            chat_session=chat_session,
            sender=request.user,  # Giả định admin đang gửi tin nhắn
            content=message_content,
            is_admin=True
        )

        messages = Message.objects.filter(chat_session=chat_session).order_by('timestamp')

        return render(request, 'dashboard/index.html', {
            'messages': messages,
            'current_session_id': session_id,
        })
