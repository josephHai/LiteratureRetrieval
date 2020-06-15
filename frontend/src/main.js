/* eslint-disable */
import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "./plugins/element.js";
import vueAxios from "vue-axios";
import axios from "axios";
import ElementUI from "element-ui";
import VueSession from "vue-session";

Vue.config.productionTip = false;
Vue.use(ElementUI);

Vue.use(vueAxios, axios);
Vue.use(VueSession);

new Vue({
  router,
  store,
  render: (h) => h(App),
}).$mount("#app");
