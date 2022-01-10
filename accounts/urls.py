from django.urls import path
from accounts.views import *

urlpatterns = [
    path('register', RegistrationAPI.as_view()),
    path('login', UserLoginAPI.as_view()),
]
