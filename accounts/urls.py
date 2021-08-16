from django.urls import path
from accounts.views import *

urlpatterns = [
    path('register', RegistrationAPI.as_view()),
    path('login', UserLoginAPI.as_view()),
    path('password/change', PasswordChangeAPI.as_view()),
    path('otp', OTPView.as_view()),
    path('reset/password', PasswordResetView.as_view())
]
