from django.contrib import admin
from .models import *


# Register your models here.
@admin.register(PaymentDetail)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'amount', 'type')
