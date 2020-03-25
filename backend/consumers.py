from channels.generic.websocket import AsyncWebsocketConsumer
import json
from backend.recognition import Recognition


class SpeechConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()

    async def disconnect(self, code):
        pass

    async def receive(self, text_data=None, bytes_data=None):
        recognition = Recognition()
        text = recognition.run()

        await self.send(text_data=json.dumps({
            'message': text
        }))