from django.urls import path
from . import views
from .views import admin_chat, get_chat_messages, send_message

urlpatterns = [
    path('send_message/', views.send_message, name='send_message'),
    path('load_chatbox/', views.load_chatbox, name='load_chatbox'),
    path('admin/chat/', admin_chat, name='admin_chat'),
    path('admin/get_chat_messages/<int:session_id>/', get_chat_messages, name='get_chat_messages'),
    path('admin/send_message/', send_message, name='send_message'),

]
