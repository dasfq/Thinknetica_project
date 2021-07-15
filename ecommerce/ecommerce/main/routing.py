from django.urls import re_path
from . import consumer
from channels.routing import ProtocolTypeRouter, URLRouter


websocket_urlpatterns = URLRouter([
    re_path("live-chat/", consumer.LiveChatConsumer.as_asgi(), name='live-chat'),
])