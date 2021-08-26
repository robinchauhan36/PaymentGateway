from django.contrib import admin
from chat_app.models import *


# Register your models here.
class ChatAdmin(admin.ModelAdmin):
    list_display = ('created_by', 'user', 'is_read', 'created_on')


admin.site.register(Message, ChatAdmin)
