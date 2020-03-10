<template>
  <div class="home">
    <img alt="Vue logo" src="../assets/logo.png" />
    <Retrieval msg="Welcome to Your Vue.js App" />
  </div>
</template>

<script>
// @ is an alias to /src
import Retrieval from "@/components/Retrieval.vue";

export default {
  name: "Home",
  components: {
    Retrieval
  }
};
</script>
