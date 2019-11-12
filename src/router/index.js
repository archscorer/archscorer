import Vue from 'vue'
import VueRouter from 'vue-router'
import Home from '@/views/Home.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'home',
    component: Home
  },
  {
    path: '/events',
    name: 'events',
    // route level code-splitting
    // this generates a separate chunk (about.[hash].js) for this route
    // which is lazy-loaded when the route is visited.
    component: () => import(/* webpackChunkName: "about" */ '@/views/Events.vue')
  },
  {
    path: '/event/:id',
    name: 'event',
    component: () => import('@/views/Event.vue')
  },
  {
    path: '/statistics',
    name: 'statistics',
    component: () => import('@/views/Statistics.vue')
  },
  {
    path: '/clubs',
    name: 'clubs',
    component: () => import('@/views/Clubs.vue')
  }
]

const router = new VueRouter({
  routes
})

export default router
