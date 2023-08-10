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
    component: () => import('@/views/Events.vue')
  },
  {
    path: '/event/:id',
    name: 'event',
    component: () => import('@/views/event/Event.vue'),
  },
  {
    path: '/series',
    name: 'series_list',
    component: () => import('@/views/Series.vue')
  },
  {
    path: '/series/:id',
    name: 'series',
    component: () => import('@/views/series/Series.vue')
  },
  {
    path: '/statistics/archer/rounds',
    name: 'past_rounds',
    component: () => import('@/views/ArcherRounds.vue')
  },
  {
    path: '/statistics/records',
    name: 'records',
    component: () => import('@/views/Records.vue')
  },
  {
    path: '/clubs',
    name: 'clubs',
    component: () => import('@/views/Clubs.vue')
  },
  {
    path: '/club/:id',
    name: 'club',
    component: () => import('@/views/club/Club.vue')
  },
  {
    path: '/accounts/profile',
    name: 'profile',
    component: () => import('@/views/user/ArcherProfile.vue')
  },
  {
    path: '*',
    component: Home
  }
]

const router = new VueRouter({
  routes
})

export default router
