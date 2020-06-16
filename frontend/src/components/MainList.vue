<template>
  <div class="box">
    <div v-if="resultList.length">
      <div class="item" :key="index" v-for="(item, index) in resultList">
        <div class="title">
          <a style="text-decoration: none;" :href="item.link">{{
            item.title
          }}</a>
        </div>
        <div class="authors">
          {{ item.authors }}
        </div>
        <div class="brief-text">
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
    <div v-else class="no-data">
      没有数据，请尝试其他关键词
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
* {
  font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB",
    "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
}
.item {
  display: flex;
  flex-direction: column;
  justify-content: flex-start;
  text-align: start;
  line-height: 24px;
}
.title {
  font-size: 20px;
  color: #1a0dab;
  margin-bottom: 10px;
}
.authors {
  font-size: 16px;
  color: #006621;
  margin-bottom: 10px;
}
.brief-text {
  overflow: hidden;
  text-overflow: ellipsis;
  display: -webkit-box;
  -webkit-box-orient: vertical;
  -webkit-line-clamp: 2;
  font-size: 16px;
  color: #222222;
  margin-bottom: 10px;
  letter-spacing: 2px;
}
.source {
  font-size: 15px;
  color: #1a0dab;
}
.source-link {
  margin-left: 5px;
  text-decoration: none;
}
.no-data {
  color: #909399;
}
</style>
