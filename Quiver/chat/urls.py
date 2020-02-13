from django.urls import path
from .views import ChatListView, room

app_name = "chat"

urlpatterns = [
    path("<str:urlparam>/", room, name="room"),
    path("", ChatListView.as_view(), name="chatList"),
]
