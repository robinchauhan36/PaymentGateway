from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(CityMaster)
class CityAdmin(admin.ModelAdmin):
    list_display = ('id', 'name')


@admin.register(Movies)
class MoviesAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'city', 'time')


@admin.register(UserBooking)
class UserBookingsAdmin(admin.ModelAdmin):
    list_display = ('id', 'movie', 'user')