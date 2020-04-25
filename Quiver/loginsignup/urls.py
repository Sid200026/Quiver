from django.urls import path
from .views import (
    LandingView,
    LoginView,
    SignUpView,
    ResetPasswordView,
    LogoutView,
    ResendCodeView,
    CompleteView,
    FriendsListView,
    UpdateProfileView,
    BeaverListView,
    UpdatePasswordView,
    filter_friends,
    beaver_filter,
    unfriend,
)

app_name = "loginsignup"

urlpatterns = [
    path("", LandingView.as_view(), name="landing"),
    path("login/", LoginView.as_view(), name="login"),
    path("signup/", SignUpView.as_view(), name="signup"),
    path("complete/", CompleteView.as_view(), name="complete"),
    path("reset/", ResetPasswordView.as_view(), name="reset"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("resendpassword/", ResendCodeView.as_view(), name="resend"),
    path("friends/", FriendsListView.as_view(), name="friends"),
    path("discover/", BeaverListView.as_view(), name="discover"),
    path("update/reset/", UpdatePasswordView.as_view(), name="passupdate"),
    path("update/", UpdateProfileView.as_view(), name="update"),
    path("ajax/friends/filter/", filter_friends),
    path("ajax/discover/filter/", beaver_filter),
    path("ajax/unfriend/", unfriend),
]
