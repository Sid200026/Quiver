from django.shortcuts import render
from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin
from loginsignup.utils import getBeaverInstance
from .models import ChatInfo


class ChatListView(LoginRequiredMixin, TemplateView):
    template_name = "chat/chat_list.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        beaverInstance = getBeaverInstance(self.request)
        response = ChatInfo.getAllURLParams(beaverInstance)
        friends = []
        for users in response:
            # The dictionary should contain the username, urlparam, profile picture
            dic = {}
            dic["urlparam"] = ChatInfo.convertUUIDToString(users.urlparam)
            friendInstance = users.member1
            if users.member1 == beaverInstance:
                friendInstance = users.member2
            dic["friend"] = friendInstance.user.username
            dic["profile"] = friendInstance.profile_photo
            friends.append(dic)
        context["friends"] = friends
        return context


class RoomView(LoginRequiredMixin, TemplateView):
    template_name = "chat/room.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        beaverInstance = getBeaverInstance(self.request)
        response = ChatInfo.getAllURLParams(beaverInstance)
        friends = []
        for users in response:
            # The dictionary should contain the username, urlparam, profile picture
            dic = {}
            dic["urlparam"] = ChatInfo.convertUUIDToString(users.urlparam)
            friendInstance = users.member1
            if users.member1 == beaverInstance:
                friendInstance = users.member2
            dic["friend"] = friendInstance.user.username
            dic["profile"] = friendInstance.profile_photo
            friends.append(dic)
        context["friends"] = friends
        urlparam = kwargs.get("urlparam")
        uuidParam = ChatInfo.convertStringToUUID(urlparam)
        response = ChatInfo.objects.get(urlparam = uuidParam)
        talkingTo = response.member1
        if beaverInstance == talkingTo:
            talkingTo = response.member2
        context["chatTo"] = talkingTo
        context["chatmssgs"] = response.getAllMessages()
        context["room_name"] = kwargs.get("urlparam")
        return context
