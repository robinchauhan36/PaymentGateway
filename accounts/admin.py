from django.contrib import admin
from accounts.models import *


# Register your models here.
@admin.register(Profile)
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'phone')
