from django.urls import path
from chat_app.consumers import *

websocket_urlpatterns = [
    path('ws/connection/<sender>/<reciver>', ChatConsumer.as_asgi())
]
