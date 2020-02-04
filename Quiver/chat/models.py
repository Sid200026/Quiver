from django.db import models
import uuid
from loginsignup.models import Beaver
from .constants import MessageConstants
from simplecrypt import encrypt, decrypt
from django.utils.crypto import get_random_string
import string

generatePublicKey = get_random_string(
    length=16,
    allowed_chars=string.ascii_uppercase +
    string.digits)


class ChatInfo(models.Model):
    member1 = models.ForeignKey(
        Beaver,
        on_delete=models.CASCADE,
        related_name="memberOne",
        related_query_name="memOne")
    member2 = models.ForeignKey(
        Beaver,
        on_delete=models.CASCADE,
        related_name="memberTwo",
        related_query_name="memTwo")
    urlparam = models.UUIDField(
        "URL Parameter",
        primary_key=True,
        default=uuid.uuid4(),
        editable=False)
    publicKey = models.CharField(
        "Encryption key",
        max_length=16,
        default=generatePublicKey,
        editable=False)

    class Meta:
        verbose_name_plural = "Chat Informations"

    def __str__(self):
        return f"{self.sender} -> {self.receiver}"

    # When someone creates a new friend call this method
    @classmethod
    def createChatInformation(cls, member1, member2):
        cls.objects.get_or_create(member1=member1, member2=member2)

    # Returns all the url param for a particular user in the form of an
    # queryset
    @classmethod
    def getAllURLParams(cls, beaver):
        return cls.objects.select_related('member1').filter(
            member1=beaver) | cls.objects.select_related('member2').filter(
            member2=beaver)


class ChatMessage(models.Model):
    chatinfo = models.OneToOneField(
        ChatInfo,
        on_delete=models.CASCADE,
        related_name="messages",
        related_query_name="message")
    sender = models.ForeignKey(
        Beaver,
        on_delete=models.CASCADE,
        related_name="messages_sent",
        related_query_name="message_sent")
    message = models.TextField(null=False)
    timeSent = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Chat Messages"

    def __str__(self):
        return f"{self.chatinfo} || Sent : {self.timeSent}"

    @classmethod
    def decryptMessage(cls, message, urlparam):
        chat_info = None
        try:
            chat_info = ChatInfo.objects.get(urlparam=urlparam)
        except BaseException:
            return {
                'status': False,
                'error': MessageConstants.notAFriend,
            }
        publicKey = chat_info.publicKey
        return decrypt(publicKey, message).decode("utf8")

    # Sender must be a beaver instance

    def createMessage(self, urlparam, sender, message):
        chat_info = None
        try:
            chat_info = ChatInfo.objects.get(urlparam=urlparam)
        except BaseException:
            return {
                'status': False,
                'error': MessageConstants.notAFriend
            }
        publicKey = self.chatinfo.publicKey
        encryptedMessage = encrypt(publicKey, message)
        ChatInfo.object.create(
            chatinfo=chat_info,
            sender=sender,
            message=encryptedMessage,
        )
