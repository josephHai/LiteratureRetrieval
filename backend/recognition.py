# -*- coding=utf-8 -*-
import requests
import json
import base64
import os
import logging
import speech_recognition as sr
from urllib.parse import urlencode
import time


class Recognition():

    def __init__(self):
        self.APP_ID = 'wBQ721zREoj9NioqDjou0krf'
        self.APP_SECRET = 'sMv0LQ8HC9eIBzcmD3SxhaiVgx3CKdrs'
        self.file_name = os.getcwd() + "/backend/audio/" + str(int(time.time())) + ".wav"
        self.token_file = 'backend/access_token.json'
        self.now = int(time.time())

    def get_token(self):
        print(os.getcwd())
        with open(self.token_file, 'r') as f:
            data = json.load(f)
        if data['expires_in'] < self.now:
            logging.info('开始获取token...')

            params = {'grant_type': 'client_credentials',
                      'client_id': self.APP_ID,
                      'client_secret': self.APP_SECRET}
            post_data = urlencode(params)
            url = 'http://openapi.baidu.com/oauth/2.0/token'
            res = requests.post(url, post_data)

            token = json.loads(res.text)['access_token']
            expires_in = json.loads(res.text)['expires_in']
            data['token'] = token
            data['expires_in'] = self.now + expires_in
            with open(self.token_file, 'w') as f:
                f.write(json.dumps(data, indent=4))
        else:
            token = data['token']
        return token

    def audio(self):
        logging.info('开始识别语音文件...')
        with open(self.file_name, "rb") as f:
            speech = base64.b64encode(f.read()).decode('utf-8')
        size = os.path.getsize(self.file_name)
        token = self.get_token()
        headers = {'Content-Type': 'application/json'}
        url = "https://vop.baidu.com/server_api"
        data = {
            "format": "wav",
            "rate": "16000",
            "dev_pid": "1536",
            "speech": speech,
            "cuid": "TEDxPY",
            "len": size,
            "channel": 1,
            "token": token,
        }

        req = requests.post(url, json.dumps(data), headers)
        result = json.loads(req.text)

        if result["err_msg"] == "success.":
            return result['result'][0]
        else:
            return -1

    def run(self):
        logging.basicConfig(level=logging.INFO)

        r = sr.Recognizer()
        # 启用麦克风
        mic = sr.Microphone()
        logging.info('录音中...')
        with mic as source:
            # 降噪
            r.adjust_for_ambient_noise(source)
            audio = r.listen(source)
        print(os.getcwd())
        with open(self.file_name, "wb") as f:
            # 将麦克风录到的声音保存为wav文件
            f.write(audio.get_wav_data(convert_rate=16000))
        logging.info('录音结束，识别中...')
        return self.audio()


if __name__ == "__main__":
    r = Recognition()
    r.run()