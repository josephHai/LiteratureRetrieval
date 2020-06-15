<template>
  <div class="retrieval">
    <el-row>
      <el-col :span="20">
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
      <el-col :span="4">
        <el-button v-show="sourceBtnV" type="text" @click="sourceBtnClick"
          >检索来源</el-button
        >
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
    <el-dialog :visible.sync="sourceDialog" title="文献检索来源" width="30%">
      <div style="margin: 15px 0;"></div>
      <el-checkbox-group v-model="checkedSources">
        <el-checkbox
          v-for="source in sources"
          :label="source.en"
          :key="source.en"
          >{{ source.name }}</el-checkbox
        >
      </el-checkbox-group>
      <span slot="footer" class="dialog-footer">
        <el-button @click="sourceDialog = false">取 消</el-button>
        <el-button type="primary" @click="sourceBtnConfirm">确 认</el-button>
      </span>
    </el-dialog>
  </div>
</template>

<script>
import { getSources } from "../api/literature";
export default {
  name: "Retrieval",
  props: {
    value: {
      type: String,
      default() {
        return "";
      },
    },
    sourceBtnVisible: {
      type: Boolean,
      default() {
        return true;
      },
    },
  },
  data() {
    return {
      websocket: null,
      inputText: this.$props.value,
      sourceBtnV: this.$props.sourceBtnVisible,
      speechDialog: false,
      speechText: "请输入语音",
      sourceDialog: false,
      sources: [],
      checkedSources: ["wf"],
    };
  },
  methods: {
    sourceBtnClick() {
      this.sourceDialog = true;
      this.sources.length === 0 ? this.getSources() : "";
    },
    sourceBtnConfirm() {
      this.$session.set("sources", JSON.stringify(this.checkedSources));
      this.sourceDialog = false;
    },
    getSources() {
      getSources().then((response) => {
        this.sources = response.data;
      });
    },
    speechCapture() {
      this.initWebSocket();
    },
    initWebSocket() {
      // 初始化websocket
      const wsUri = "ws://s.c/ws/speech/";
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
        this.speechDialog = false;
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
    },
  },
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
