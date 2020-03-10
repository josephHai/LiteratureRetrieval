import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "./plugins/element.js";
import { Input } from "element-ui";

Vue.config.productionTip = false;
Vue.use(Input);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
