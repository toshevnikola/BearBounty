import Vue from 'vue'
import VueRouter, { RouteConfig } from 'vue-router'
import Dashboard from './views/Dashboard.vue'
import Landing from './views/Landing.vue'
import About from './views/About.vue'
import Plans from './views/Plans.vue'
import Charts from './views/Charts.vue'
import Algorithms from './views/Algorithms.vue'
import Exchange from './views/Exchange.vue'
import Statistics from './views/Statistics.vue'
Vue.use(VueRouter)

const routes: Array<RouteConfig> = [
  
  {
    path: '/',
    name: 'Landing',
    component: Landing
  },
  {
    path: '/dashboard',
    name: 'Dashboard',
    component: Dashboard
  },
  {
    path:'/exchanges',
    name:'Exchange',
    component:Exchange
  },
  {
    path: '/about',
    name: 'About',
    component:About
  },
  {
    path: '/algorithms',
    name: 'Algorithms',
    component:Algorithms
  },
  {
    path: '/plans',
    name: 'Plans',
    component:Plans
  },
  {
    path: '/charts',
    name: 'Cryptocurrencies',
    component:Charts
  },
  {
    path:'/statistics',
    name:'Statistics',
    component:Statistics
  }
  
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
