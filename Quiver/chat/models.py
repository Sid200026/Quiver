from django.db import models
import uuid
from .constants import MessageConstants
from .managers import ChatMessageManager
from cryptography.fernet import Fernet

generatePublicKey = Fernet.generate_key().decode("utf8")


class ChatInfo(models.Model):
    member1 = models.ForeignKey(
        "loginsignup.Beaver",
        on_delete=models.CASCADE,
        related_name="memberOne",
        related_query_name="memOne",
    )
    member2 = models.ForeignKey(
        "loginsignup.Beaver",
        on_delete=models.CASCADE,
        related_name="memberTwo",
        related_query_name="memTwo",
    )
    urlparam = models.UUIDField(
        "URL Parameter", primary_key=True, default=uuid.uuid4(), editable=False
    )
    publicKey = models.CharField(
        "Encryption key", max_length=32, default=generatePublicKey, editable=False
    )

    class Meta:
        verbose_name_plural = "Chat Informations"

    def __str__(self):
        return f"{self.member1} <-> {self.member2}"

    # When someone creates a new friend call this method
    @classmethod
    def createChatInformation(cls, member1, member2):
        cls.objects.get_or_create(member1=member1, member2=member2)

    # Returns all the url param for a particular user in the form of an
    # queryset
    @classmethod
    def getAllURLParams(cls, beaver):
        return cls.objects.select_related("member1").filter(
            member1=beaver
        ) | cls.objects.select_related("member2").filter(member2=beaver)

    @classmethod
    def convertUUIDToString(cls, uniqueid):
        return str(uniqueid).replace("-","")

    @classmethod
    def convertStringToUUID(cls, string):
        return uuid.UUID(string)

    def getAllMessages(self):
        getMessages = self.messages.all()
        response = []
        for messageDetail in getMessages:
            messageInfo = {}
            messageInfo["message"] = ChatMessage.decryptMessage(
                messageDetail.message, urlparam=messageDetail.chatinfo.urlparam
            )
            messageInfo["sender"] = messageDetail.sender.user.username
            response.append(messageInfo)
        return response


class ChatMessage(models.Model):
    objects = ChatMessageManager()
    chatinfo = models.ForeignKey(
        ChatInfo,
        on_delete=models.CASCADE,
        related_name="messages",
        related_query_name="message",
    )
    sender = models.ForeignKey(
        "loginsignup.Beaver",
        on_delete=models.CASCADE,
        related_name="messages_sent",
        related_query_name="message_sent",
    )
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
            return {"status": False, "error": MessageConstants.notAFriend}
        publicKey = chat_info.publicKey.encode("utf8")
        fernet = Fernet(publicKey)
        # Convert the message into byte string and then into string
        return fernet.decrypt(message.encode("utf8")).decode("utf8")

    # Sender must be a beaver instance
    # urlparam must be an UUID
    @classmethod
    def createMessage(cls, urlparam, sender, message):
        chat_info = None
        try:
            chat_info = ChatInfo.objects.get(urlparam=urlparam)
        except BaseException:
            return {"status": False, "error": MessageConstants.notAFriend}
        publicKey = chat_info.publicKey.encode("utf8")
        fernet = Fernet(publicKey)
        # Convert the message into byte and then convert the encrypted byte
        # string into string
        encryptedMessage = fernet.encrypt(message.encode("utf8")).decode("utf8")
        cls.objects.create(chatinfo=chat_info, sender=sender, message=encryptedMessage)
        return {"status": True, "error": None}
