import hashlib
import base64
import hmac
import json
from urllib.parse import urlencode
import logging

from wsgiref.handlers import format_date_time
import datetime
from datetime import datetime
import time
from time import mktime
import _thread as thread
import pyaudio
import numpy as np

from ws4py.client.threadedclient import WebSocketClient
from scipy import fftpack

logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)


STATUS_FIRST_FRAME = 0  # 第一帧的标识
STATUS_CONTINUE_FRAME = 1  # 中间帧标识
STATUS_LAST_FRAME = 2  # 最后一帧的标识

CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 16000
THRESHOLD = 7000


class WsParam(object):
    # 初始化
    def __init__(self, APPId, APIKey, APISecret, AudioFile):
        self.APPId = APPId
        self.APIKey = APIKey
        self.APISecret = APISecret
        self.AudioFile = AudioFile

        # 公共参数(common)
        self.CommonArgs = {
            'app_id': self.APPId
        }
        # 业务参数(business)，更多个性化参数可在官网查看
        self.BusinessArgs = {
            'domain': 'iat',
            'language': 'zh_cn',
            'accent': 'mandarin',
            'vinfo': 1,
            'vad_eos': 10000,
            'dwa': 'wpgs',
            'ptt': 0
        }

    # 生成url
    def create_url(self):
        url = 'wss://ws-api.xfyun.cn/v2/iat'
        # 生成RFC1123格式的时间戳
        now = datetime.now()
        date = format_date_time(mktime(now.timetuple()))

        # 拼接字符串
        signature_origin = 'host: ' + 'ws-api.xfyun.cn' + '\n'
        signature_origin += 'date: ' + date + '\n'
        signature_origin += 'GET ' + '/v2/iat ' + 'HTTP/1.1'
        # 进行hmac-sha256进行加密
        signature_sha = hmac.new(self.APISecret.encode('utf-8'), signature_origin.encode('utf-8'),
                                 digestmod=hashlib.sha256).digest()
        signature_sha = base64.b64encode(signature_sha).decode(encoding='utf-8')

        authorization_origin = 'api_key="%s", algorithm="%s", headers="%s", signature="%s"' % (
            self.APIKey, 'hmac-sha256', 'host date request-line', signature_sha)
        authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
        # 将请求的鉴权参数组合为字典
        v = {
            'authorization': authorization,
            'date': date,
            'host': 'ws-api.xfyun.cn'
        }
        # 拼接鉴权参数，生成url
        url = url + '?' + urlencode(v)
        # print('date: ',date)
        # print('v: ',v)
        # 此处打印出建立连接时候的url,参考本demo的时候可取消上方打印的注释，比对相同参数时生成的url与自己代码生成的url是否一致
        # print('websocket url :', url)
        return url


class RecognitionWebsocket(WebSocketClient):
    def __init__(self, url, pre_websocket, ws_param):
        super().__init__(url)
        self.pre_websocket = pre_websocket
        self.ws_param = ws_param
        self.rec_text = {}

    # 收到websocket消息的处理
    def received_message(self, message):
        message = message.__str__()

        try:
            code = json.loads(message)['code']
            sid = json.loads(message)['sid']
            status = json.loads(message)['data']['status']
            if code != 0:
                err_msg = json.loads(message)['message']
                logging.error('sid:%s call error:%s code is:%s' % (sid, err_msg, code))

            else:
                data = json.loads(message)['data']['result']
                ws = data['ws']
                pgs = data['pgs']
                sn = data['sn']

                result = ''
                logging.info(message)
                for i in ws:
                    for w in i['cw']:
                        result += w['w']
                if pgs == 'rpl':
                    rg = data['rg']
                    self.rec_text.update({rg[0]: result})
                    for i in range(rg[0] + 1, rg[1]):
                        self.rec_text.pop(i, '404')
                else:
                    self.rec_text[sn] = result
                self.pre_websocket.send(text_data=json.dumps({
                    'message': ''.join(self.rec_text.values()),
                    'status': status
                }))
                logging.info('识别结果为: {}'.format(self.rec_text))
        except Exception as e:
            logging.info(message)
            logging.error('receive msg,but parse exception: {}'.format(e))

    # 收到websocket错误的处理
    @staticmethod
    def on_error(self, error):
        logging.error(error)

    # 收到websocket关闭的处理
    def closed(self, code, reason=None):
        logging.info('语音识别通道关闭' + str(code) + str(reason))

    # 收到websocket连接建立的处理
    def opened(self):
        def run(*args):
            interval = 0.04  # 发送音频间隔(单位:s)
            status = STATUS_FIRST_FRAME  # 音频的状态信息，标识音频是第一帧，还是中间帧、最后一帧
            audio = pyaudio.PyAudio()
            stream = audio.open(format=FORMAT,
                                channels=CHANNELS,
                                rate=RATE,
                                input=True)
            stop_flag = 0
            stop_flag2 = 1

            logging.info('开始录音')
            self.pre_websocket.send(text_data=json.dumps({
                'message': '开始录音',
                'status': STATUS_FIRST_FRAME
            }))

            while True:
                buf = stream.read(CHUNK)
                rt_buf = np.frombuffer(buf, np.dtype('<i2'))

                # 傅里叶变换
                fft_temp_buf = fftpack.fft(rt_buf, rt_buf.size, overwrite_x=True)
                fft_data = np.abs(fft_temp_buf)[0:fft_temp_buf.size // 2 + 1]

                # print(sum(fft_data) // len(fft_data))
                # 判断麦克风是否停止，判断说话是否结束，
                # 麦克风阈值，默认7000
                if sum(fft_data) // len(fft_data) > THRESHOLD:
                    stop_flag += 1
                else:
                    stop_flag2 += 1
                one_second = int(RATE / CHUNK) * 1.5
                if stop_flag2 + stop_flag > one_second:
                    if stop_flag2 > one_second:
                        status = STATUS_LAST_FRAME
                    else:
                        stop_flag2 = 0
                        stop_flag = 0

                # 第一帧处理
                # 发送第一帧音频，带business 参数
                # appid 必须带上，只需第一帧发送
                if status == STATUS_FIRST_FRAME:
                    d = {'common': self.ws_param.CommonArgs,
                         'business': self.ws_param.BusinessArgs,
                         'data': {'status': 0, 'format': 'audio/L16;rate=16000',
                                  'audio': str(base64.b64encode(buf), 'utf-8'),
                                  'encoding': 'raw'}}
                    d = json.dumps(d)
                    self.send(d)
                    status = STATUS_CONTINUE_FRAME
                # 中间帧处理
                elif status == STATUS_CONTINUE_FRAME:
                    d = {'data': {'status': 1, 'format': 'audio/L16;rate=16000',
                                  'audio': str(base64.b64encode(buf), 'utf-8'),
                                  'encoding': 'raw'}}
                    self.send(json.dumps(d))
                # 最后一帧处理
                elif status == STATUS_LAST_FRAME:
                    d = {'data': {'status': 2, 'format': 'audio/L16;rate=16000',
                                  'audio': str(base64.b64encode(buf), 'utf-8'),
                                  'encoding': 'raw'}}
                    self.send(json.dumps(d))
                    logging.info('录音结束')
                    time.sleep(1)

                    stream.stop_stream()
                    stream.close()
                    audio.terminate()

                    break
                # 模拟音频采样间隔
                time.sleep(interval)
            self.closed(1000, '')

        thread.start_new_thread(run, ())