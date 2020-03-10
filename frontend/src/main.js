import Vue from "vue";
import App from "./App.vue";
import router from "./router";
import store from "./store";
import "./plugins/element.js";
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
  Dialog
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

new Vue({
  router,
  store,
  render: h => h(App)
}).$mount("#app");
