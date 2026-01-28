from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import UserRegisterAPIView, UserLoginAPIView, UserLogoutAPIView

urlpatterns = [
    path("register/", UserRegisterAPIView.as_view(), name="register-user"),
    path("login/", UserLoginAPIView.as_view(), name="login-user"),
    path("logout/", UserLogoutAPIView.as_view(), name="logout-user"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
