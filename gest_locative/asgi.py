import os
from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.auth import AuthMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "gest_locative.settings")

# IMPORTANT : charger Django avant d'importer ton routing
django_asgi_app = get_asgi_application()

# importer ton routing **après** que Django soit prêt
import gest_locative.routing

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": AuthMiddlewareStack(
        URLRouter(
            gest_locative.routing.websocket_urlpatterns
        )
    ),
})
