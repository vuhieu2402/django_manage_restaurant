from django.db import models
from user.models import Customer
from django.utils import timezone

# Create your models here.

class ChatSession(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    started_at = models.DateTimeField(default=timezone.now)
    last_activity = models.DateTimeField(auto_now=True)


class Message(models.Model):
    chat_session = models.ForeignKey(ChatSession, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(Customer, on_delete=models.CASCADE)  # Dùng để biết ai gửi tin nhắn (customer hay admin)
    content = models.TextField()
    timestamp = models.DateTimeField(default=timezone.now)
    is_admin = models.BooleanField(default=False)  # True nếu tin nhắn từ admin, False nếu từ khách hàng

