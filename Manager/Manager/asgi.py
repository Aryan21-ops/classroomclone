import os

import django
from channels.auth import AuthMiddlewareStack
from channels.http import AsgiHandler
from channels.routing import ProtocolTypeRouter, URLRouter
import group.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Manager.settings')
django.setup()

application = ProtocolTypeRouter({
    "http": AsgiHandler(),
    "websocket": AuthMiddlewareStack(
        URLRouter(
            group.routing.websocket_urlpatterns,
        )
    )
    # Just HTTP for now. (We can add other protocols later.)
})
