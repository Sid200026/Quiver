from django.urls import path, re_path
from .views import LoginView

app_name = 'loginsignup'

urlpatterns = [
    # path('', Landing, name="landing"),
    path('login/', LoginView.as_view(), name="login"),
    # path('signup', SignUpView.as_view(), name="signup"),
    # path('completeprofile', CompleteView.as_view(), name="complete"),
    # path('logout', LogoutUser, name="logout"),
]
