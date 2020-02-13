from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin


class ChatListView(LoginRequiredMixin, TemplateView):
    template_name = "chat/chat_list.html"


def room(request, urlparam):
    return render(request, "chat/room.html", {"room_name": urlparam})
