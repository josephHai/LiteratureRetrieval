<template>
  <div class="retrieval">
    <el-row>
      <el-col :span="24">
        <el-input v-model="inputText" prefix-icon="el-icon-search">
          <el-tooltip
            slot="append"
            class="item"
            effect="dark"
            content="按语音搜索"
            placement="bottom"
          >
            <el-button
              icon="el-icon-microphone"
              @click="speechCapture"
            ></el-button>
          </el-tooltip>
        </el-input>
      </el-col>
    </el-row>
    <el-dialog :fullscreen="true" :visible.sync="speechDialog">
      <el-row
        type="flex"
        justify="center"
        align="middle"
        style="margin-top: 250px;"
      >
        <el-col :span="4">
          <span class="content">{{ speechText }}</span>
        </el-col>
        <el-col :span="4">
          <el-button class="microphone-btn" circle>
            <div class="icon-warp">
              <i class="el-icon-microphone" @click="speechDialog = false"></i>
            </div>
          </el-button>
        </el-col>
      </el-row>
    </el-dialog>
  </div>
</template>

<script>
export default {
  name: "Retrieval",
  props: {
    value: {
      type: String,
      default() {
        return "";
      }
    }
  },
  data() {
    return {
      websocket: null,
      inputText: this.$props.value,
      speechDialog: false,
      speechText: "请输入语音"
    };
  },
  methods: {
    speechCapture() {
      this.initWebSocket();
    },
    initWebSocket() {
      // 初始化websocket
      const wsUri = "ws://192.168.1.114:8000/ws/speech/";
      this.websocket = new WebSocket(wsUri);
      this.websocket.onmessage = this.websocketOnMessage;
      this.websocket.onopen = this.websocketOnOpen;
      this.websocket.onerror = this.websocketOnError;
      this.websocket.onclose = this.websocketClose;
    },
    websocketOnOpen() {
      // 连接建立之后执行send方法发送数据
      let actions = { message: "start" };
      this.websocketSend(JSON.stringify(actions));
    },
    websocketOnError() {
      // 连接建立失败重连
      this.initWebSocket();
    },
    websocketOnMessage(e) {
      // 数据接收
      const response = JSON.parse(e.data).message;
      const status = JSON.parse(e.data).status;
      this.speechText = response;
      console.log(status === 0);
      if (status === 2) {
        this.websocket.close();
        this.$emit("inputChange", response);
      } else if (status === 0) {
        this.speechDialog = true;
      }
    },
    websocketSend(Data) {
      // 数据发送
      this.websocket.send(Data);
    },
    websocketClose(e) {
      // 关闭
      console.log("断开连接", e);
    }
  }
};
</script>

<style>
.microphone-btn {
  width: 150px;
  height: 150px;
}
.icon-warp {
  font-size: 70px;
  color: red;
}
.content {
  font-size: 1.5rem;
  color: gray;
}
</style>
