from django.conf.urls import url

from . import consumers

websocket_urlpatterns = [
    url(r'^retro/(?P<session_name>[^/]+)/$', consumers.SessionConsumer),
]
