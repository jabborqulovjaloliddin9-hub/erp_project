import json
from channels.generic.websocket import AsyncWebsocketConsumer
from asgiref.sync import sync_to_async
from .models import Group, ChatMessage

class GroupChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.group_id = self.scope['url_route']['kwargs']['group_id']
        self.room_group_name = f'chat_{self.group_id}'
        self.user = self.scope['user']
        if self.user.is_anonymous:
            await self.close()
            return
        has_access = await self.check_access(self.user, self.group_id)
        if not has_access:
            await self.close()
            return
        await self.channel_layer.group_add(self.room_group_name, self.channel_name)
        await self.accept()

    async def disconnect(self, close_code):
        await self.channel_layer.group_discard(self.room_group_name, self.channel_name)

    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        await self.save_message(self.user, self.group_id, message)
        await self.channel_layer.group_send(
            self.room_group_name,
            {'type': 'chat_message', 'message': message, 'sender': self.user.username}
        )

    async def chat_message(self, event):
        await self.send(text_data=json.dumps({'message': event['message'], 'sender': event['sender']}))

    @sync_to_async
    def check_access(self, user, group_id):
        if user.role == 'admin': return True
        try:
            group = Group.objects.get(id=group_id)
            if user.role == 'teacher' and group.teacher == user: return True
            if user.role == 'student' and group.students.filter(id=user.id).exists(): return True
        except Group.DoesNotExist: pass
        return False

    @sync_to_async
    def save_message(self, user, group_id, message):
        group = Group.objects.get(id=group_id)
        ChatMessage.objects.create(sender=user, group=group, message=message)
