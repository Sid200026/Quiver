# chat/consumers.py
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
import json
from .forms import ChatMessageForm


class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.room_name = self.scope["url_route"]["kwargs"]["room_name"]
        self.room_group_name = "chat_%s" % self.room_name
        # Join room group
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json["message"]
        username = self.scope["user"].username
        status = await self.sendMessageToDB(message)
        dic = {
            "message": message,
            "sender": username,
        }
        if status:
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name, {"type": "chat_message", "dic": dic}
            )

    # Receive message from room group
    async def chat_message(self, event):
        message = event["dic"]["message"]
        sender = event["dic"]["sender"]
        # Send message to WebSocket
        await self.send(text_data=json.dumps({"message": message, "sender": sender}))

    @database_sync_to_async
    def sendMessageToDB(self, message):
        form = ChatMessageForm({"message": message})
        user = self.scope["user"]
        status = form.createNewMessage(self.room_name, user)
        return status
