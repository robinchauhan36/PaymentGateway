from django.contrib import admin
from accounts.models import *


# Register your models here.
class ProfileModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'phone')


class OTPModelAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'otp', 'type', 'verify')


admin.site.register(Profile, ProfileModelAdmin)
admin.site.register(Otp, OTPModelAdmin)
