import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth import get_user_model
from bailti.models import Conversation, Message

User = get_user_model()

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.conversation_id = self.scope['url_route']['kwargs']['conversation_id']
        self.room_group_name = f"chat_{self.conversation_id}"

        user = self.scope["user"]
        # Vérifier que l'utilisateur fait partie de la conversation
        if not user.is_authenticated:
            await self.close()
            return

        is_participant = await database_sync_to_async(self._is_participant)()
        if not is_participant:
            await self.close()
            return

        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    def _is_participant(self):
        try:
            conv = Conversation.objects.get(pk=self.conversation_id)
            return conv.participants.filter(pk=self.scope["user"].id).exists()
        except Conversation.DoesNotExist:
            return False

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    # Receive message from WebSocket
    async def receive(self, text_data=None, bytes_data=None):
        data = json.loads(text_data)
        message = data.get("message", "").strip()
        if not message:
            return

        user = self.scope["user"]
        # Sauvegarder en DB
        msg_obj = await database_sync_to_async(self._save_message)(user.id, message)

        # Distribuer à tous les clients du groupe
        await self.channel_layer.group_send(
            self.room_group_name,
            {
                "type": "chat_message",
                "message": message,
                "sender_id": user.id,
                "sender_username": user.username,
                "created_at": msg_obj.created_at.isoformat(),
                "message_id": msg_obj.id,
            }
        )

    def _save_message(self, user_id, content):
        user = User.objects.get(pk=user_id)
        conv = Conversation.objects.get(pk=self.conversation_id)
        msg = Message.objects.create(conversation=conv, sender=user, content=content)
        return msg

    # Receive message from room group
    async def chat_message(self, event):
        # Send message to WebSocket
        await self.send(text_data=json.dumps({
            "message": event["message"],
            "sender_id": event["sender_id"],
            "sender_username": event["sender_username"],
            "created_at": event["created_at"],
            "message_id": event["message_id"],
        }))
