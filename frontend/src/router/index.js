import Vue from 'vue'
import Router from 'vue-router'
import Retrieval from '@/components/Retrieval'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'index',
      component: Retrieval
    }
  ]
})
