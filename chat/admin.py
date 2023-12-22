from django.contrib import admin
from chat.models import Message, Chat

class MessageAdmin(admin.ModelAdmin):    
    fields = ('text','created_at', 'author', 'receiver', 'chat')    
    list_display = ('created_at', 'author', 'text', 'receiver',  'chat')    
    search_fields = ('text',)

# Register your models here.
admin.site.register(Message, MessageAdmin)
admin.site.register(Chat)