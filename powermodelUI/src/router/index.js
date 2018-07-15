import Vue from 'vue'
import Router from 'vue-router'
import Index from '@/components/Index'
import Results from '@/components/Results'

Vue.use(Router)

export default new Router({
  routes: [
    {
      path: '/',
      name: 'Index',
      component: Index
    },
    {
      path: '/Results',
      name: 'Results',
      component: Results
    }
  ]
})
