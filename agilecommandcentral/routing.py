from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from core.auth_websocket import QueryEmailAuthMiddlewareStack
import core.routing

application = ProtocolTypeRouter({
    # (http->django views is added by default)
    'websocket': QueryEmailAuthMiddlewareStack(
        URLRouter(
            core.routing.websocket_urlpatterns
        )
    ),
})
