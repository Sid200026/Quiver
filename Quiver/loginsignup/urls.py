from django.urls import path
from .views import (
    LoginView,
    SignUpView,
    ResetPasswordView,
    LogoutView,
    ResendCodeView,
    CompleteView,
    FriendsListView,
)
from django.views.generic import TemplateView

app_name = "loginsignup"
landing_page_template = "loginsignup/landing.html"

urlpatterns = [
    path("", TemplateView.as_view(template_name=landing_page_template), name="landing"),
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("complete/", CompleteView.as_view(), name="complete"),
    path("reset/", ResetPasswordView.as_view(), name="reset"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("resendpassword/", ResendCodeView.as_view(), name="resend"),
    path("friends/", FriendsListView.as_view(), name="friends"),
]
