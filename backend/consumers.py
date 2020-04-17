from channels.generic.websocket import WebsocketConsumer
from backend.recognition import WsParam, RecognitionWebsocket

import logging

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


class SpeechConsumer(WebsocketConsumer):
    def connect(self):
        self.accept()

    def disconnect(self, code):
        pass

    def receive(self, text_data=None, bytes_data=None):
        logging.info('开始')

        ws_param = WsParam(APPId='5e33cbd7', APIKey='0b8832e558059b6334c2a8042f8034be',
                           APISecret='ff9061ae93b39844e1acd7524aec74c8',
                           AudioFile=r'')

        ws_url = ws_param.create_url()
        ws = RecognitionWebsocket(ws_url, self, ws_param)
        ws.connect()
        ws.run_forever()


