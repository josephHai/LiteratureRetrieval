<template>
  <el-container>
    <el-header>
      <el-row type="flex" justify="center">
        <el-col :span="12">
          <Retrieval :value="inputText" @inputChange="change($event)" />
        </el-col>
      </el-row>
    </el-header>
    <el-container>
      <el-aside width="200">Aside</el-aside>
      <el-main>Main</el-main>
    </el-container>
  </el-container>
</template>

<script>
import Retrieval from "../components/Retrieval";

export default {
  name: "Result",
  data() {
    return {
      inputText: ""
    };
  },
  created() {
    this.inputText = this.$route.query.inputText;
  },
  methods: {
    change(data) {
      this.inputText = data;
    }
  },
  components: { Retrieval }
};
</script>
