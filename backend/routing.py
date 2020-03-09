from django.urls import path
from backend.consumers import SpeechConsumer

websocket_urlpatterns = [
    path('ws/speech/', SpeechConsumer)
]