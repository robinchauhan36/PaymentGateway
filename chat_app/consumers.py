import json
from channels.generic.websocket import AsyncJsonWebsocketConsumer, WebsocketConsumer
from django.contrib.auth.models import User
from django.db.models import Q
from chat_app.models import *
from chat_app.serializers import *


class ChatConsumer(WebsocketConsumer):
    # Called when WebSocket connection is established, ws://

    def connect(self, *args, **kwargs):
        sender = self.scope['url_route']['kwargs']['sender']
        reciver = self.scope['url_route']['kwargs']['reciver']

        room_name = sender + reciver
        room_group_name = 'room_%s' % room_name

        chat_inst = Message.objects.filter(
            Q(created_by__username=sender, user__username=reciver) | Q(created_by__username=reciver,
                                                                       user__username=sender))

        chat = ChatDetailSerializer(chat_inst, many=True)

        async_to_sync(self.channel_layer.group_add)(
            room_group_name,
            self.channel_name
        )
        self.accept()
        self.send(
            json.dumps(chat.data)
        )

    def disconnect(self):
        self.disconnect()

    def send_message(self, event):
        sender = event['value']['sender']
        reciver = event['value']['reciver']

        chat_inst = Message.objects.filter(
            Q(created_by__username=sender, user__username=reciver) | Q(created_by__username=reciver,
                                                                       user__username=sender))

        chat = ChatDetailSerializer(chat_inst, many=True)
        self.send(
            json.dumps(chat.data)
        )
