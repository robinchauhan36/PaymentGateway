from rest_framework import routers
from django.urls import path, include

from .views import *

router = routers.DefaultRouter()

router.register(r'city', CityViewSet, basename='city')
router.register(r'movies', MoviesViewSet, basename='movies')
router.register(r'user_booking', UserMovieBookingViewSet, basename='user_booking')

urlpatterns = [
    path('', include(router.urls)),
]
