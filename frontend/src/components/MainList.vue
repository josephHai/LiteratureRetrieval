<template>
  <div class="box">
    <div class="item" :key="item" v-for="item in resultList">
      <div class="title">
        {{ item }}
        <span class="type">[图书]</span>
        <a style="text-decoration: none" href="#">计算机系统安全</a>
      </div>
      <div class="authors">
        曹天杰， 张立江， 张爱娟 - 2014 - idl.hbdlib.cn
      </div>
      <div class="content">
        本书全面系统地介绍了计算机系统安全知识,
        反映了计算机系统安全领域的新概念, 新发展. 全书分十三章, 涉及了密码学,
        物理安全, 运行安全(风险分析, 审计跟踪, 备份与恢复, 应急),
        信息安全(网络安全, 访问控制, 认证等) 等内容. 本书概念准确, 选材合理,
        结构紧凑, 条理清晰 …
      </div>
      <div class="source">
        <span>来源: </span>
        <a class="source-link" href="#">百度学术</a>
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
      resultList: [1, 2, 3, 4]
    };
  }
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
.type {
  font-size: 13px;
  margin-right: 4px;
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
