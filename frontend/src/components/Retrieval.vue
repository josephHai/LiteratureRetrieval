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
      <span>这是语音信息</span>
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
      speechText: "这里是语音信息"
    };
  },
  methods: {
    speechCapture() {
      this.speechDialog = true;
      this.initWebSocket();
    },
    initWebSocket() {
      // 初始化websocket
      const wsUri = "ws://127.0.0.1:8000/ws/speech/";
      this.websocket = new WebSocket(wsUri);
      this.websocket.onmessage = this.websocketOnMessage;
      this.websocket.onopen = this.websocketOnOpen;
      this.websocket.onerror = this.websocketOnError;
      this.websocket.onclose = this.websocketClose;
    },
    websocketOnOpen() {
      // 连接建立之后执行send方法发送数据
      let actions = { message: "12345" };
      this.websocketSend(JSON.stringify(actions));
    },
    websocketOnError() {
      // 连接建立失败重连
      this.initWebSocket();
    },
    websocketOnMessage(e) {
      // 数据接收
      const response = JSON.parse(e.data).message;
      this.inputText = response;
      this.websocket.close();
      this.$emit("inputChange", response);
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
