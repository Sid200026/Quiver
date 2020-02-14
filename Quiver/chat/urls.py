from django.urls import path
from .views import ChatListView, RoomView

app_name = "chat"

urlpatterns = [
    path("<str:urlparam>/", RoomView.as_view(), name="room"),
    path("", ChatListView.as_view(), name="chatList"),
]
