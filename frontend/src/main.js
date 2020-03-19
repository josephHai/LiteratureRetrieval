import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "./plugins/element.js";
import vueAxios from "vue-axios";
import axios from "axios";
import {
  Button,
  Input,
  Container,
  Header,
  Main,
  Aside,
  Col,
  Row,
  Tooltip,
  Dialog,
  Pagination,
  Divider
} from "element-ui";

Vue.config.productionTip = false;
Vue.use(Button);
Vue.use(Input);
Vue.use(Container);
Vue.use(Header);
Vue.use(Main);
Vue.use(Aside);
Vue.use(Col);
Vue.use(Row);
Vue.use(Tooltip);
Vue.use(Dialog);
Vue.use(Pagination);
Vue.use(Divider);

Vue.use(vueAxios, axios);

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
