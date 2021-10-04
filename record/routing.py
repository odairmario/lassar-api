from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
        re_path(r"^record/$",consumers.RecordConsumer.as_asgi()),
        ]
