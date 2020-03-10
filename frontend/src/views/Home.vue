<template>
  <el-container>
    <el-header></el-header>
    <el-main>
      <el-row type="flex" justify="center">
        <el-col :span="12">
          <Retrieval @inputChange="change($event)" />
        </el-col>
      </el-row>
    </el-main>
  </el-container>
</template>

<script>
// @ is an alias to /src
import Retrieval from "@/components/Retrieval.vue";

export default {
  name: "Home",
  data() {
    return {
      inputText: ""
    };
  },
  methods: {
    change(data) {
      this.inputText = data;
      this.$router.push({
        path: "/result",
        query: {
          inputText: this.inputText
        }
      });
    }
  },
  components: {
    Retrieval
  }
};
</script>
