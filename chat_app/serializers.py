from rest_framework import serializers
from chat_app.models import *
from accounts.serializers import *


class ChatSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = '__all__'


class ChatDetailSerializer(serializers.ModelSerializer):
    user = UserChatSerializer()
    created_by = UserChatSerializer()

    class Meta:
        model = Message
        fields = '__all__'
