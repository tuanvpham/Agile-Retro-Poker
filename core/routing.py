from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^retro/(?P<session_name>[^/]+)/$', consumers.RetroConsumer),
    url(r'^poker/(?P<session_name>[^/]+)/$', consumers.PokerConsumer),
    url(r'^lobby/(?P<session_name>[^/]+)/$', consumers.LobbyConsumer),
]
