<template>
  <div>
    <el-row>
      <el-col :span="12" :offset="4">
        <Retrieval
          :value="listQuery.kw"
          @inputChange="change($event)"
          :source-btn-visible="false"
        />
      </el-col>
    </el-row>
    <el-row style="margin-top: 30px;">
      <el-col v-loading="resLoading" :span="12" :offset="4">
        <MainList ref="main" />
        <pagination
          v-show="total > 0"
          :total="total"
          :limit.sync="listQuery.limit"
          :page.sync="listQuery.page"
          @pagination="getList"
        />
      </el-col>
    </el-row>
  </div>
</template>

<script>
import Retrieval from "../components/Retrieval";
import MainList from "../components/MainList";
import Pagination from "../components/Pagination";
import { getLiterature } from "../api/literature";

export default {
  name: "Result",
  data() {
    return {
      resultList: null,
      total: 0,
      listQuery: {
        page: 1,
        limit: 20,
        kw: "",
        sources: [],
      },
      resLoading: false,
    };
  },
  created() {
    this.listQuery.kw = this.$route.query.kw;
    this.getList();
  },
  methods: {
    change(data) {
      this.listQuery.kw = data.value;
    },
    getList() {
      this.listQuery.sources = this.$session.get("sources");
      this.resLoading = true;
      getLiterature(this.listQuery).then((response) => {
        this.total = response.data.total;
        this.$refs.main.initList(response.data.items);
        this.resLoading = false;
      });
    },
  },
  components: { Retrieval, MainList, Pagination },
};
</script>
