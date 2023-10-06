from django.urls import path
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from . import views


urlpatterns = [
    path("", views.UserInfo.as_view()),
    path("signup", views.Signup.as_view()),
    path("username_duplicate", views.UsernameDuplicate.as_view()),
    path("email_duplicate", views.EmailDuplicate.as_view()),
    path(
        "login/token",
        views.CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),
    path("login/token/refresh", TokenRefreshView.as_view(), name="token_refresh"),
    path("logout", views.Logout.as_view()),
    path("withdrawl", views.Withdrawal.as_view()),
]
