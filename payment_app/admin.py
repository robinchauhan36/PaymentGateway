from django.contrib import admin
from payment_app.models import *


# Register your models here.
@admin.register(StripeAccount)
class StripeAccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'created_by', 'account_id')
