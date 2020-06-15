<template>
  <div class="box">
    <div class="item" :key="index" v-for="(item, index) in resultList">
      <div class="title">
        <a style="text-decoration: none;" :href="item.link">{{ item.title }}</a>
      </div>
      <div class="authors">
        {{ item.authors }}
      </div>
      <div class="content">
        {{ item.brief }}
      </div>
      <div class="source">
        <span>来源: </span>

        <span :key="index" v-for="(source, index) in item.sources">
          <a class="source-link" :href="source.link">{{ source.name }}</a>
        </span>
      </div>
      <el-divider></el-divider>
    </div>
  </div>
</template>

<script>
export default {
  name: "MainList",
  data() {
    return {
      resultList: [],
    };
  },
  methods: {
    initList(arr) {
      this.resultList = arr;
    },
  },
};
</script>

<style scoped>
.item {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  text-align: start;
  line-height: 24px;
}
.title {
  font-size: 17px;
  color: #1a0dab;
}
.authors {
  font-size: 13px;
  color: #006621;
}
.content {
  font-size: 13px;
  color: #222222;
}
.source {
  font-size: 13px;
  color: #1a0dab;
}
.source-link {
  margin-left: 5px;
  text-decoration: none;
}
</style>
