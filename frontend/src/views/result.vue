<template>
  <div>
    <el-row>
      <el-col :span="12" :offset="4">
        <Retrieval :value="inputText" @inputChange="change($event)" />
      </el-col>
    </el-row>
    <el-row style="margin-top: 30px;">
      <el-col :span="12" :offset="4">
        <MainList />
        <el-pagination
          background
          layout="prev, pager, next"
          :total="100"
        ></el-pagination>
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Retrieval from "../components/Retrieval";
import MainList from "../components/MainList";

export default {
  name: "Result",
  data() {
    return {
      // the text in search box
      inputText: ""
    };
  },
  created() {
    this.inputText = this.$route.query.text;
  },
  methods: {
    change(data) {
      this.inputText = data;
    }
  },
  components: { Retrieval, MainList }
};
</script>
