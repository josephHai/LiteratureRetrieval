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
  methods: {
    change(data) {
      this.$router.push({
        path: "/result",
        query: {
          kw: data,
        },
      });
    },
  },
  components: {
    Retrieval,
  },
};
</script>
