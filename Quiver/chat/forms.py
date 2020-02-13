from django import forms
from .models import ChatMessage, ChatInfo
from loginsignup.utils import getBeaverInstance


class ChatMessageForm(forms.ModelForm):
    class Meta:
        model = ChatMessage
        fields = ["message"]

    def createNewMessage(self, urlparam, request):
        status = super().is_valid()
        if not status:
            return status
        message = self.cleaned_data.get("message")
        beaver = getBeaverInstance(request)
        uuidUrlparam = ChatInfo.convertStringToUUID(urlparam)
        response = ChatMessage.createMessage(uuidUrlparam, beaver, message)
        return response.get("status")
