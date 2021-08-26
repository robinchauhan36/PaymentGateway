from django.db import models
from django.contrib.auth.models import User
from accounts.models import ModelMixin
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync


# Create your models here.
class Message(ModelMixin):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    message = models.TextField(default='')
    file = models.FileField(null=True, blank=True)
    is_read = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        channel_layer = get_channel_layer()
        data = {
            'sender': self.created_by.username,
            'reciver': self.user.username
        }
        channel_name = 'room_' + self.created_by.username + self.user.username

        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"{channel_name}",
            {
                "type": "send_message",
                "value": data,
            },
        )

        channel_name_user = 'room_' + self.user.username + self.created_by.username

        async_to_sync(channel_layer.group_send)(
            f"{channel_name_user}",
            {
                "type": "send_message",
                "value": data,
            },
        )

        super(Message, self).save(*args, **kwargs)
