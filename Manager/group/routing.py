from django.urls import re_path
from .consumers import SignallingConsumer

websocket_urlpatterns = [
    re_path(r'ws/signalRoom/(?P<room_name>\w+)/$',
            SignallingConsumer.as_asgi()),
]
