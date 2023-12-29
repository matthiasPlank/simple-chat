from django.db import models
from datetime import date , datetime
from django.conf import settings
from django.utils.timezone import now


# Create your models here.


class Chat(models.Model): 
     created_at = models.DateField(default=date.today)
    
class Message(models.Model):
    text = models.CharField(max_length=500) 
    created_at = models.DateTimeField(default=now , blank=True)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE , related_name='chat_message_set', default=None, blank=True, null=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name='author_message_set')
    receiver = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE , related_name='receiver_message_set')

