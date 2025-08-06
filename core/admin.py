from django.contrib import admin
from .models import ChatLog

@admin.register(ChatLog)
class ChatLogAdmin(admin.ModelAdmin):
    list_display = ('user', 'user_message', 'bot_response', 'created_at')
    search_fields = ('user__username', 'user_message', 'bot_response')
    list_filter = ('created_at',)
