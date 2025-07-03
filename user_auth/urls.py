from django.urls import path, include
from .views import UserRegisterView, UserLoginView, OTPVerifyView
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('register/', UserRegisterView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('otp-verify/', OTPVerifyView.as_view(), name='otp_verify'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout'),
]