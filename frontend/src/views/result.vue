<template>
  <div>
    <el-row>
      <el-col :span="12" :offset="4">
        <Retrieval :value="inputText" @inputChange="change($event)" />
      </el-col>
    </el-row>
    <el-row style="margin-top: 30px;">
      <el-col :span="12" :offset="4">
        <MainList ref="main" />
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
import Qs from "qs";

export default {
  name: "Result",
  data() {
    return {
      // the text in search box
      inputText: "",
      resultList: null,
      resultNum: null
    };
  },
  created() {
    this.inputText = this.$route.query.kw;
    this.queryResults();
  },
  methods: {
    change(data) {
      this.inputText = data;
    },
    queryResults() {
      let _this = this;
      this.axios
        .get("http://192.168.1.114:8000/search", {
          params: { kw: this.inputText }
        })
        .then(function(res) {
          let resObj = Qs.parse(res)["data"];
          _this.resultNum = resObj.total;
          _this.$refs.main.initList(resObj.data);
        })
        .catch(function(error) {
          console.error(error);
        });
    }
  },
  components: { Retrieval, MainList }
};
</script>
