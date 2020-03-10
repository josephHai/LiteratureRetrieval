<template>
  <div id="app">
    <retrieval />
  </div>
</template>

<script>
import Retrieval from "./components/Retrieval.vue";

export default {
  name: "app",
  components: {
    Retrieval
  }
};
</script>

<style>
#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
